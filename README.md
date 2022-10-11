# LiZhi-OnlineClassroom-Courseware-Tool  
希沃立知课堂中教师课件自动获取工具，使用Python开发，包括自动下载课件、自动打包课件为enbx等  
因为该程序在运行过程中需要反复调用自己，需要使用系统内置的命令（不同系统命令是不一样的），因此若大家想让这个程序运行在macOS、Linux、Android等，需要按照情况对程序做出相应的改动。而本作者只有Windows PC，没有运行macOS或Linux的电脑。  
如果程序出现问题，请参照本文档的“维护方法”部分！   
**来自编者：最基础的版本所需要的步骤十分复杂，学习成本高，不容易操作。而现在的最新版本**  

## 一、 通过该工具获取课程回放中的课件的方法  
**1.打开立知课堂官网**  
<img width="960" alt="步骤1" src="https://user-images.githubusercontent.com/79049368/164376453-89c8591d-0809-4662-af44-d2401bcb70b7.PNG">

**2.点击需要获取课件的直播课程，然后等待直播加载完成**  

**3.在浏览器的地址栏中全选（Ctrl + A）并复制链接（Ctrl + C）**  
<img width="881" alt="步骤3" src="https://user-images.githubusercontent.com/79049368/164584235-69c660ac-6fad-44cd-85e7-fc6f9f5dfdc7.PNG">

**4.打开程序所在目录（文件夹），并启动程序**  
![步骤4](https://user-images.githubusercontent.com/79049368/165438884-ee3a4959-2961-4480-a480-611582525c25.png)

**5.在弹出的黑框里的“Url: ”后面粘贴刚刚复制的链接（标题栏右键->编辑->粘贴），并按下Enter键（如图）**  
![步骤5](https://user-images.githubusercontent.com/79049368/165437929-1b36b1b0-8279-4681-864c-034743ffb0fd.png)

**6.之后会提示在课件列表中做出选择，选择想要下载的课件后输入所选择的课件名称前的数字序号**  

**7.如果你完美地执行了以上所给的操作，那么就会出现以下界面。**  
提示：程序会执行一段时间（执行时间按照课件大小而定），等到程序界面显示了“===[FINISH]===”后，就会开始打包课件为enbx格式  
打包完毕后，程序会自动关闭。如果你在使用当中关闭了程序，课件将会下载失败！  
<img width="441" alt="步骤7" src="https://user-images.githubusercontent.com/79049368/164379009-620a710f-ce9a-49b9-8f42-d34fded1ac73.PNG">

**8.课件下载完成后，就可以看见软件的目录下出现“课件名 + .enbx”（课件名是按照课件的名称而定的），这个文件就是可以用希沃白板直接打开的课件**  
<img width="490" alt="步骤8" src="https://user-images.githubusercontent.com/79049368/164380886-99aa36d4-e4ea-4aac-b84c-772070ba45fa.PNG">


## 维护方法（出现错误提示框，显示“auth fail”的解决方法）   
**首先，请按照以下图片所示的方式，找到官网中最新的x-auth-token**   
![image](https://user-images.githubusercontent.com/79049368/169180912-a4596f5c-24c6-44e7-aa95-f0f99e27c498.png)   

**接着修改AuthToken.key中的token变量，将上一步所找到的x-auth-token覆盖原先的变量**   
![image](https://user-images.githubusercontent.com/79049368/189658251-062e344e-5fbd-4781-8c4e-0035698bf6fa.png)
   
**保存文件后，重新打开软件即可**
