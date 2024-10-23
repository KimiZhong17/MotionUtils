import os
from tkinter import Tk, StringVar, Entry, Button, Label, Checkbutton, IntVar, Toplevel, messagebox
from tkinter.filedialog import askdirectory
from bvh_utils.combine_bvh import merge_bvh_files
from bvh_utils.reset_y_bvh import reset_y_to
from common.common import return_to_main_menu

# global variables
src_folder_var = None
out_folder_var = None
target_y_var = None

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
        
def DoResetY():
    try:
        # 获取目标Y值
        target_y = float(target_y_var.get())
        
        # 获取源文件夹路径
        src_folder = src_folder_var.get()
        if not src_folder:
            messagebox.showerror("错误", "未选择源文件夹。")
            return
        
        # 获取输出文件夹路径
        out_folder = out_folder_var.get()
        if not out_folder:
            messagebox.showerror("错误", "未选择输出文件夹。")
            return
        
        # 列出所有BVH文件
        bvh_files = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if f.endswith('.bvh')]
        if not bvh_files:
            messagebox.showinfo("信息", "在源文件夹中没有找到任何BVH文件。")
            return
        
        # 调用重置函数
        reset_y_to(bvh_files, target_y, out_folder)
        
        # 处理完成，显示消息
        messagebox.showinfo("完成", "Y轴重置已完成!")
    
    except ValueError:
        messagebox.showerror("错误", "请输入有效的目标Y值。")
    except Exception as e:
        messagebox.showerror("错误", str(e))
        

def open_bvh_reset_interface(parent_window=None):
    global interface, target_y_var, src_folder_var, out_folder_var
    
    if parent_window is None:
        interface = Tk()
    else:
        interface = Toplevel(parent_window)
    
    interface.geometry("500x250")
    interface.title("BVH Y轴重置")
    interface.configure(bg='#F5F5F5')

    # 目标Y值输入
    target_y_var = StringVar()
    Label(interface, text="目标Y值", bg='#F5F5F5').grid(row=0, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=target_y_var).grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # 源文件夹选择
    src_folder_var = StringVar()
    Label(interface, text="源BVH路径").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=src_folder_var, state='readonly', width=30).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    Button(interface, text="选择文件夹", command=OpenSrcFolder).grid(row=1, column=2, padx=10, pady=5, sticky="w")

    # 输出文件夹选择
    out_folder_var = StringVar()
    Label(interface, text="输出文件夹").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    Entry(interface, textvariable=out_folder_var, state='readonly', width=30).grid(row=2, column=1, padx=10, pady=5, sticky="w")
    Button(interface, text="选择文件夹", command=OpenOutFolder).grid(row=2, column=2, padx=10, pady=5, sticky="w")

    # 处理按钮
    Button(interface, text="开始重置Y轴", bd=5, font=('黑体', 14, 'bold'), command=DoResetY).grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="we")
    
    if parent_window:
        Button(interface, text="返回", bd=5, font=('黑体', 14, 'bold'), command=lambda: return_to_main_menu(interface, parent_window)).grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="we")
        interface.protocol("WM_DELETE_WINDOW", lambda: (interface.destroy(), parent_window.deiconify()))
    else:
        interface.mainloop()