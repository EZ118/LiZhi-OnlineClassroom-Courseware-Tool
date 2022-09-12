import requests
import sys
import json
import pyperclip
from tkinter import *
from tkinter.messagebox import *

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


def getCoursewareList():
    url = "https://easilive.seewo.com/apis.json?actionName=STUDENT_GET_COURSE_LIST_WITH_PAGE&ts=1662983257493"
    #接入立知后台

    global filelist
    fl_tmp = {}

    for i in range(0,10):
        data = {"page":i,"pageSize":100}
        fl = requests.post(url=url, data=data, headers=headers)
        if i == 0:
            filelist = json.loads(fl.content)
    
        fl_tmp = json.loads(fl.content)
        try:
            filelist["data"]["content"] += fl_tmp["data"]["content"]
        except:
            print("error")
        win.update()

    clist.delete(0, END)
    if filelist["error_code"] != 0:
        showerror('错误 [' + str(filelist["error_code"]) +'] ', filelist["message"])
        #return "error"
    else:
        global cnt
        cnt = 0
        for dl in filelist["data"]["content"]:
            cnt += 1
            clist.insert(END, str(cnt) + ". " + dl["name"])

            
def OK1():
    IptNum = int(clist.curselection()[0])
    pyperclip.copy(filelist["data"]["content"][IptNum]["uid"])

def OK2():
    IptNum = int(clist.curselection()[0])
    pyperclip.copy(filelist["data"]["content"][IptNum]["name"])

def OK3():
    IptNum = int(clist.curselection()[0])
    pyperclip.copy("https://easilive.seewo.com/preview/replay?courseId=" + filelist["data"]["content"][IptNum]["uid"] + "&origin=course")

def Main():
    global win, text_entry, clist
    win = Tk()
    win.title('Get Course List')
    win.geometry('314x350+150+150')

    ButtonGo = Button(win, text='I want My CourseList Now!', font=('黑体', 11), command = getCoursewareList).place(y=15, x=15, width=286, height=28)

    clist = Listbox(win, font=('黑体', 11))
    clist.place(y=57, x=15, width=286, height=241)

    ButtonCid = Button(win, text='COPY UID', font=('黑体', 11), command = OK1).place(y=310, x=15, width=69.3, height=28)
    ButtonAc = Button(win, text='COPY NAME', font=('黑体', 11), command = OK2).place(y=310, x=98.3, width=69.3, height=28)
    ButtonUrl = Button(win, text='COPY URL', font=('黑体', 11), command = OK3).place(y=310, x=181.6, width=69.3, height=28)

    win.mainloop()


if __name__ == '__main__':
    Main()
    
