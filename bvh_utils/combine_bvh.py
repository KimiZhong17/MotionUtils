'''
XSense 动捕数据后处理与合并脚本
written by Kimi Zhong
Sept.24th, 2024
'''

import os
import argparse
from common.bvh_manager import read_bvh, write_bvh
from common.common import sorted_alphanumeric, write_csv

def merge_bvh_files(bvh_files, output_file, csv_file, inv_fps_scale=1, normalization=False):
    bvh_files = sorted_alphanumeric(bvh_files)
    hierarchy = None
    motions = []
    frame_count = 0
    csv_data = []

    for file_path in bvh_files:
        hierarchy_lines, _, frame_time, motion_lines = read_bvh(file_path)

        # scale frame time
        frame_time *= inv_fps_scale
        
        # 如果是第一个文件，存储Hierarchy部分
        if hierarchy is None:
            hierarchy = hierarchy_lines
        
        # 抽帧
        resampled_motion_lines = [line.strip() for i, line in enumerate(motion_lines) if i % inv_fps_scale == 0]

        # 每一段动画数据根据自己的第一帧进行 normalization
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

        # 记录每个文件的起始帧和结束帧
        start_frame = frame_count + 1
        end_frame = frame_count + len(resampled_motion_lines) 
        csv_data.append([file_path, start_frame, end_frame, len(resampled_motion_lines)])

        # 确保每一行motion数据都按行拼接，并添加换行符
        motions.extend([line.strip() + '\n' for line in resampled_motion_lines])

        # 更新帧数
        frame_count += len(resampled_motion_lines)

    # 写入拼接后的BVH文件
    write_bvh(output_file, hierarchy, frame_count, frame_time, motions)

    # 写入CSV文件
    csv_headers = ['File Name', 'Start Frame', 'End Frame', 'nFrames']
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
        out_file = os.path.join(args.out_folder, 'merged_file_' + task_name + '.bvh')
        csv_file = os.path.join(args.out_folder, 'output_data_' + task_name + '.csv')
        inv_fps_scale = args.inv_fps_scale
        normalization = args.normalization
        bvh_files = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if f.endswith('.bvh')]
        merge_bvh_files(bvh_files, out_file, csv_file, inv_fps_scale, normalization)
    except Exception as e:
        print(e)