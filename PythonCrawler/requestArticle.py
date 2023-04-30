# 如果是 arXiv，进入文献链接
from pyquery import PyQuery as pq 
import requests
import pandas as pd
import json
import os

def getContent(content_data,link):
    url = link.replace("pdf","abs")
    # 访问要抓取的页面
    # r = requests.get(url,verify=False,headers={'Host': 'www.example.com'})
    r = requests.get(url,verify=False)
    # r.encoding = "utf-8"
    html = r.text.encode("utf-8")
    doc = pq(html)
    class_content = {".subheader":"学科",".dateline":"当前版本",".authors":"作者",".primary-subject":"主题",".submission-history":"通讯作者+历史版本","blockquote.abstract.mathjax":"摘要"}
    for c,content in class_content.items():
        t = doc(c).text()
        content_data[content].append(t)


    # 确保长度都一致
    max_length = max(len(i) for i in content_data.values())
    min_length = min(len(i) for i in content_data.values())
    if max_length != min_length:
        for k,v in content_data.items():
            content_data[k] = v+["补全"]*(max_length-len(v))


content_data={"标题":[],"学科":[],"当前版本":[],"作者":[],"摘要":[],"主题":[],"通讯作者+历史版本":[]}
files_list = os.listdir('./')
# 如果意外中断，可保存数据
try:
    for file in files_list:
        # 打开 json 文件
        if file[:2]=="文章" and file[-4:]=="json":
            with open(file) as f:
                data = json.load(f)
                for name,link in data.items():
                    content_data["标题"].append(name)
                    getContent(content_data,link)
                    print("论文名：",name)
except:
    print("中途中断")
df = pd.DataFrame(content_data)
df.to_csv("paper_detail.csv",index=False, encoding='utf-8-sig')