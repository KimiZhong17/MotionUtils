'''
XSens 动捕数据后处理与合并脚本
written by Kimi Zhong
Sept.24th, 2024
'''

import os
import argparse
from common.bvh_manager import read_bvh, write_bvh
from common.common import sorted_alphanumeric, write_csv

def merge_bvh_files(bvh_files, out_prefix, csv_prefix, inv_fps_scale=1, normalization=False, max_frames_per_file=10000):
    '''
    Merge a bunch of BVH files
    @param bvh_files[List[Str]]:        a list of bvh files to manipulate
    @param out_prefix[Str]:             prefix of output BVH files
    @param csv_prefix[Str]:             prefix of output CSV files
    @param inv_fps_scale[Int]:          inverse scale of current FPS
    @param normalization[Boolean]:      whether to normalize motion base on the first frame (except the T-pose frame) of each
    @param max_frames_per_file[Int]:    maximum number of frames per file
    '''
    bvh_files = sorted_alphanumeric(bvh_files)
    hierarchy = None
    motions = []
    frame_count = 0
    csv_data = []
    csv_headers = ['File Name', 'Start Frame', 'End Frame', 'nFrames']
    out_index = 1

    for file_path in bvh_files:
        # reading bvh
        hierarchy_lines, _, frame_time, motion_lines = read_bvh(file_path)

        # scale frame time
        frame_time *= inv_fps_scale
        
        # save hierarchy if this is the first
        if hierarchy is None:
            hierarchy = hierarchy_lines
        
        # resampling motion
        resampled_motion_lines = [line.strip() for i, line in enumerate(motion_lines) if i % inv_fps_scale == 0]

        # normalize motion base on the first frame of each
        if normalization:
            x0, z0 = 0, 0
            for i, line in enumerate(resampled_motion_lines):
                if i > 0:
                    values = line.strip().split(' ')
                    if i == 1:
                        x0, z0 = float(values[0]), float(values[2])
                    xt, zt = float(values[0]) - x0, float(values[2]) - z0
                    values[0], values[2] = "{:.6f}".format(xt), "{:.6f}".format(zt)
                    resampled_motion_lines[i] = ' '.join(values)
                    
        if frame_count + len(resampled_motion_lines) > max_frames_per_file:
            # write spliced bvh
            out_file = f"{out_prefix}_{str(out_index).zfill(3)}.bvh"
            write_bvh(out_file, hierarchy, frame_count, frame_time, motions)
            
            # write corresponding csv file
            csv_file = f"{csv_prefix}_{str(out_index).zfill(3)}.csv"
            write_csv(csv_file, csv_headers, csv_data)
            
            # reset
            out_index += 1
            motions = []
            frame_count = 0
            csv_data = []

        # record the start and end frame of each motion into a csv format
        start_frame = frame_count + 1
        end_frame = frame_count + len(resampled_motion_lines) 
        csv_data.append([file_path, start_frame, end_frame, len(resampled_motion_lines)])

        # splicing motion lines and add line breaks
        motions.extend([line.strip() + '\n' for line in resampled_motion_lines])

        # update frame count
        frame_count += len(resampled_motion_lines)

    # write the last BVH and CSV file if any frames remain
    if frame_count + len(resampled_motion_lines) > max_frames_per_file:
        out_file = f"{out_prefix}_{str(out_index).zfill(3)}.bvh"
        write_bvh(out_file, hierarchy, frame_count, frame_time, motions)
        
        csv_file = f"{csv_prefix}_{str(out_index).zfill(3)}.csv"
        write_csv(csv_file, csv_headers, csv_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='动捕数据后处理与合并')
    parser.add_argument('--src_folder', help='原始动捕bvh数据地址', type=str, required=True)
    parser.add_argument('--out_folder', help='输出的整合bvh和csv地址', type=str, default='.')
    parser.add_argument('--task_name', help='本次处理的特定名称，将会出现在输出的文件的后缀', type=str, default='')
    parser.add_argument('--inv_fps_scale', help='帧率的缩小倍数', type=int, default=2)
    parser.add_argument('--normalization', help='是否将每个动画的开头归一化到(0,0)点', type=bool, default=False)
    args = parser.parse_args()
    try:
        src_folder = args.src_folder
        task_name = args.task_name
        out_prefix = os.path.join(args.out_folder, 'merged_file_' + task_name)
        csv_prefix = os.path.join(args.out_folder, 'output_data_' + task_name)
        inv_fps_scale = args.inv_fps_scale
        normalization = args.normalization
        bvh_files = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if f.endswith('.bvh')]
        merge_bvh_files(bvh_files, out_prefix, csv_prefix, inv_fps_scale, normalization)
    except Exception as e:
        print(e)