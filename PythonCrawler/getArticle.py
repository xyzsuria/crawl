# 如果是 arXiv，进入文献链接
import json
import os
from selenium import webdriver
import pandas as pd
# files_list = os.listdir('./')
# for file in files_list:
#     if file[:2]=="文章" and file[-4:]=="json":
#         print(file)
# with open("文章—链接1.json") as f:
#     data = json.load(f)
# print(data)

link = 'https://arxiv.org/pdf/2107.01294'
url = link.replace("pdf","abs")
driver_path = r'D:\rj\install_rj\PYTHON\chromedriver'
# 创建 Chrome 浏览器实例
driver = webdriver.Chrome(executable_path=driver_path)
# 访问要抓取的页面
driver.get(url)
content_data={"学科":[],"当前版本":[],"作者":[],"摘要":[],"主题":[],"通讯作者":[],"历史版本":[]}
class_content = {"subheader":"学科","dateline":"当前版本","authors":"作者","primary-subject":"主题","submission-history":"通讯作者+历史版本"}
css_content = {"摘要":"blockquote.abstract.mathjax"}
for c,content in class_content.items():
    t = driver.find_element_by_class_name(c).text
    content_data[content].append(t)
for c,content in css_content.items():
    t = driver.find_element_by_css_selector(c).text()
    content_data[content].append(t)

# 确保长度都一致
max_length = max(len(i) for i in content_data.values())
min_length = min(len(i) for i in content_data.values())
if max_length != min_length:
    for k,v in content_data.items():
        content_data[k] = v+["补全"]*(max_length-len(v))
df = pd.DataFrame(content_data)
df.to_csv("paper_detail.csv",index=False, encoding='utf-8-sig')