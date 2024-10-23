from tkinter import Tk, Button, Label, messagebox
from bvh_utils.blend_bvh_pac import open_bvh_blend_interface
from bvh_utils.combine_bvh_pac import open_bvh_merger
from bvh_utils.reset_y_bvh_pac import open_bvh_reset_interface

global main_menu
main_menu = None

# 定义函数，用于打开不同的界面
def open_merge_bvh_interface():
    main_menu.withdraw()  # 隐藏选择操作窗口
    open_bvh_merger(main_menu)

def open_blend_bvh_interface():
    main_menu.withdraw()
    open_bvh_blend_interface(main_menu)
    
def open_reset_bvh_interface():
    main_menu.withdraw()
    open_bvh_reset_interface(main_menu)

def open_other_function():
    main_menu.withdraw()  # 隐藏选择操作窗口
    messagebox.showinfo("其他功能", "此功能还未实现！")
    main_menu.deiconify()  # 重新显示选择窗口
    
# 返回主菜单
def return_to_main_menu(current_window, parent_window):
    current_window.destroy()  # 关闭当前窗口
    parent_window.deiconify()  # 重新显示主菜单窗口

# 操作选择窗口
if __name__ == '__main__':
    main_menu = Tk()
    main_menu.title("请选择操作")
    main_menu.geometry("300x250")
    Label(main_menu, text="选择要进行的操作", padx=10, pady=10).pack()

    Button(main_menu, text="合并BVH文件", width=25, command=open_merge_bvh_interface).pack(pady=5)
    Button(main_menu, text="融合BVH文件", width=25, command=open_blend_bvh_interface).pack(pady=5)
    Button(main_menu, text="重置root高度", width=25, command=open_reset_bvh_interface).pack(pady=5)
    Button(main_menu, text="其他功能", width=25, command=open_other_function).pack(pady=5)

    main_menu.mainloop()