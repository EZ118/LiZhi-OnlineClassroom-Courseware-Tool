import requests
import json
import os
import sys
import zipfile
import shutil

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cookie": "x-auth-token=7516bf29191348b683bb7c3b4c601c1a; x-auth-app=en-easilive; ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;` rv:47.0) Gecko/20100101 Firefox/47.0"
}
#请求时传输的Cookies、UA等待数据

def DelEvalString(s):
    #该函数用于去除课件名中的敏感字符
    #该函数用于避免恶意课件的非法命名
    #造成的影响具体表现为：电脑用户无法删除、移动、修改下载的文件。
    s = s.replace("\\", "_").replace("/", "_").replace(":", "_").replace("\"", "_").replace(" ", "_")
    s = s.replace("*", "_").replace("?", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    return s

def getCoursewareList(cUid):
    #用于通过courseUid获取课件列表
    
    url = "https://s2.imlizhi.com/slive/pc/apis.json?actionName=GET_COURSE_ACCESS_CODE_LIST&t=1650588247339"
    #接入立知后台
    
    data = {"courseUid":cUid}
    fl = requests.post(url=url, data=data, headers=headers)
    filelist = json.loads(fl.content)
    
    if filelist["error_code"] != 0:
        #当返回的结果输出错误代码
        
        print("[ERROR] " + filelist["message"])
        return "error"
    else:
        #正确返回
        
        print("[MSG] Choose A Courseware To Download")
        #提示选择返回的课件列表
        
        cnt = 0
        for dl in filelist["data"]:
            cnt += 1
            print("< " + str(cnt) + " > NAME: " + dl["name"])
        #输出得到的课件列表
        
        IptNum = int(input("[INPUT] Input No.: ")) - 1
        #输入想要的课件号

        if IptNum < 0 or IptNum >= cnt:
            return {}
        else:
            return {"name":filelist["data"][IptNum]["name"],"cid":filelist["data"][IptNum]["cid"],"accessCode":filelist["data"][IptNum]["accessCode"],"version":filelist["data"][IptNum]["version"]}


def request_download(IMAGE_URL, fn):
    #用于课件文件下载工具
    r = requests.get(IMAGE_URL)
    with open(fn, 'wb') as f:
        f.write(r.content)

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

def submit(ac, zName):
    #课件下载部分
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
    #重新创建临时下载文件夹
    
    url = "https://easilive.seewo.com/enow/open/api/v1/courseware/2/detail?shareLinkUid=&accessCode=" + ac + "&cid=&turnMp4=true&expireSeconds=10800&w=1280&h=612&turnWebp=false"
    fl = requests.get(url, headers=headers)
    filelist=json.loads(fl.content)
    #从接口获取信息
    
    if filelist["error_code"] != 0:
        print("[ERROR] " + filelist["message"])
        return
    #确保返回的状态正常
    
    cnt = 0
    for i in filelist["data"]["files"]:
        #课件下载部分
        try:
            DownloadUrl = filelist["data"]["files"][cnt]["url"]
            FilePath = filelist["data"]["files"][cnt]["path"]
            print("[DOWNLOAD] FILE: " + filelist["data"]["files"][cnt]["name"])
            request_download(DownloadUrl, dirf + "\\Courseware\\" + FilePath)
            print("[DONE] SIZE: " + str(filelist["data"]["files"][cnt]["size"]) + " byte")
        except Exception as re:
            print(re)
            continue
        cnt+=1
    print("======[ FINNISH ]======")
    
    print('[MSG] Download Process Finished，Trying To Package The Courseware...')    
    dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    print("[DEBUG] AppDir: " + dirf + "\\")
    print("[DEBUG] CoursewareDir: " + dirf + "\\Courseware\\")
    #获取程序所在的根目录
    
    print("======[ PACKING ]======")
    os.system("cd " + dirf + "\\Courseware\\ && " + sys.argv[0] + " -p " + dirf + " " + DelEvalString(zName) + ".enbx")
    #调用自己，打包课件
    
    print("======[ DELATING ]======")
    os.system(sys.argv[0] + " -del")
    #调用自己，删除临时的下载文件

def main():
    #主程序

    print("Welcome Using Lizhi Courseware Tool (Lite)")
    print("输入立知课堂浏览器版的直播教室链接（或couseUid）")
    cUid = input("[INPUT] URL: ")
    #输出问候语并向用户询问课程链接
    
    print("")
    
    if "https://" in cUid:
        try:
            cUid = cUid.split("?")[1].split("&")[0].split("=")[1]
            print("[DEBUG] Get Uid From Web Link,uid=" + cUid)
        except:
            print("[ERROR] Failed to Get Uid From Web Link!")
            return
    else:
        print("[DEBUG] Get Uid Directly")
    #从URL中提取courseUid或直接获取courseUid
    
    CList = getCoursewareList(cUid)
    #调用函数，返回用户所选的课件的详细信息（包括课件名、课件访问代码、课件编号、课件版本）
    
    if CList == {}:
        #当函数的返回值表示为空数组
        print("[ERROR] Please Input The Right No.")
        return
    else:
        print("======[ PROCESSING ]======")
        submit(str(CList["accessCode"]), str(CList["name"]))
        #向课件下载函数传递课程访问代码、课程名称

def execData():
    #这里是用于ZIP打包时获取后缀信息
    try:
        if sys.argv[1] == "-p":
            #打包课件部分
            zPath = sys.argv[2]
            zName = DelEvalString(sys.argv[3])
            
            zipFilePath = os.path.join(zPath, zName)
            zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
            absDir = os.path.join(zPath, "Courseware")
            GoZip(absDir, zipFile)
            print("[MSG] DONE!")
            sys.exit(0)
            
        elif sys.argv[1] == "-d":
            #下载部分（外部程序调用）
            print("Downloading...")
            submit(sye.argv[2], sye.argv[3])
            
        elif sys.argv[1] == "-del":
            #删除下载后保留的临时文件
            dirf = dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
            try:
                shutil.rmtree(dirf + "\\Courseware\\")
                print("Done")
            except:
                print("Failed")
            
        elif sys.argv[1] == "-h":
            #命令行帮助
            print("-d [AccessCode] [SaveName]   <Start Download>")
            print("-h                           <Print Help MSG>")
            print("-p [path] [SaveName]         <Start Packing>")
            print("-del                         <Del Temp Files >")
        
        return "ok"
        
    except Exception as re:
        #print(re)
        return ""

if __name__ == '__main__':
    a = execData()
    if a == "":
        main()
