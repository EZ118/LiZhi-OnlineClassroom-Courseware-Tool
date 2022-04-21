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
    "Cookie": "x-auth-app=en-easilive; ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64;` rv:47.0) Gecko/20100101 Firefox/47.0"
}

def request_download(IMAGE_URL, fn):
    r = requests.get(IMAGE_URL)
    with open(fn, 'wb') as f:
        f.write(r.content)

def GoZip(absDir,zipFile):
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

def submit(ac):
    dirf = dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    try:
        shutil.rmtree(dirf + "\\Courseware\\")
        print("[DEL] Done!")
    except:
        print("[DEL] Failed!")
    
    try:
        os.mkdir(dirf + "\\Courseware\\")
        os.makedirs(dirf + "\\Courseware\\Resources\\")
        os.makedirs(dirf + "\\Courseware\\Slides\\")
        print("[MD] Done!")
    except:
        print("[MD] Failed!")
    
    url = "https://easilive.seewo.com/enow/open/api/v1/courseware/2/detail??shareLinkUid=&accessCode=" + ac + "&cid=&turnMp4=true&expireSeconds=10800&w=1280&h=612&turnWebp=false"
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
    print('[MSG] 完成下载，正在尝试打包课件...')
    dirf = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    print("[DEBUG] AppDir: " + dirf + "\\")
    print("[DEBUG] CoursewareDir: " + dirf + "\\Courseware\\")
    os.system("cd " + dirf + "\\Courseware\\ && " + sys.argv[0] + " -p " + dirf)

try:
    if sys.argv[1] == "-p":
        print("======[ PACKING ]======")
        zipFilePath = os.path.join(sys.argv[2], "Courseware.enbx")
        zipFile = zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED)
        absDir = os.path.join(sys.argv[2], "Courseware")
        GoZip(absDir, zipFile)
        print("[MSG] DONE!")
        sys.exit(0)
    elif sys.argv[1] == "-d":
        print("Downloading...")
        submit(sye.argv[2])
    elif sys.argv[1] == "-h":
        print("-d [AccessCode]           <Start Download>")
        print("-h                        <Print Help MSG>")
        print("-p [path]                 <Start Packing>")
    
except Exception as re:
    print(re)
    print("")

print("Welcome Using Lizhi Courseware Tool (Lite)")
print("Now, Enter The AccessCode Of The Courseware, you can find it in Network item of F12 Tool when online classroom loading.")
data = input("ACCESSCODE: ")
print("")
print("======[ PROCESSING ]======")
submit(data)
