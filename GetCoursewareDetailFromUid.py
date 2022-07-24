import requests
import sys
import json
import pyperclip
from tkinter import *
from tkinter.messagebox import *
import pyzbar.pyzbar as pyzbar
from PIL import Image,ImageEnhance

with open('AuthToken.key',"r") as f:    #设置文件对象
    token = f.read()
#token表示用户识别字符串，如果使用时提示“auth fail”，请按照：
#https://github.com/EZ118/LiZhi-OnlineClassroom-Courseware-Tool/blob/main/README.md
#所示的“维护方法”，修复提示。
#注：每个人的用户识别字符串不同，而且字符串会随着时间而变化，所以说目前是无法完全修复的!

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "x-auth-token=" + token + "; x-auth-app=en-easilive; ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;` rv:47.0) Gecko/20100101 Firefox/47.0"
}
#请求时传输的Cookies、UA等待数据


global readerUrl
readerUrl = "https://easilive.seewo.com/ZZY_WISU/"


def scanBarCode(fp):
    image= fp
    img = Image.open(image)
    img = ImageEnhance.Sharpness(img).enhance(17.0)#锐利化
    img = ImageEnhance.Contrast(img).enhance(4.0)#增加对比度
    img = img.convert('L')#灰度化

    CodeUrl = []
    
    barcodes=pyzbar.decode(img)
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        CodeUrl.append(barcodeData)
    return CodeUrl

def getCoursewareList():
    url = "https://s2.imlizhi.com/slive/pc/apis.json?actionName=GET_COURSE_ACCESS_CODE_LIST&t=1650588247339"
    #接入立知后台

    clist.delete(0, END)
    entryGet = Entry1.get()
    copyGet = pyperclip.paste()
    
    if entryGet == "":
        text_entry.set(copyGet)
        print("Get From Clipboard")
    else:
        print("Get From Entry Box")
    
    entryGet = Entry1.get()
    
    try:
        cUid = (entryGet + "&").split("?")[1].split("&")[0].split("=")[1]
    except:
        cUid = entryGet
    
    data = {"courseUid":cUid}
    fl = requests.post(url=url, data=data, headers=headers)
    
    global filelist
    filelist = json.loads(fl.content)
    
    if filelist["error_code"] != 0:
        showerror('错误 [' + str(filelist["error_code"]) +'] ', filelist["message"])
        #return "error"
    else:
        global cnt
        cnt = 0
        lasturl = entryGet
        for dl in filelist["data"]:
            cnt += 1
            clist.insert(0,dl["name"])

            
def OK1():
    IptNum = cnt - int(clist.curselection()[0]) - 1
    pyperclip.copy(filelist["data"][IptNum]["cid"])
    print("Version: " + str(filelist["data"][IptNum]["version"]))

def OK2():
    IptNum = cnt - int(clist.curselection()[0]) - 1
    pyperclip.copy(filelist["data"][IptNum]["accessCode"])

def OK3():
    IptNum = cnt - int(clist.curselection()[0]) - 1
    pyperclip.copy(readerUrl + "@" + filelist["data"][IptNum]["cid"] + "@0@" + filelist["data"][IptNum]["name"] + "@" + str(filelist["data"][IptNum]["version"]))

def CheckIfQrCodeInput():
    try:
        text_entry.set(scanBarCode(sys.argv[1])[0])
        getCoursewareList()
        return True
    except:
        return False

def Main():
    global win, Entry1, text_entry, clist
    win = Tk()
    win.title('Get AC')
    win.geometry('264x375+150+150')

    Label1 = Label(win, text='courseUid Here:', font=('黑体', 12), anchor=W).place(y=13, x=14, width=234, height=20)

    text_entry = StringVar()
    text_entry.set('')

    Entry1 = Entry(win, font=('黑体', 11), textvariable = text_entry, width = 70)
    Entry1.place(y=41, x=15, width=169, height=26)
    Entry1.focus_set()

    ButtonGo = Button(win, text='Go!', font=('黑体', 11), command = getCoursewareList).place(y=40, x=187, width=65, height=28)

    clist = Listbox(win, font=('黑体', 11))
    clist.place(y=82, x=15, width=236, height=241)

    ButtonCid = Button(win, text='COPY CID', font=('黑体', 11), command = OK1).place(y=335, x=15, width=69.3, height=28)
    ButtonAc = Button(win, text='COPY AC', font=('黑体', 11), command = OK2).place(y=335, x=98.3, width=69.3, height=28)
    ButtonUrl = Button(win, text='COPY URL', font=('黑体', 11), command = OK3).place(y=335, x=181.6, width=69.3, height=28)

    CheckIfQrCodeInput()
    
    win.mainloop()


if __name__ == '__main__':
    Main()
    
