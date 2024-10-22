'''
XSens 动捕数据融合脚本
written by Kimi Zhong
Oct.21th, 2024
'''

import os
import ast
from tkinter import IntVar, Tk, StringVar, Entry, Button, Label, Toplevel, messagebox
from tkinter.filedialog import askdirectory, askopenfilename
from bvh_utils.blend_bvh import blend
from common.common import return_to_main_menu

# 全局变量
interface = None
src_bvh_var = None
src_folder_var = None
out_folder_var = None
start_frame_var = None
end_frame_var = None
start_index_var = None
end_index_var = None
interval_display_var  = None
interval_list = []

def OpenSrcFolder():
    selected_folder = askdirectory()
    if selected_folder:
        src_folder_var.set(selected_folder)
    else:
        messagebox.showinfo("信息", "未选择任何文件夹。")

def OpenOutFolder():
    selected_folder = askdirectory()
    if selected_folder:
        out_folder_var.set(selected_folder)
    else:
        messagebox.showinfo("信息", "未选择任何文件夹。")

def OpenSrcBVH():
    selected_file = askopenfilename(filetypes=[("BVH files", "*.bvh")])
    if selected_file:
        src_bvh_var.set(selected_file)
    else:
        messagebox.showinfo("信息", "未选择任何BVH文件。")

def add_index_range():
    start_index = start_index_var.get()
    end_index = end_index_var.get()
    # validation
    if start_index < end_index:
        try:
            # 获取当前的 interval_str
            interval_str = interval_display_var.get()
            interval_list = decode_intervals(interval_str)

            # 添加新的索引范围
            interval_list.append([start_index, end_index])

            # 更新 interval_str
            interval_str = str(interval_list)
            interval_display_var.set(interval_str)

            # 自动合并和排序
            sort_and_merge_intervals()

        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
    else:
        messagebox.showerror("输入错误", "请确保输入的索引范围正确")

def sort_and_merge_intervals():
    try:
        interval_str = interval_display_var.get()
        interval_list = decode_intervals(interval_str)
        
        # sort
        interval_list.sort(key=lambda x: x[0])
        
        # merge
        merged = [interval_list[0]]
        for current in interval_list[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                last[1] = max(last[1], current[1])
            else:
                merged.append(current)

        # 更新 interval_str 和 interval_display_var
        interval_str = str(merged)
        interval_display_var.set(interval_str)
    
    except ValueError as e:
        messagebox.showerror("输入错误", str(e))

def decode_intervals(interval_str):
    try:
        # 使用 ast.literal_eval 安全地解析字符串
        intervals = ast.literal_eval(interval_str)

        # 验证解析结果是否为 List[List[int]]
        if not isinstance(intervals, list) or not all(isinstance(i, list) and len(i) == 2 and all(isinstance(x, int) for x in i) for i in intervals):
            raise ValueError("输入格式错误，应为 List[List[int]] 的形式")

        return intervals
    
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"无效输入: {e}")

def DoBlend():
    try:
        src_bvh = src_bvh_var.get()
        if not src_bvh:
            messagebox.showerror("未选择源BVH文件")
            return

        folder = src_folder_var.get()
        if not folder:
            messagebox.showerror("未选择源文件夹")
            return

        out_folder = out_folder_var.get()
        if not out_folder:
            messagebox.showerror("未选择输出文件夹")
            return

        # 获取帧范围
        start_frame = start_frame_var.get()
        end_frame = end_frame_var.get()
        if start_frame < 1 or end_frame < start_frame:
            messagebox.showerror("请输入合法的帧范围")
            return
        src_frame_range = [start_frame, end_frame]

        # 获取需要替换的关节索引范围
        indices_to_replace = []
        interval_str = interval_display_var.get()
        interval_list = decode_intervals(interval_str)
        sort_and_merge_intervals()  # 确保索引已排序和合并
        for interval in interval_list:
            indices_to_replace.extend(range(interval[0], interval[1]))

        # 拼接输出文件路径
        bvh_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.bvh')]
        if not bvh_files:
            messagebox.showerror("错误", "源文件夹中没有找到BVH文件。")
            return

        # 执行融合
        blend(bvh_files, src_bvh, src_frame_range, indices_to_replace, out_folder)
        messagebox.showinfo("完成", "BVH数据融合已完成!")

    except Exception as e:
        messagebox.showerror("错误", str(e))


