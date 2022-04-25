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
        IptNum = int(input("[INPUT] Input No.: ")) - 1

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
    
    try:
        os.mkdir(dirf + "\\Courseware\\")
        os.makedirs(dirf + "\\Courseware\\Resources\\")
        os.makedirs(dirf + "\\Courseware\\Slides\\")
        print("[MAKEDIR] Done!")
    except:
        print("[MAKEDIR] Failed!")
    
    url = "https://easilive.seewo.com/enow/open/api/v1/courseware/2/detail?shareLinkUid=&accessCode=" + ac + "&cid=&turnMp4=true&expireSeconds=10800&w=1280&h=612&turnWebp=false"
    fl = requests.get(url, headers=headers)
    filelist=json.loads(fl.content)
    if filelist["error_code"] != 0:
        print("[ERROR] " + filelist["message"])
        return
    
    cnt = 0
    for i in filelist["data"]["files"]:
        try:
            DownloadUrl = filelist["data"]["files"][cnt]["url"]
            FilePath = filelist["data"]["files"][cnt]["path"]
            print("[DOWNLOAD] FILE:" + filelist["data"]["files"][cnt]["name"])
            request_download(DownloadUrl, dirf + "\\Courseware\\" + FilePath)
            print("[DONE] SIZE: " + str(filelist["data"]["files"][cnt]["size"]))
        except Exception as re:
            print(re)
            continue
        cnt+=1
    print("======[ FINNISH ]======")
    print('[MSG] Download Process Finished，Trying To Package The Courseware...')
    dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    print("[DEBUG] AppDir: " + dirf + "\\")
    print("[DEBUG] CoursewareDir: " + dirf + "\\Courseware\\")
    
    print("======[ PACKING ]======")
    os.system("cd " + dirf + "\\Courseware\\ && " + sys.argv[0] + " -p " + dirf + " " + DelEvalString(zName) + ".enbx")
    #调用自己，打包课件
    
    print("======[ DELATING ]======")
    os.system(sys.argv[0] + " -del")
    #调用自己，删除临时的下载文件

def main():
    #主程序
    print("Welcome Using Lizhi Courseware Tool (Lite)")
    print("输入courseUid来获取教室课件资源，你可以在教室的链接中找到它（如\".../room?courseUid=[这里就是courseUid]&appCode...\"）")
    cUid = input("[INPUT] courseUid: ")
    print("")
    CList = getCoursewareList(cUid)

    if CList == {}:
        print("[ERROR] Please Input The Right No.")
        sys.exit(0)
    else:
        print("======[ PROCESSING ]======")
        submit(str(CList["accessCode"]), str(CList["name"]))

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
            #删除用于下载的临时文件
            dirf = dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
            try:
                shutil.rmtree(dirf + "\\Courseware\\")
                print("Done")
            except:
                print("Failed")
            
        elif sys.argv[1] == "-h":
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
