'''
XSens 动捕数据后处理与合并脚本
written by Kimi Zhong
Sept.24th, 2024
'''

import os
from tkinter import Tk, StringVar, Entry, Button, Label, Checkbutton, IntVar, Toplevel, messagebox
from tkinter.filedialog import askdirectory
from bvh_utils.combine_bvh import merge_bvh_files
from common.common import return_to_main_menu

# global variables
task_name_var = None
src_folder_var = None
out_folder_var = None
fps_scale = None
normalize = None
interface = None

def OpenSrcFolder():
    selected_folder = askdirectory()
    if selected_folder:  # 检查是否选择了文件夹
        src_folder_var.set(selected_folder)
    else:
        messagebox.showinfo("信息", "未选择任何文件夹。")

def OpenOutFolder():
    selected_folder = askdirectory()
    if selected_folder:  # 检查是否选择了文件夹
        out_folder_var.set(selected_folder)
    else:
        messagebox.showinfo("信息", "未选择任何文件夹。")

def DoMerge():
    try:
        # 获取任务名称
        task_name = task_name_var.get().strip()
        if not task_name:
            messagebox.showerror("Please enter a task name.")
            return
        
        # 获取源文件夹路径
        folder = src_folder_var.get()
        if not folder:
            messagebox.showerror("No folder selected.")
            return

        # 获取输出文件夹路径
        out_folder = out_folder_var.get()
        if not out_folder:
            messagebox.showerror("No output folder selected.")
            return
        
        # 拼接输出文件路径
        out_prefix = os.path.join(out_folder, 'merged_file_' + task_name)
        csv_prefix = os.path.join(out_folder, 'output_data_' + task_name)
        
        # 确保帧率缩小倍数是合法的数字
        inv_fps_scale = int(fps_scale.get()) if fps_scale.get().isdigit() else 1
        
        # 获取是否归一化选项
        normalization = bool(normalize.get())
        
        # 创建一个新窗口用于显示处理状态
        process_window = Toplevel(interface)
        process_window.title("处理状态")
        Label(process_window, text="正在合并文件，请稍候...", padx=20, pady=20).pack()
        
        # 列出BVH文件
        bvh_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.bvh')]
        if not bvh_files:
            print("No BVH files found in the folder.")
            return

        # 调用函数进行合并
        merge_bvh_files(bvh_files, out_prefix, csv_prefix, inv_fps_scale, normalization)
        
        # 处理完成，关闭窗口并显示消息
        process_window.destroy()
        messagebox.showinfo("完成", "合并已完成!")
    
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 打开BVH合并界面
def open_bvh_merger(parent_window=None):
    global interface, task_name_var, src_folder_var, out_folder_var, fps_scale, normalize
    
    if parent_window == None:
        interface = Tk()
    else:
        interface = Toplevel(parent_window)
    interface.geometry("500x300")
    interface.title("BVH Merger")
    interface.configure(bg='#F5F5F5')

    # 任务名称输入
    task_name_var = StringVar()
    Label(interface, text="任务名称", bg='#F5F5F5').grid(row=0, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=task_name_var, width=40).grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # 源文件夹选择
    src_folder_var = StringVar()
    Label(interface, text="源BVH路径").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=src_folder_var, state='readonly', width=40).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    Button(interface, text="选择文件夹", command=OpenSrcFolder).grid(row=1, column=2, padx=10, pady=5, sticky="w")

    # 输出文件夹选择
    out_folder_var = StringVar()
    Label(interface, text="输出文件夹").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=out_folder_var, state='readonly', width=40).grid(row=2, column=1, padx=10, pady=5, sticky="w")
    Button(interface, text="选择文件夹", command=OpenOutFolder).grid(row=2, column=2, padx=10, pady=5, sticky="w")

    # 帧率缩小倍数
    fps_scale = StringVar(value="2")
    Label(interface, text="帧率缩小倍率").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=fps_scale).grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # 是否归一化到(0,0)
    normalize = IntVar(value=0)
    Label(interface, text="是否归一化").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    Checkbutton(interface, text="归一化", variable=normalize).grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # 处理按钮
    Button(interface, text="开始合并", bd=5, font=('黑体', 14, 'bold'), height=1, command=DoMerge).grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="we")
    
    if parent_window:
        # 返回按钮
        Button(interface, text="返回", bd=5, font=('黑体', 14, 'bold'), height=1, command=lambda: return_to_main_menu(interface, parent_window)).grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="we")
        interface.protocol("WM_DELETE_WINDOW", lambda: (interface.destroy(), parent_window.deiconify()))
    else:
        interface.mainloop()