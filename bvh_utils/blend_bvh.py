'''
XSens 动捕数据融合脚本
written by Kimi Zhong
Oct.21th, 2024
'''

import os
from common.bvh_manager import read_bvh, write_bvh

def blend(bvh_files, src_bvh, src_frame_range, indices_to_replace, out_dir):
    '''
    A function to blend part of the reference motion into targeted motions
    @param bvh_files[List[Str]]:        a list of bvh files to manipulate
    @param src_bvh[Str]:                source bvh file
    @param src_frame_range[List[Int]]:  the range of frames to set as reference
    @param indices_to_replace[Int]:     indices of joints that would be blended (replaced)
    @param out_dir[Str]:                output folder
    '''
    ref_data = []
    
    # 获取reference数据
    hierarchy, _, _, src_motion_lines = read_bvh(src_bvh)
    
    # 获取用于替换的源数据
    for j in range(src_frame_range[0], src_frame_range[1]):
        src_motion_line = src_motion_lines[j].strip().split()
        ref_data.append([src_motion_line[k] for k in indices_to_replace])
    half_length = len(ref_data) // 2
    ref_data = ref_data[:half_length] + ref_data[:half_length][::-1] + ref_data + ref_data[::-1] + ref_data[:half_length] + ref_data[:half_length][::-1]
    ref_data = [item for item in ref_data for _ in range(2)]

    # 读取多个BVH文件
    for file_path in bvh_files:
        _, frame_count, frame_time, motion_lines = read_bvh(file_path)
        
        idx = 0      
        for i, line in enumerate(motion_lines):
            if i > 0:
                values = line.strip().split(' ')
                for j in range(len(indices_to_replace)):
                    values[indices_to_replace[j]] = ref_data[idx][j]

                motion_lines[i] = ' '.join(values) + '\n'
                
                if idx < len(ref_data) - 1:
                    idx += 1
                else:
                    idx = 0
        
        # 输出路径
        basename = os.path.basename(file_path)
        output_file = os.path.join(out_dir, basename)
        
        # 写入拼接后的BVH文件
        write_bvh(output_file, hierarchy, frame_count, frame_time, motion_lines)
        
if __name__ == "__main__":
    try:
        src_folder = 'C:/Users/kimiz/Desktop/LBVR专项/test/blend_test/raw'
        out_dir = 'C:/Users/kimiz/Desktop/LBVR专项/test/blend_test/processed'
        src_bvh = 'C:/Users/kimiz/Desktop/LBVR专项/test/blend_test/Zhuli_Sit_idle.bvh'
        bvh_files = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if f.endswith('.bvh')]
        src_frame_range = [1, 76]
        leg_indices = list(range(0, 6)) + list(range(137, 162))
        blend(bvh_files, src_bvh, src_frame_range, leg_indices, out_dir)
    except Exception as e:
        print(e)