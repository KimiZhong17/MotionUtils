'''
XSens 动捕数据Y轴重置脚本
written by Kimi Zhong
Oct.21th, 2024
'''

import os
from common.bvh_manager import read_bvh, write_bvh

def reset_y_to(bvh_files, target_y, out_dir):
    '''
    A function to reset all y-axis values (height) of root joint to specific target_y
    @param bvh_files[List[Str]]:    a list of bvh files
    @param target_y[Float]:         target y value
    @param out_dir[Str]:            output folder
    '''
    # read all BVHs for manipulation
    for file_path in bvh_files:        
        hierarchy, frame_count, frame_time, motion_lines = read_bvh(file_path)
        
        dy = 0
        for i, line in enumerate(motion_lines):
            if i > 0:
                values = line.strip().split(' ')
                if i == 1:
                    dy = target_y - float(values[1])
                yt = float(values[1]) + dy
                values[1] = "{:.6f}".format(yt)

                motion_lines[i] = ' '.join(values) + '\n'
        
        # output
        basename = os.path.basename(file_path)
        out_name = '_reset_y'.join(os.path.splitext(basename))
        output_file = os.path.join(out_dir, out_name)
        
        write_bvh(output_file, hierarchy, frame_count, frame_time, motion_lines)
        
if __name__ == "__main__":
    try:
        src_folder = 'F:/一千零一夜动捕/朱莉3/片段/no_level'
        target_y = 5
        out_dir = 'F:/一千零一夜动捕/朱莉3/片段/reset_y'
        bvh_files = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if f.endswith('.bvh')]
        reset_y_to(bvh_files, target_y, out_dir)
    except Exception as e:
        print(e)