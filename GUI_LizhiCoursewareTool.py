import requests
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
import json
import os
import sys
import zipfile
import shutil

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

def init():
    dirf = dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    try:
        shutil.rmtree(dirf + "\\Courseware\\")
        print("[DELETE] Done!")
    except:
        print("[DELETE] Failed!")
    #删除之前的临时文件
    
    try:
        os.mkdir(dirf + "\\Courseware\\")
        os.makedirs(dirf + "\\Courseware\\Resources\\")
        os.makedirs(dirf + "\\Courseware\\Slides\\")
        print("[MAKEDIR] Done!")
    except:
        print("[MAKEDIR] Failed!")

def DelEvalString(s):
    #该函数用于去除课件名中的敏感字符
    #该函数用于避免恶意课件的非法命名
    #造成的影响具体表现为：电脑用户无法删除、移动、修改下载的文件。
    s = s.replace("\\", "_").replace("/", "_").replace(":", "_").replace("\"", "_").replace(" ", "_")
    s = s.replace("*", "_").replace("?", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    return s

def GoZip(absDir,zipFile):
    #打包课件函数
    for f in os.listdir(absDir):
        absFile=os.path.join(absDir,f)
        if os.path.isdir(absFile):
            relFile=absFile[len(os.getcwd())+1:]
            zipFile.write(relFile)
            GoZip(absFile,zipFile)
        else:
            relFile=absFile[len(os.getcwd())+1:]
            zipFile.write(relFile)
    return

def getCoursewareList():
    url = "https://s2.imlizhi.com/slive/pc/apis.json?actionName=GET_COURSE_ACCESS_CODE_LIST&t=1650588247339"
    #接入立知后台

    clist.delete(0, END)
    entryGet = Entry1.get()
    
    try:
        cUid = entryGet.split("?")[1].split("&")[0].split("=")[1]
    except:
        cUid = entryGet
    
    data = {"courseUid":cUid}
    fl = requests.post(url=url, data=data, headers=headers)
    
    global courselist
    courselist = json.loads(fl.content)

    global CoursewareNum
    CoursewareNum = 0
    
    if courselist["error_code"] != 0:
        showerror('错误 [' + str(courselist["error_code"]) +'] ', courselist["message"])
        #return "error"
    else:
        lasturl = entryGet
        for dl in courselist["data"]:
            CoursewareNum += 1
            clist.insert(0,dl["name"])

def request_download(IMAGE_URL, fn):
    r = requests.get(IMAGE_URL)
    with open(fn, 'wb') as f:
        f.write(r.content)

def submit(ac):
    init()
    pb['value'] = 0.00    
    url = "https://easilive.seewo.com/enow/open/api/v1/courseware/2/detail?shareLinkUid=&accessCode=" + ac + "&cid=&turnMp4=true&expireSeconds=10800&w=1280&h=612&turnWebp=false"
    fl = requests.get(url, headers=headers)
    filelist=json.loads(fl.content)
    
    
    PageNum = 0
    for i in filelist["data"]["files"]:
        PageNum += 1

    cnt = 0
    for i in filelist["data"]["files"]:
        try:
            DownloadUrl = filelist["data"]["files"][cnt]["url"]
            FilePath = filelist["data"]["files"][cnt]["path"].replace("\\", "/")
            request_download(DownloadUrl, "./Courseware/" + FilePath)
            pb['value'] += (100.00 / PageNum)
            win.update()
        except Exception as re:
            print(re)
            continue
        cnt+=1
    showinfo('提示', '完成下载！')

def select():
    IptNum = CoursewareNum - int(clist.curselection()[0]) - 1
    submit(courselist["data"][IptNum]["accessCode"])
    global zName
    zName = courselist["data"][IptNum]["name"]

def StartExecToPack():
    dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    #获取程序所在的根目录
    
    print("======[ PACKING ]======")

    try:
        os.system("cd " + dirf + "\\Courseware\\ && " + sys.argv[0] + " -p " + dirf + " " + DelEvalString(zName) + ".enbx")
    except:
        os.system("cd " + dirf + "\\Courseware\\ && " + sys.argv[0] + " -p " + dirf + " Courseware.enbx")
    
    showinfo('提示', '打包完成！')

    dirf = dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    try:
        shutil.rmtree(dirf + "\\Courseware\\")
        print("[DELETE] Done!")
    except:
        print("[DELETE] Failed!")
    #自动删除临时文件

def main():
    global win
    win = Tk()
    win.title('立知课堂课件下载器')
    win.geometry('514x335+150+150')
    
    Label1 = ttk.Label(win, text='直播教室链接:', font=('黑体', 12), anchor=W).place(y=13, x=14, width=130, height=26)

    text_entry = StringVar()
    text_entry.set('')

    global Entry1
    Entry1 = ttk.Entry(win, font=('黑体', 11), textvariable = text_entry, width = 290)
    Entry1.place(y=13, x=130, width=290, height=26)
    Entry1.focus_set()

    Button1 = ttk.Button(win, text='查询', command = getCoursewareList).place(y=13, x=435, width=65, height=26)

    global clist
    clist = Listbox(win, font=('黑体', 11))
    clist.place(y=56, x=15, width=236, height=241)

    global pb
    pb = ttk.Progressbar(win)
    pb.place(y=300, x=14, width=162, height=26)
    pb['maximum'] = 100.00
    
    Button2 = ttk.Button(win, text='下载', command = select).place(y=300, x=185, width=65, height=26)

    Label2 = ttk.Label(win, text='功能区:', font=('黑体', 12), anchor=W).place(y=56, x=281, width=200, height=26)
    Button3 = ttk.Button(win, text='将下载的课件打包', command = StartExecToPack).place(y=87, x=281, width=200, height=26)
    win.mainloop()

def execData():
    #这里是用于ZIP打包时获取后缀信息
    try:
        if sys.argv[1] == "-p":
            #打包课件部分
            zPath = sys.argv[2]
            zName = DelEvalString(sys.argv[3])
            if zName.replace(".enbx", "") == "":
                zName = "Courseware.enbx"
            
            zipFilePath = os.path.join(zPath, zName)
            zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
            absDir = os.path.join(zPath, "Courseware")
            GoZip(absDir, zipFile)
            
            sys.exit(0)
    except Exception as re:
        print(re)
        return ""

if __name__ == '__main__':
    a = execData()
    if a == "":
        main()



