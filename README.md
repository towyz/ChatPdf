# myChatPDFHelper
 
## 1. About This Repo

本仓库是一个基于 [ChatPDF](https://www.chatpdf.com/) 平台提供的 API 编写的一个**论文助手的 demo**，很多功能比较粗糙，但是可以基本满足正常情况下 API 的调用。

项目后端基于 flask 框架，作者不会前端，知识很简陋地展示了一下子🤔 一些辅助功能需要在 notebook 里打开进行操作。

## 2. How to Use

### vscode.bat 文件:
这个批处理文件是作者打开自己 VS Code 用的，包括配置代理啥的，如果你也用的是 VS Code，那就可以：
1. 修改一下代理的端口号（找找你的🪜，一般都会在很显眼的位置指明端口号的）:
`SET HTTP_PROXY=http://127.0.0.1:XXXX`
`SET HTTPS_PROXY=http://127.0.0.1:XXXX`
2. 修改你的 VSCode 路径（以D盘根目录为例），或者直接删掉这两行:
`cd "D:\Microsoft VS Code"`
`start Code.exe`

之后，用这个批处理打开你的 IDE 了。

### settings 文件夹：
这个文件夹下面应该有两个 json 文件，得自己创建：
1. API_KEY.json:
这里面装的是你的 API KEY，自个儿从网站上复制🧐，格式如下：
`{
    "ChatPDF_API": "sec_balabala_aba_ABA"
}`
2. pdf.source.json:
这里面装的是你的每一个 PDF 上传后对应的一个 ID，**新建的时候**要保证里面有一个：
`{}`

### 在 notebooks 中上传新的 PDF：
找到 test_api.ipynb 中第一个 cell 里面的 path_to_pdf 变量，这里改成你要上传的 PDF 的路径，传一次就得改一次，嘻嘻主要是懒得写了🤣：
`path_to_pdf = "D://path//to//your//file.pdf"`
然后，运行这个 cell ，当然，记得导前面的包~

### 运行 app.py 进行选择＋提问：
后续就是在网页上进行问答了，可以搭配 edge 的分屏功能，大概是这样：
![示例](/img/example.jpg)

## 3. 写得不好，别骂我