# LiZhi-OnlineClassroom-Courseware-Tool  
希沃立知课堂中教师课件自动获取工具，使用Python开发，包括自动下载课件、自动打包课件为enbx等  

## 一、 通过该工具获取课程回放中的课件的方法  
** 1.打开立知课堂官网 **  
<img width="960" alt="捕获1" src="https://user-images.githubusercontent.com/79049368/164376453-89c8591d-0809-4662-af44-d2401bcb70b7.PNG">

**2.打开F12开发者工具，并找到“网络”（如图）**  
<img width="960" alt="捕获2" src="https://user-images.githubusercontent.com/79049368/164376524-cba22c0f-1d55-4f92-ac22-0c7ce0266a7f.PNG">

**3.点击需要获取课件的回放课程（点击“查看回放”按钮），然后等待回放加载完成**  
<img width="960" alt="捕获3" src="https://user-images.githubusercontent.com/79049368/164376678-14b653ca-4421-476b-8af0-47884ae2f532.PNG">

**4.在列表中找到名称中的第一个单词为“detail”的项目，并点击**  
点击后，在右侧的详情栏找到“负载”（如图）  
可以展开“查询字符串参数”（如果已展开，就不需要做这一项操作）  
在展开的数据中找到“accessCode”，然后用鼠标选择冒号后的所有字符，直到这一行结束，然后复制这一段字符  
<img width="617" alt="捕获4" src="https://user-images.githubusercontent.com/79049368/164376800-4f9654a0-0f7d-48ef-a663-9ee915e0b0a8.PNG">

**5.打开程序所在目录（文件夹），并启动程序**  
<img width="485" alt="捕获5" src="https://user-images.githubusercontent.com/79049368/164378133-b4eed9b3-0e3c-444e-845c-e7ae13d039c4.PNG">

**6.在弹出的黑框里的“ACCCESSCODE”后面粘贴刚刚复制的字符串，并按下Enter键**  
<img width="435" alt="捕获6" src="https://user-images.githubusercontent.com/79049368/164378379-72bd5076-68f6-4e99-acfe-3fb78231b38e.PNG">

**7.如果你完美地执行了以上所给的操作，那么就会出现以下界面。**  
提示：程序会执行一段时间（执行时间按照课件大小而定），等到程序界面显示了“===[FINISH]===”后，就会开始打包课件为enbx格式  
打包完毕后，程序会自动关闭。如果你在使用当中关闭了程序，课件将会下载失败！  
<img width="441" alt="捕获7" src="https://user-images.githubusercontent.com/79049368/164379009-620a710f-ce9a-49b9-8f42-d34fded1ac73.PNG">

**8.课件下载完成后，就可以看见软件的目录下出现“Courseware.enbx”，这个文件就是可以用希沃白板直接打开的课件**  
<img width="490" alt="捕获8" src="https://user-images.githubusercontent.com/79049368/164380886-99aa36d4-e4ea-4aac-b84c-772070ba45fa.PNG">
