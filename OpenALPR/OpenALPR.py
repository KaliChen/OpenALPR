import cv2
#import rtsp
import requests
import base64
import numpy as np
import time
from PIL import Image, ImageTk, ImageDraw, ExifTags, ImageColor,ImageFont
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
import tkinter.messagebox as tkmsg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
from tkinter.colorchooser import *
import json
"""
fontofcv2_Item = {cv2.FONT_HERSHEY_SIMPLEX:'HERSHEY_SIMPLEX',cv2.FONT_HERSHEY_PLAIN:'HERSHEY_PLAIN', cv2.FONT_HERSHEY_DUPLEX:'HERSHEY_DUPLEX', 
                  cv2.FONT_HERSHEY_COMPLEX:'HERSHEY_COMPLEX',cv2.FONT_HERSHEY_TRIPLEX:'HERSHEY_TRIPLEX', cv2.FONT_HERSHEY_COMPLEX_SMALL:'HERSHEY_COMPLEX_SMALL',
                  cv2.FONT_HERSHEY_SCRIPT_SIMPLEX:'ERSHEY_SCRIPT_SIMPLEX', cv2.FONT_HERSHEY_SCRIPT_COMPLEX:'HERSHEY_SCRIPT_COMPLEX'} 
"""
fontlinetype_Item = {cv2.LINE_AA:'LINE_AA',cv2.LINE_8:'LINE_8'}
fontsize = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 22, 24, 28, 32, 36, 40, 44, 48, 52, 54, 60, 72)
linewidth = ( 1, 2, 3, 4, 5)
class OpenALPR():
    def __init__(self, master):
        self.parent = master
        self.imageFile = str()
        self.color_1 = (0,0,0)
        self.color_2 = (0,0,0)
        self.OpenALPRPanel = tk.LabelFrame(self.parent, text="OpenALPR",font=('Courier', 10))
        self.OpenALPRPanel.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)
        self.init_OpenALPR_tab()
        self.init_setting_tab()
        self.init_DisplaySceneMarkInfo_tab()


    def init_setting_tab(self):
        self.setting_tab = tk.Frame(self.OpenALPRPanel)
        self.setting_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #self.settingnotebook.add(self.ColorDraw_tab, text = "Color&Draw")

        self.MarkSettingPanel = tk.LabelFrame(self.setting_tab, text="Color and font Setting Panel",font=('Courier', 10))
        self.MarkSettingPanel.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        '''Color Panel'''
        ColorPanel = tk.Frame(self.MarkSettingPanel)
        ColorPanel.grid(row = 0, column = 0 ,sticky = tk.E+tk.W)        
        self.Color1Button = tk.Button(ColorPanel, text = "Color 1",font=('Courier', 10), command = self.askcolor1)
        self.Color1Button.grid(row = 0, column = 0, sticky = tk.E+tk.W)

        self.Color2Button = tk.Button(ColorPanel, text = "Color 2",font=('Courier', 10), command = self.askcolor2)
        self.Color2Button.grid(row = 1, column = 0, sticky = tk.E+tk.W)

        #self.Color3Button = tk.Button(ColorPanel, text = "Color 3",font=('Courier', 7),bg = "#0000ff", command = self.askcolor3)
        #self.Color3Button.grid(row = 2, column = 0, sticky = tk.E+tk.W)

        #self.Color4Button = tk.Button(ColorPanel, text = "Color 4",font=('Courier', 7),bg = "#ffffff", command = self.askcolor4)
        #self.Color4Button.grid(row = 3, column = 0, sticky = tk.E+tk.W)

        '''font line type setting'''
        fontcv2Panel = tk.Frame(self.MarkSettingPanel)
        fontcv2Panel.grid(row = 0, column = 1 ,sticky = tk.E+tk.W)
        """
        '''Font of cv2 label'''
        tk.Label(fontcv2Panel , text = "Font of cv2",font=('Courier', 7)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.fontcv2Var = tk.IntVar()
        self.fontcv2Var.set(1)
        for val, fontcv2type, in fontofcv2_Item.items(): 
            tk.Radiobutton(fontcv2Panel, text = fontcv2type, variable = self.fontcv2Var, value = val,font=('Courier', 6)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        '''Font Size'''
        tk.Label(self.MarkSettingPanel, text = "font size",font=('Courier', 7)).grid(row = 0, column = 2, sticky = tk.E+tk.W)
        #self.fontsizespinbox = tk.Spinbox(self.MarkSettingPanel, from_ = 1, to = 48, increment = 1, width = 3)
        self.fontsizespinbox = tk.Spinbox(self.MarkSettingPanel, values = fontsize, width = 3)
        self.fontsizespinbox.grid(row = 0, column = 3, sticky = tk.E+tk.W)
        """
        '''Line Size'''
        tk.Label(self.MarkSettingPanel, text = "Line size",font=('Courier', 10)).grid(row = 0, column = 4, sticky = tk.E+tk.W)        
        #self.linesizespinbox = tk.Spinbox(self.MarkSettingPanel, from_ = 1, to = 10, increment = 1, width = 3)
        self.linesizespinbox = tk.Spinbox(self.MarkSettingPanel, values = linewidth,  width = 3)
        self.linesizespinbox.grid(row = 0, column = 5, sticky = tk.E+tk.W)

        '''font line type setting'''
        fontlinetypecv2Panel = tk.Frame(self.MarkSettingPanel)
        fontlinetypecv2Panel.grid(row = 0, column = 6 ,sticky = tk.E+tk.W)
        '''line type label'''
        tk.Label(fontlinetypecv2Panel, text = "line type",font=('Courier', 10)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)       
        self.fontlinetypecv2Var = tk.IntVar()
        self.fontlinetypecv2Var.set(8)
        for val, linetype, in fontlinetype_Item.items(): 
            tk.Radiobutton(fontlinetypecv2Panel, text = linetype, variable = self.fontlinetypecv2Var, value = val,font=('Courier', 10)).pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def init_DisplaySceneMarkInfo_tab(self):
        self.DisplaySceneMarkInfo_Frame = tk.LabelFrame(self.OpenALPRPanel, text="Display OpenALPR Info", font=('Courier', 9))
        self.DisplaySceneMarkInfo_Frame .pack(side=tk.TOP, expand=tk.NO)
        DisplaySceneMarkInfoCLEAR =tk.Button(self.OpenALPRPanel, text = "Clear",font=('Courier', 10), command = self.DisplaySceneMarkInfoCLEAR)
        DisplaySceneMarkInfoCLEAR.pack(side=tk.TOP, expand=tk.NO)
        self.DisplaySceneMarkInfo = tk.Text(self.DisplaySceneMarkInfo_Frame, width = 50, height = 19) 
        DisplaySceneMarkInfo_sbarV = Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.VERTICAL)
        DisplaySceneMarkInfo_sbarH = Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.HORIZONTAL)
        DisplaySceneMarkInfo_sbarV.config(command=self.DisplaySceneMarkInfo.yview)
        DisplaySceneMarkInfo_sbarH.config(command=self.DisplaySceneMarkInfo.xview)
        self.DisplaySceneMarkInfo.config(yscrollcommand=DisplaySceneMarkInfo_sbarV.set)
        self.DisplaySceneMarkInfo.config(xscrollcommand=DisplaySceneMarkInfo_sbarH.set)
        DisplaySceneMarkInfo_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        DisplaySceneMarkInfo_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.DisplaySceneMarkInfo.pack(side=tk.TOP, expand=tk.NO)
    def DisplaySceneMarkInfoCLEAR(self, event = None):
        self.DisplaySceneMarkInfo.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR")
    def askcolor1(self, event = None):
        self.color1 = askcolor()
        self.Color1Button.configure(bg=self.color1[1])
        self.color_1 = self.HTMLColorToRGB(self.color1[1])

    def askcolor2(self, event = None):
        self.color2 = askcolor()
        self.Color2Button.configure(bg=self.color2[1])
        self.color_2 = self.HTMLColorToRGB(self.color2[1])
    """
    def askcolor3(self, event = None):
        self.color3 = askcolor()
        self.Color3Button.configure(bg=self.color3[1])
        print(self.HTMLColorToRGB(self.color3[1]))
    def askcolor4(self, event = None):
        self.color4 = askcolor()
        self.Color4Button.configure(bg=self.color4[1])
        print(self.HTMLColorToRGB(self.color4[1]))
    """
    def HTMLColorToRGB(self,colorstring):
        """ convert #RRGGBB to an (R, G, B) tuple """
        colorstring = colorstring.strip()
        if colorstring[0] == '#': colorstring = colorstring[1:]
        if len(colorstring) != 6:
            raise(ValueError, "input #%s is not in #RRGGBB format" % colorstring)
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]
        return (r, g, b)

    def workon_openalpr(self, event = None):
        print(self.imageFile)
        IMAGE_PATH = self.imageFile
        SECRET_KEY = self.OpenALPRkey.get()
        with open(IMAGE_PATH, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())

        img = cv2.imread(IMAGE_PATH)

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
        r = requests.post(url, data = img_base64)

        jsonfile = "Traffic_output.json"
        with open(jsonfile, 'w') as fp:
            json.dump(r.json(), fp)

        with open('Traffic_output.json') as data_file:
            data = json.loads(data_file.read())       
        #draw the rectangle on the license plate
        cv2.rectangle(img,
                     (data['results'][0]['coordinates'][0]['x'], data['results'][0]['coordinates'][0]['y']),
                     (data['results'][0]['coordinates'][2]['x'], data['results'][0]['coordinates'][2]['y']),
                     self.color_1,int(self.linesizespinbox.get()))
        #draw the rectangle on the car
        cv2.rectangle(img,
                     (data['results'][0]['vehicle_region']['x'],data['results'][0]['vehicle_region']['y']),
                     (data['results'][0]['vehicle_region']['x']+data['results'][0]['vehicle_region']['width'],
                      data['results'][0]['vehicle_region']['y']+data['results'][0]['vehicle_region']['height']),
                     self.color_2,int(self.linesizespinbox.get()))

        cv2.imwrite('Traffic_output.png', img)

        self.DisplaySceneMarkInfo.insert(tk.END,'plate: '+ data['results'][0]['plate']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'region: '+ data['results'][0]['region']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'orientation: '+ data['results'][0]['vehicle']['orientation'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'color: '+ data['results'][0]['vehicle']['color'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'make as: '+ data['results'][0]['vehicle']['make'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'body type: '+ data['results'][0]['vehicle']['body_type'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'year: '+ data['results'][0]['vehicle']['year'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,'make model: '+ data['results'][0]['vehicle']['make_model'][0]['name']+'\n') 

        while True:
            # 複製一份原始影像
            imOut = img.copy()
            # 顯示結果
            cv2.imshow("Output", imOut)
            # 讀取使用者所按下的鍵
            k = cv2.waitKey(0) & 0xFF
            # 若按下 q 鍵，則離開
            if k == 113:
                break
        # 關閉圖形顯示視窗
        cv2.destroyAllWindows()               
  
    def init_OpenALPR_tab(self):
        self.OpenALPR_tab = tk.Frame(self.OpenALPRPanel)
        self.OpenALPR_tab.pack(side=tk.TOP, expand=tk.NO)
        #self.imgfunnotebook.add(self.OpenALPR_tab, text="Open ALPR")

        self.OpenALPRkey = tk.StringVar()
        self.OpenALPRkey.set('')
        tk.Label(self.OpenALPR_tab, text='SECRET\n KEY', font=('Courier', 8),width=8, height=2).pack(side=tk.LEFT, expand=tk.NO)
        self.Secret_OpenALPRKey = tk.Entry(self.OpenALPR_tab, textvariable=self.OpenALPRkey,font=('Courier', 10))
        self.Secret_OpenALPRKey.pack(side=tk.LEFT, expand=tk.NO)
        
        self.workonOpenALPRButton = tk.Button(self.OpenALPR_tab, text = "Workon ",font=('Courier', 10), command = self.workon_openalpr)
        self.workonOpenALPRButton.pack(side=tk.LEFT, expand=tk.NO)

if __name__ == '__main__':
    root = tk.Tk()
    OpenALPR(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()      