def open_blend_interface(parent_window=None):
    global interface, src_bvh_var, src_folder_var, out_folder_var, start_frame_var, end_frame_var
    global start_index_var, end_index_var, interval_display_var
    
    if parent_window is None:
        interface = Tk()
    else:
        interface = Toplevel(parent_window)
    interface.geometry("550x350")
    interface.title("BVH Data Blender")
    interface.configure(bg='#F5F5F5')

    # 选择源BVH文件
    src_bvh_var = StringVar()
    Label(interface, text="源BVH文件", bg='#F5F5F5').grid(row=0, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=src_bvh_var, state='readonly', width=40).grid(row=0, column=1, columnspan=4, padx=10, pady=5, sticky="w")
    Button(interface, text="选择BVH文件", command=OpenSrcBVH).grid(row=0, column=5, padx=10, pady=5, sticky="w")

    # 源文件夹选择
    src_folder_var = StringVar()
    Label(interface, text="源BVH文件夹", bg='#F5F5F5').grid(row=1, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=src_folder_var, state='readonly', width=40).grid(row=1, column=1, columnspan=4, padx=10, pady=5, sticky="w")
    Button(interface, text="选择文件夹", command=OpenSrcFolder).grid(row=1, column=5, padx=10, pady=5, sticky="w")

    # 输出文件夹选择
    out_folder_var = StringVar()
    Label(interface, text="输出文件夹", bg='#F5F5F5').grid(row=2, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=out_folder_var, state='readonly', width=40).grid(row=2, column=1, columnspan=4, padx=10, pady=5, sticky="w")
    Button(interface, text="选择文件夹", command=OpenOutFolder).grid(row=2, column=5, padx=10, pady=5, sticky="w")

    # 帧范围输入
    Label(interface, text="帧范围", bg='#F5F5F5').grid(row=3, column=0, padx=10, pady=5, sticky="w")
    
    start_frame_var = IntVar()
    Label(interface, text="开始帧").grid(row=3, column=1, padx=5, pady=5, sticky="w")
    Entry(interface, textvariable=start_frame_var, width=10).grid(row=3, column=2, padx=5, pady=5, sticky="w")

    end_frame_var = IntVar()
    Label(interface, text="结束帧").grid(row=3, column=3, padx=5, pady=5, sticky="w")
    Entry(interface, textvariable=end_frame_var, width=10).grid(row=3, column=4, padx=5, pady=5, sticky="w")

    # 替换关节索引输入部分
    Label(interface, text="关节索引范围", bg='#F5F5F5').grid(row=4, column=0, padx=10, pady=5, sticky="w")
    
    start_index_var = IntVar()
    Label(interface, text="起始索引").grid(row=4, column=1, padx=5, pady=5, sticky="w")
    Entry(interface, textvariable=start_index_var, width=10).grid(row=4, column=2, padx=5, pady=5, sticky="w")

    end_index_var = IntVar()
    Label(interface, text="结束索引").grid(row=4, column=3, padx=5, pady=5, sticky="w")
    Entry(interface, textvariable=end_index_var, width=10).grid(row=4, column=4, padx=5, pady=5, sticky="w")

    # 添加按钮以保存关节索引范围
    Button(interface, text="添加索引范围", command=add_index_range).grid(row=4, column=5, padx=5, pady=5, sticky="w")

    # 显示所有添加的索引范围
    interval_display_var = StringVar(value="[]")
    Entry(interface, textvariable=interval_display_var, width=40, fg="blue").grid(row=5, column=1, columnspan=4, padx=10, pady=5, sticky="w")
    Button(interface, text="整理索引范围", command=sort_and_merge_intervals).grid(row=5, column=5, padx=5, pady=5, sticky="w")

    # 处理按钮
    Button(interface, text="开始融合", bd=5, font=('黑体', 14, 'bold'), height=1, command=DoBlend).grid(row=6, column=0, columnspan=6, padx=10, pady=5, sticky="we")
    
    if parent_window:
        # 返回按钮
        Button(interface, text="返回", bd=5, font=('黑体', 14, 'bold'), height=1, command=lambda: return_to_main_menu(interface, parent_window)).grid(row=7, column=0, columnspan=6, padx=10, pady=5, sticky="we")
        interface.protocol("WM_DELETE_WINDOW", lambda: (interface.destroy(), parent_window.deiconify()))
    else: 
        interface.mainloop()


if __name__ == "__main__":
    try:
        open_blend_interface()
    except Exception as e:
        print(e)
