import os
import sys
import tkinter as tk
from tkinter import filedialog
import pyperclip
from PIL import Image, ImageDraw, ImageFont



try:
    # 设置 DPI 意识（仅适用于 Windows）
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass  # 忽略非 Windows 系统或设置失败的情况

win = tk.Tk()
win.geometry("1200x742+500+250")  # size
win.tk.call("tk", "scaling", 2)
win.resizable(0, 0)
win.attributes("-topmost", 0)  # 打开时置顶
win.title("Watermake")
win.config(bg="#FFF2E2")
# 图标路径
path_icon = os.path.dirname(os.path.realpath(sys.argv[0]))  # 与dist文件夹
path_icon = os.path.join(path_icon, "icon", "pictures_97526.ico")
win.iconbitmap(path_icon)


# Function 合集
# Function 样板
def picture():  # 打开两种图片 对比
    path_picture_1 = os.path.dirname(os.path.realpath(sys.argv[0]))  # 与dist文件夹
    path_picture_1 = os.path.join(path_picture_1, "icon", "yangben.jpg")

    path_picture_2 = os.path.dirname(os.path.realpath(sys.argv[0]))  # 与dist文件夹
    path_picture_2 = os.path.join(path_picture_2, "icon", "watermaked.jpg")

    # 打开图片
    path = [path_picture_1, path_picture_2]
    for path in path:
        os.startfile(path)


# 文件选取
def browse_file():
    file_path = filedialog.askopenfilename(
        title="选择文件",  # 对话框标题
        filetypes=[("所有文件", "*.*"), ("图片文件", "*.png;*.jpg")],  # 文件类型过滤
    )
    if file_path:
        en_xuanqu_var.set(file_path)  # 更新路径到 Entry 中


# 另存为文件
def save_file():
    original_file_path = en_xuanqu_var.get()
    if not original_file_path:
        return

    # 获取文件名和扩展名
    file_name = os.path.basename(en_xuanqu_var.get())  # 获取文件名（包含扩展名）
    file_name_without_extension = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]

    # 弹出文件保存对话框，用户选择保存路径和文件名
    file_path = filedialog.asksaveasfilename(
        title="另存为文件",  # 对话框标题
        filetypes=[
            ("图片文件", "*.png;*.jpg;*.jpeg"),
            ("所有文件", "*.*"),
        ],  # 文件类型过滤
        initialfile=f"{file_name_without_extension}_ian{extension}",  # 默认文件名
    )
    if file_path:
        en_lingcunwei_var.set(file_path)


# 复制
def copy():
    lujing = en_xuanqu_var.get()
    pyperclip.copy(lujing)


# 复制
def copy_2():
    lujing = en_lingcunwei_var.get()
    pyperclip.copy(lujing)


def add_watermark():

    try:
        # 检查输入文件路径是否合法
        original_file_path = en_xuanqu_var.get()
        if not original_file_path:
            return

        # 检查输出文件路径是否合法
        output_file_path = en_lingcunwei_var.get()
        if not output_file_path:
            return

        # 打开原始图片
        original_image = Image.open(en_xuanqu_var.get())
        image_width, image_height = original_image.size

        # 计算水印区域高度
        image_added_height = int(image_height * 0.0618)
        canvas_height = image_height + image_added_height

        # 创建画布
        canvas = Image.new("RGB", (image_width, canvas_height), (255, 255, 255))
        canvas.paste(original_image, (0, 0))
        draw = ImageDraw.Draw(canvas)

        # 字体大小计算
        k = max(image_width / 1900, image_added_height / 74.16)

        # 绘制水印
        font_large = ImageFont.truetype("msyh.ttc", int(30 * k))
        font_small = ImageFont.truetype("LeelawUI.ttf", int(25 * k))

        # 绘制文字
        text_parts_1 = [
            {"text": "Redmi", "font": font_large, "fill": (0, 0, 0)},
            {"text": "14C", "font": font_large, "fill": (255, 0, 0)},
        ]

        x = int(image_width * 0.01)
        for part in text_parts_1:
            text_bbox = draw.textbbox((0, 0), part["text"], font=part["font"])
            text_width = text_bbox[2] - text_bbox[0]
            y = (
                image_height
                + (image_added_height - (text_bbox[3] - text_bbox[1])) * 0.4
            )
            draw.text((x, y), part["text"], font=part["font"], fill=part["fill"])
            x += text_width + int(image_width * 0.00618)

        text_parts_2 = "25mm | f/2.2 | 1/711s | ISO800"
        text_bbox = draw.textbbox((0, 0), text_parts_2, font=font_small)
        text_width = text_bbox[2] - text_bbox[0]
        x = image_width * 0.99 - text_width
        y = image_height + (image_added_height - (text_bbox[3] - text_bbox[1])) * 0.4
        draw.text((x, y), text_parts_2, font=font_small, fill=(0, 0, 0))

        # 保存图片
        canvas.save(en_lingcunwei_var.get())

        # 创建一个标签来显示文字
        lb_tishi = tk.Label(win)
        lb_tishi.config(
            text="SUCCESS!",
            font=("Forte", 40, "bold"),
            fg="red",
            bg="#FFF2E2",
            relief="flat",
        )
        lb_tishi.place(x=560, y=300, anchor="center")

        # 2.5秒后销毁标签
        win.after(2500, lambda: lb_tishi.destroy())

    except:
        # 创建一个标签来显示文字
        lb_tishi = tk.Label(win)
        lb_tishi.config(
            text="RUN WRONGLY",
            font=("Forte", 40, "bold"),
            fg="#2b2e4a",
            bg="#FFF2E2",
            relief="flat",
        )
        lb_tishi.place(x=560, y=300, anchor="center")

        # 2.5秒后销毁标签
        win.after(2500, lambda: lb_tishi.destroy())

