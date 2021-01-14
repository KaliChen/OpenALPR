# OpenALPR
OpenALPR 是自動車牌辨識的開源函式庫，提供的API拿來做車輛辨識工具

![https://ithelp.ithome.com.tw/upload/images/20200928/20119608KXW18jikKi.jpg](https://ithelp.ithome.com.tw/upload/images/20200928/20119608KXW18jikKi.jpg)
![https://ithelp.ithome.com.tw/upload/images/20200928/20119608jcqerG0Ix9.png](https://ithelp.ithome.com.tw/upload/images/20200928/20119608jcqerG0Ix9.png)

## 範例
```
import requests
import base64
import json

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
IMAGE_PATH = '/tmp/sample.jpg'
SECRET_KEY = '*******************'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v3/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)

print(json.dumps(r.json(), indent=2))
```

定義字型線條種類和線的粗細
```
fontlinetype_Item = {cv2.LINE_AA:'LINE_AA',cv2.LINE_8:'LINE_8'}
linewidth = ( 1, 2, 3, 4, 5)
```

定義模組OpenALPR，self.imageFile是圖片來源指標，self.color_1和self.color_2為調色按鈕，定義一個self.OpenALPRPanel為帶框線的面板，接下來有三個程式依序執行:self.init_OpenALPR_tab(),  self.init_setting_tab(), self.init_DisplaySceneMarkInfo_tab()

```
class OpenALPR():
    def __init__(self, master):
        self.parent = master
        self.imageFile = str()
        self.color_1 = (0,0,0)
        self.color_2 = (0,0,0)
        self.OpenALPRPanel = tk.LabelFrame(self.parent,
                                           text="OpenALPR",
                                           font=('Courier', 10))
        self.OpenALPRPanel.pack(side=tk.LEFT,
                                expand=tk.NO,
                                fill = tk.X)
        self.init_OpenALPR_tab()
        self.init_setting_tab()
        self.init_DisplaySceneMarkInfo_tab()

```
定義模組內的函式init_setting_tab(), 設定的功能有2個調色鍵，文字線條種類和框線線條粗細
```
    def init_setting_tab(self):
        self.setting_tab = tk.Frame(self.OpenALPRPanel)
        self.setting_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

        self.MarkSettingPanel = tk.LabelFrame(self.setting_tab,
                                        text="Color and font Setting Panel",
                                        font=('Courier', 10))
        self.MarkSettingPanel.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        ColorPanel = tk.Frame(self.MarkSettingPanel)
        ColorPanel.grid(row = 0, column = 0 ,sticky = tk.E+tk.W)
 
        self.Color1Button = tk.Button(ColorPanel,
                                      text = "Color 1",
                                      font=('Courier', 10),
                                      command = self.askcolor1)
        self.Color1Button.grid(row = 0, column = 0, sticky = tk.E+tk.W)

        self.Color2Button = tk.Button(ColorPanel,
                                      text = "Color 2",
                                      font=('Courier', 10), 
                                      command = self.askcolor2)
        self.Color2Button.grid(row = 1, column = 0, sticky = tk.E+tk.W)

        '''font line type setting'''
        fontcv2Panel = tk.Frame(self.MarkSettingPanel)
        fontcv2Panel.grid(row = 0, column = 1 ,sticky = tk.E+tk.W)
        
        '''Line Size'''
        tk.Label(self.MarkSettingPanel,
                 text = "Line size",
                 font=('Courier', 10)).grid(row = 0,
                                            column = 4,
                                            sticky = tk.E+tk.W)
        self.linesizespinbox = tk.Spinbox(self.MarkSettingPanel,
                                          values = linewidth,
                                          width = 3)
        self.linesizespinbox.grid(row = 0,
                                  column = 5,
                                  sticky = tk.E+tk.W)
        '''font line type setting'''
        fontlinetypecv2Panel = tk.Frame(self.MarkSettingPanel)
        fontlinetypecv2Panel.grid(row = 0,
                                  column = 6 ,
                                  sticky = tk.E+tk.W)
        '''line type label'''
        tk.Label(fontlinetypecv2Panel, 
                 text = "line type",
                 font=('Courier', 10)).pack(side = tk.TOP, 
                                            expand=tk.YES,
                                            fill=tk.BOTH)
        self.fontlinetypecv2Var = tk.IntVar()
        self.fontlinetypecv2Var.set(8)
        for val, linetype, in fontlinetype_Item.items(): 
            tk.Radiobutton(fontlinetypecv2Panel,
            text = linetype, 
            variable = self.fontlinetypecv2Var,
            value = val,
            font=('Courier', 10)).pack(side = tk.TOP,
                                       expand=tk.YES,
                                       fill=tk.BOTH)
```
顯示偵測回饋資訊的面板，含一個文字清除鍵, 一個文字物件
```
    def init_DisplaySceneMarkInfo_tab(self):
        self.DisplaySceneMarkInfo_Frame = tk.LabelFrame(self.OpenALPRPanel, 
                                              text="Display OpenALPR Info",
                                              font=('Courier', 9))
        self.DisplaySceneMarkInfo_Frame .pack(side=tk.TOP, expand=tk.NO)
        DisplaySceneMarkInfoCLEAR =tk.Button(self.OpenALPRPanel,
                                       text = "Clear",
                                      font=('Courier', 10),
                                   command = self.DisplaySceneMarkInfoCLEAR)
        DisplaySceneMarkInfoCLEAR.pack(side=tk.TOP, expand=tk.NO)
        self.DisplaySceneMarkInfo = tk.Text(self.DisplaySceneMarkInfo_Frame,
                                            width = 50,
                                            height = 19) 
        DisplaySceneMarkInfo_sbarV = Scrollbar(
                                        self.DisplaySceneMarkInfo_Frame,
                                        orient=tk.VERTICAL)
        DisplaySceneMarkInfo_sbarH = Scrollbar(
                                       self.DisplaySceneMarkInfo_Frame,
                                       orient=tk.HORIZONTAL)
        DisplaySceneMarkInfo_sbarV.config(
                    command=self.DisplaySceneMarkInfo.yview)
        DisplaySceneMarkInfo_sbarH.config(
                    command=self.DisplaySceneMarkInfo.xview)
        self.DisplaySceneMarkInfo.config(
                    yscrollcommand=DisplaySceneMarkInfo_sbarV.set)
        self.DisplaySceneMarkInfo.config(
                    xscrollcommand=DisplaySceneMarkInfo_sbarH.set)
        DisplaySceneMarkInfo_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        DisplaySceneMarkInfo_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.DisplaySceneMarkInfo.pack(side=tk.TOP, expand=tk.NO)
 ```
 清除回饋資訊的按鍵
 ```
    def DisplaySceneMarkInfoCLEAR(self, event = None):
        self.DisplaySceneMarkInfo.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR")
 ```
 調色按鍵1
 ```
    def askcolor1(self, event = None):
                  .
                  .
                  .
 ```
 調色按鍵2
 ```
    def askcolor2(self, event = None):
                  .
                  .
                  .
 ```
執行OpenALPR
```
    def workon_openalpr(self, event = None):
        #圖檔來源
        IMAGE_PATH = self.imageFile
        #API金鑰
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
                     (data['results'][0]['coordinates'][0]['x'],
                     data['results'][0]['coordinates'][0]['y']),
                     (data['results'][0]['coordinates'][2]['x'],
                     data['results'][0]['coordinates'][2]['y']),
                     self.color_1,int(self.linesizespinbox.get()))
                     
        #draw the rectangle on the car
        cv2.rectangle(img,
                     (data['results'][0]['vehicle_region']['x'],
                     data['results'][0]['vehicle_region']['y']),
                     (data['results'][0]['vehicle_region']['x']+
                     data['results'][0]['vehicle_region']['width'],
                      data['results'][0]['vehicle_region']['y']+
                      data['results'][0]['vehicle_region']['height']),
                     self.color_2,int(self.linesizespinbox.get()))

        cv2.imwrite('Traffic_output.png', img)

        self.DisplaySceneMarkInfo.insert(tk.END,
                   'plate: '+ data['results'][0]['plate']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                   'region: '+ data['results'][0]['region']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                   'orientation: '+
                 data['results'][0]['vehicle']['orientation'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                   'color: '+
                   data['results'][0]['vehicle']['color'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                   'make as: '+
                   data['results'][0]['vehicle']['make'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                   'body type: '+
                   data['results'][0]['vehicle']['body_type'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                   'year: '+
                   data['results'][0]['vehicle']['year'][0]['name']+'\n')
        self.DisplaySceneMarkInfo.insert(tk.END,
                 'make model: '+
                 data['results'][0]['vehicle']['make_model'][0]['name']+'\n')

        while True:
            imOut = img.copy()
            cv2.imshow("Output", imOut)
            k = cv2.waitKey(0) & 0xFF
            if k == 113: # 若按下 q 鍵，則離開
                break
        cv2.destroyAllWindows()               
```
輸入金鑰及按下運作的面板
```
    def init_OpenALPR_tab(self):
        self.OpenALPR_tab = tk.Frame(self.OpenALPRPanel)
        self.OpenALPR_tab.pack(side=tk.TOP, expand=tk.NO)
        self.OpenALPRkey = tk.StringVar()
        self.OpenALPRkey.set('Key of OpenALPR')
        tk.Label(self.OpenALPR_tab,
                 text='SECRET\n KEY',
                 font=('Courier', 8),
                 width=8,
                 height=2).pack(side=tk.LEFT, expand=tk.NO)
        self.Secret_OpenALPRKey = tk.Entry(self.OpenALPR_tab,  
                                           textvariable=self.OpenALPRkey,
                                           font=('Courier', 10))
        self.Secret_OpenALPRKey.pack(side=tk.LEFT, expand=tk.NO)
        
        self.workonOpenALPRButton = tk.Button(self.OpenALPR_tab,
                                              text = "Workon ",
                                              font=('Courier', 10),
                                              command = self.workon_openalpr)
        self.workonOpenALPRButton.pack(side=tk.LEFT, expand=tk.NO)
```
