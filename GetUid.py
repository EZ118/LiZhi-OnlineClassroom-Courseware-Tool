import requests
import json
import pyperclip
from tkinter import *

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "x-auth-token=7516bf29191348b683bb7c3b4c601c1a; x-auth-app=en-easilive; ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;` rv:47.0) Gecko/20100101 Firefox/47.0"
}
#请求时传输的Cookies、UA等待数据

def getCoursewareList():
    url = "https://s2.imlizhi.com/slive/pc/apis.json?actionName=GET_COURSE_ACCESS_CODE_LIST&t=1650588247339"
    #接入立知后台

    clist.delete(0, END)
    entryGet = Entry1.get()
    copyGet = pyperclip.paste()
    
    if entryGet == "":
        text_entry.set(copyGet)
    else:
        print("OK")

    entryGet = Entry1.get()
    cUid = entryGet.split("?")[1].split("&")[0].split("=")[1]
    
    data = {"courseUid":cUid}
    fl = requests.post(url=url, data=data, headers=headers)
    global filelist
    filelist = json.loads(fl.content)
    
    if filelist["error_code"] != 0:
        print("[ERROR] " + filelist["message"])
        return "error"
    else:
        lasturl = entryGet
        for dl in filelist["data"]:
            #print("< " + str(cnt) + " > NAME: " + dl["name"])
            clist.insert(0,dl["name"])

            
def OK1():
    IptNum = int(clist.curselection()[0])
    pyperclip.copy(filelist["data"][IptNum]["cid"])

def OK2():
    IptNum = int(clist.curselection()[0])
    pyperclip.copy(filelist["data"][IptNum]["accessCode"])




#print(getCoursewareList())


win = Tk()
win.title('Get AC')
win.geometry('264x375+150+150')

Label1 = Label(win, text='courseUid Here:', font=('黑体', 12), anchor=W).place(y=13, x=14, width=234, height=20)

text_entry = StringVar()
text_entry.set('')

Entry1 = Entry(win, font=('黑体', 11), textvariable = text_entry, width = 70)
Entry1.place(y=41, x=15, width=169, height=26)
Entry1.focus_set()

Button1 = Button(win, text='Go!', font=('黑体', 11), command = getCoursewareList).place(y=40, x=187, width=65, height=28)

clist = Listbox(win, font=('黑体', 11))
clist.place(y=82, x=15, width=236, height=241)

Button2 = Button(win, text='COPY CID', font=('黑体', 11), command = OK1).place(y=335, x=15, width=109.5, height=28)
Button3 = Button(win, text='COPY AC', font=('黑体', 11), command = OK2).place(y=335, x=139.5, width=109.5, height=28)

win.mainloop()