#说明
def instruction ():
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    path = os.path.join(path,"explanation","instruction.txt")
    os.startfile(path)
    
    


# label 产品介绍
lb_introduction = tk.Label(win)
lb_introduction.config(
    text="这是一款致力于给照片添加红米14C水印的软件!",
    bg="#FFF2E2",
    fg="#3e4149",
    font=("Snap ITC", 20),
)
lb_introduction.pack()

# 样板
btn_example = tk.Button(win)
btn_example.config(
    bg="#ff9999",
    fg="black",
    text="样板",
    font=("黑体", 12),
    width=5,
    relief="flat",
    command=picture,
)
btn_example.place(anchor="center", x=70, y=680)


# 选取文件界面
lb_xuanqu = tk.Label()
lb_xuanqu.config(
    bg="#FFF2E2", fg="#aa96da", text="选取图片", font=("方正粗黑宋简体", 17)
)
lb_xuanqu.place(anchor="center", x=260, y=150)

en_xuanqu_var = tk.StringVar()  # 创建一个 StringVar 对象
en_xuanqu = tk.Entry(win)
en_xuanqu.config(
    bg="white",
    fg="black",
    width=26,
    highlightbackground="skyblue",  # 无焦点时的边缘颜色
    highlightcolor="#ffde7d",  # 有焦点时的边缘颜色
    highlightthickness=2,
    font=("微软雅黑", 13),
    textvariable=en_xuanqu_var,  # 将 Entry的内容与tringVar绑定
)
en_xuanqu.place(anchor="center", x=300, y=200)


lb_lujing1 = tk.Label(win)
lb_lujing1.config(text="路径:", fg="black", bg="#FFF2E2", font=("微软雅黑", 14))
lb_lujing1.place(anchor="center", x=60, y=200)

btn_xuanqu = tk.Button(win)
btn_xuanqu.config(
    text="选取",
    relief="flat",
    fg="#323232",
    bg="#a5dee5",
    width=5,
    font=("方正粗黑宋简体", 15),
    command=browse_file,
)
btn_xuanqu.place(anchor="center", x=180, y=300)

btn_fuzhi = tk.Button(win)
btn_fuzhi.config(
    text="复制",
    relief="flat",
    fg="#323232",
    bg="#a5dee5",
    width=5,
    font=("方正粗黑宋简体", 15),
    command=copy,
)
btn_fuzhi.place(anchor="center", x=180, y=400)

# 另存为文件界面


btn_lingcunwei = tk.Button(win)
btn_lingcunwei.config(
    text="另存为",
    relief="flat",
    fg="#323232",
    bg="#a5dee5",
    width=5,
    font=("方正粗黑宋简体", 15),
    command=save_file,
)
btn_lingcunwei.place(anchor="center", x=960, y=300)

btn_fuzhi_2 = tk.Button(win)
btn_fuzhi_2.config(
    text="复制",
    relief="flat",
    fg="#323232",
    bg="#a5dee5",
    width=5,
    font=("方正粗黑宋简体", 15),
    command=copy_2,
)
btn_fuzhi_2.place(anchor="center", x=960, y=400)


lb_lingcunwei = tk.Label(win)
lb_lingcunwei.config(
    bg="#FFF2E2", fg="#aa96da", text="另存为图片", font=("方正粗黑宋简体", 17)
)
lb_lingcunwei.place(anchor="center", x=840, y=150)

en_lingcunwei_var = tk.StringVar()
en_lingcunwei = tk.Entry(win)
en_lingcunwei.config(
    bg="white",
    fg="black",
    width=26,
    highlightbackground="skyblue",  # 无焦点时的边缘颜色
    highlightcolor="#ffde7d",  # 有焦点时的边缘颜色
    highlightthickness=2,
    font=("微软雅黑", 13),
    textvariable=en_lingcunwei_var,
)
en_lingcunwei.place(anchor="center", x=880, y=200)


lb_lujing2 = tk.Label(win)
lb_lujing2.config(text="路径:", fg="black", bg="#FFF2E2", font=("微软雅黑", 14))
lb_lujing2.place(anchor="center", x=640, y=200)


# 加水印
btn_tianjia = tk.Button(win)
btn_tianjia.config(
    text="运行",
    fg="#323232",
    bg="#a5dee5",
    font=("方正粗黑宋简体", 17),
    relief="flat",
    command=add_watermark,
)
btn_tianjia.place(anchor="center", x=560, y=560)

# 加说明
btn_instruction = tk.Button(win)
btn_instruction.config(
    bg="#ff9999",
    fg="black",
    text="说明",
    font=("黑体", 12),
    width=5,
    relief="flat",
    command=instruction,
)
btn_instruction.place(anchor="center", x=170, y=680)


win.mainloop()
