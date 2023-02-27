import cv2
import qrcode  # 二维码生成包
from pyzbar.pyzbar import decode  # 二维码解码包
import webbrowser
import validators
import tkinter
import os
from MyQR import myqr
from PIL import Image
from tkinter import filedialog


class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title('周楚骎的编解码器')
        self.iconphoto(True, tkinter.PhotoImage(file='Qin.png'))
        l1 = tkinter.Label(self, text="周楚骎的二维码编解码器", font=("Microsoft Sans Serif", 24))
        # l1.place(x=50, y=50)
        l1.pack()
        button1 = tkinter.Button(self, text="编码器", command=CoderGUI, height=10, width=20, font=20, bd=5)
        button1.pack(side=tkinter.LEFT)
        button2 = tkinter.Button(self, text="解码器", command=DecoderGUI, height=10, width=20, font=20, bd=5)
        button2.pack(side=tkinter.RIGHT)
        self.mainloop()


class CoderGUI(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title('周楚骎的编码器')
        self.path = tkinter.StringVar()
        l1 = tkinter.Label(self, text="二维码内容")
        l1.grid(row=0, column=0)
        self.e1 = tkinter.Entry(self, bd=5, width=30, justify="center", cursor="circle")
        self.e1.grid(row=0, column=1)
        l3 = tkinter.Label(self, text="二维码背景文件(可选)")
        l3.grid(row=1, column=0)
        self.e3 = tkinter.Entry(self, bd=5, width=30, textvariable=self.path, justify="center", cursor="circle")
        self.e3.grid(row=1, column=1)
        b2 = tkinter.Button(self, bd=5, text='路径选择', command=self.selectPath)
        b2.grid(row=1, column=2)
        l2 = tkinter.Label(self, text="二维码储存文件名")
        l2.grid(row=2, column=0)
        self.e2 = tkinter.Entry(self, bd=5, width=30, justify="center", cursor="circle")
        self.e2.grid(row=2, column=1)
        b1 = tkinter.Button(self, bd=5, text='生成二维码', width=20, height=5, command=self.create_qpcode)
        b1.grid(row=3, column=1)

    def create_qpcode(self):
        background = self.e3.get()
        loc = self.e2.get()
        if loc == '':
            return
        if os.path.exists(background):
            b2 = tkinter.Button(self, text='将图片作为背景', width=20, height=5, command=self.create_background)
            b2.grid(row=4, column=0)
            b2 = tkinter.Button(self, text='将图片放在中心', width=20, height=5, command=self.create_center)
            b2.grid(row=4, column=2)
        else:
            self.qpcode_create()

    def qpcode_create(self):
        msg = self.e1.get()
        loc = self.e2.get()
        qrcode_create(msg, loc)

    def create_background(self):
        msg = self.e1.get()
        background = self.e3.get()
        loc = self.e2.get()
        qrcode_create_background(msg, background, loc)

    def create_center(self):
        msg = self.e1.get()
        background = self.e3.get()
        loc = self.e2.get()
        qrcode_create_center(msg, background, loc)

    def selectPath(self):
        # 选择文件path_接收文件地址
        path_ = filedialog.askopenfilename()

        # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
        # \\转义后为\，所以\\\\转义后为\\
        path_ = path_.replace("/", "\\\\")
        # path设置path_的值
        self.path.set(path_)


class DecoderGUI(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("408x500")
        self.title('周楚骎的解码器')
        self.path = tkinter.StringVar()
        # 按下后打开电脑摄像头并开始寻找二维码进行解码
        b1 = tkinter.Button(self, text='电脑摄像头拍摄二维码', width=30, height=5, command=self.camera_decoder)
        b1.grid(row=0, column=1)
        l1 = tkinter.Label(self, text="待解码文件名")
        l1.grid(row=1, column=0)
        self.e1 = tkinter.Entry(self, bd=5, textvariable=self.path, justify="center", cursor="circle")
        self.e1.grid(row=1, column=1)
        b2 = tkinter.Button(self, bd=5, text='路径选择', command=self.selectPath)
        b2.grid(row=1, column=2)
        # 按下后寻找该文件开始解码
        b2 = tkinter.Button(self, text='开始解码', command=self.select_decoder)
        b2.grid(row=2, column=1)
        l3 = tkinter.Label(self, text="解码结果")
        l3.grid(row=3, column=1)
        self.t1 = tkinter.Text(self, bd=5, width=20, height=10)
        self.t1.grid(row=4, column=1)
        b3 = tkinter.Button(self, text="清空解码输出结果", command=self.clear_box)
        b3.grid(row=3, column=2)

    def camera_decoder(self):
        msg = cameraDecoder()
        self.t1.insert('insert', msg)

    def select_decoder(self):
        msg = self.e1.get()
        res = qrcode_decode_local(msg)
        self.t1.insert('insert', res)

    def clear_box(self):
        self.t1.delete("1.0", "end")

    def selectPath(self):
        # 选择文件path_接收文件地址
        path_ = filedialog.askopenfilename()

        # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
        # 注意：\\转义后为\，所以\\\\转义后为\\
        path_ = path_.replace("/", "\\\\")
        # path设置path_的值
        self.path.set(path_)


def qrcode_create(data_str: str, save_name: str):
    img = qrcode.make(data_str)
    img.save(save_name)
    img = cv2.imread(save_name, 1)
    cv2.imshow("IMG", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def qrcode_create_center(data_str: str, back_str: str, save_name: str):
    img = qrcode.make(data_str)
    img = img.convert("CMYK")  # RGBA
    # 添加logo
    icon = Image.open(back_str).convert("RGBA")
    # 获取图片的宽高
    img_w, img_h = img.size
    factor = 6
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    # 重新设置logo的尺寸
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    img.paste(icon, (w, h), icon)
    # 显示图片
    img.save(save_name)
    img = cv2.imread(save_name)
    cv2.imshow("IMG", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def qrcode_create_background(data_str, back_str, save_name):
    flag = 0
    save_name = save_name.split('.')
    if save_name[-1] == 'jpg':
        flag = 1
        save_name[-1] = 'png'
        save_name = str.join(".", save_name)
    myqr.run(words=data_str, picture=back_str, colorized=True, save_name=save_name)
    img = cv2.imread(save_name)
    cv2.imshow("IMG", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    img = Image.open(save_name)
    save_name = save_name.split(".")
    if flag == 1:
        save_name[-1] = 'jpg'
        save_name = str.join(".", save_name)
        r, g, b, a = img.split()
        img = Image.merge("RGB", (r, g, b))
        img.save(save_name)
        save_name = save_name.split('.')
        save_name[-1] = 'png'
        save_name = str.join(".", save_name)
        os.remove(save_name)


def qrcode_decode_camera(src_img):
    data = False
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    barcode_objects = decode(gray_img)
    if len(barcode_objects) > 0:
        for obj in barcode_objects:
            data = obj.data
            data = data.decode('utf-8')
            # print(data)
            if validators.url(data):
                webbrowser.open(data, new=0, autoraise=True)
    return data


def cameraDecoder():
    capture = cv2.VideoCapture(0)  # 0是代表摄像头编号，只有一个的话默认为0
    data = ''
    while True:
        # 调用摄像机
        ref, capframe = capture.read()
        if ref is True:
            # 二维码识别
            data = qrcode_decode_camera(capframe)
            cv2.imshow('frame', capframe)
            if cv2.waitKey(15) == ord('q') or data:
                # 当输入 q 或截取到有用信息时关闭窗口
                break
    capture.release()
    cv2.destroyAllWindows()
    return data


def qrcode_decode_local(src_img):
    data = '解码结果'
    if not os.path.exists(src_img):
        data = '不存在该文件'
        # print(data)
        return data
    gray_img = cv2.imread(src_img, cv2.IMREAD_GRAYSCALE)
    barcode_objects = decode(gray_img)
    if len(barcode_objects) > 0:
        for obj in barcode_objects:
            data = obj.data
            data = data.decode('utf-8')
            # print(data)
            if validators.url(data):
                webbrowser.open(data, new=0, autoraise=True)
    return data


def main():
    GUI()


if __name__ == '__main__':
    main()
