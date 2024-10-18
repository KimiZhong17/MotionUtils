def read_bvh(bvh_file):
    with open(bvh_file, 'r') as f:
        lines = f.readlines()

    motion_start_idx = 0
    hierarchy_lines = []
    
    # 找到Hierarchy部分并存储它
    for i, line in enumerate(lines):
        if line.strip().startswith("MOTION"):
            motion_start_idx = i
            break
        hierarchy_lines.append(line)

    # 读取Frame Time，并做scaling处理
    frame_time_line = lines[motion_start_idx + 2]
    frame_time = float(frame_time_line.strip().split(":")[-1])

    # 读取Motion部分的数据
    motion_lines = lines[motion_start_idx + 3:]
    
    # Frames
    frame_count = len(motion_lines)
    
    return hierarchy_lines, frame_count, frame_time, motion_lines


def write_bvh(output_file, hierarchy, frame_count, frame_time, motion_lines):
    # 写入拼接后的BVH文件
    with open(output_file, 'w') as out_f:
        # 写入Hierarchy部分
        out_f.writelines(hierarchy)

        # 写入MOTION部分
        out_f.write("MOTION\n")
        out_f.write(f"Frames: {frame_count}\n")
        out_f.write(f"Frame Time: {frame_time:.6f}\n")

        # 写入拼接后的Motion数据，确保每帧数据分行存储
        out_f.writelines(motion_lines)