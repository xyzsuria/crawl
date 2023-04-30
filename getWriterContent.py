
# 如果是 arXiv，进入文献链接
from pyquery import PyQuery as pq 
from selenium import webdriver
import requests
import pandas as pd
import json,time
import os

# 获取作者的 姓名，简洁，电子邮箱，研究领域；
# 标题、引用次数、年份、引用信息
# 保存的数据格式 {"姓名":[],"简介":[],"电子邮箱":[],"研究领域":[],"相关数据":[{"标题":[],"引用次数":[],"年份":[],"引用信息":[]}]}
driver_path = r'D:\rj\install_rj\PYTHON\chromedriver'
def writerSearch(url,content_data):
    # 创建 Chrome 浏览器实例
    driver = webdriver.Chrome(executable_path=driver_path)
    # 访问要抓取的页面
    driver.get(url)
    time.sleep(25)
    # 点击展开
    try:
        driver.find_element_by_id("gsc_bpf_more").click()
    except:
        pass
    relate_data = {"标题":[],"引用次数":[],"年份":[],"引用信息":[]}
    # 访问要抓取的页面
    # r = requests.get(url,verify=False)
    # html = r.text.encode("utf-8")
    # doc = pq(html)
    class_content = {"gsc_prf_il":"简介"}
    id_content = {"gsc_prf_in":"姓名","gsc_prf_ivh":"电子邮箱","gsc_prf_int":"研究领域"}
    for k,v in class_content.items():
        _ = driver.find_element_by_class_name(k).text
        content_data[v].append(_)
    for k,v in id_content.items():
        _ = driver.find_element_by_id(k).text
        content_data[v].append(_)
    cite_tr_class = "gsc_a_tr" 
    cite_info_class = {"gsc_a_at":"标题","gsc_a_y":"年份"}
    cite_info_css = {"gsc_a_ac gs_ibl":"引用次数"}
    cite_infos_class = {"gs_gray":"引用信息"}
    cite_divs = driver.find_elements_by_class_name(cite_tr_class)
    for i in cite_divs:
        for k,v in cite_info_class.items():
            _ = i.find_element_by_class_name(k).text
            relate_data[v].append(_)
        for k,v in cite_info_class.items():
            _ = i.find_element_by_css_selector(k).text
            relate_data[v].append(_)        
        # 该 class 下有两条数据
        i_d = ""
        for k,v in cite_infos_class.items():
            items = _ = i.find_elements_by_class_name(k)
            for item in items:
                i_d += item.text+" "
            relate_data[v].append(i_d)
        content_data["相关数据"].append(relate_data)

    # 确保长度都一致
    max_length = max(len(i) for i in content_data.values())
    min_length = min(len(i) for i in content_data.values())
    if max_length != min_length:
        for k,v in content_data.items():
            content_data[k] = v+["补全"]*(max_length-len(v))


content_data= {"姓名":[],"简介":[],"电子邮箱":[],"研究领域":[],"相关数据":[]}
url = "https://scholar.google.com/citations?user=_VmflIEAAAAJ&hl=zh-CN&oi=sra"
writerSearch(url,content_data)
# files_list = os.listdir('./')
# 如果意外中断，可保存数据
# try:
#     for file in files_list:
#         # 打开 json 文件
#         if file[:2]=="文章" and file[-4:]=="json":
#             with open(file) as f:
#                 data = json.load(f)
#                 for name,link in data.items():
#                     content_data["标题"].append(name)
#                     getContent(content_data,link)
#                     print("论文名：",name)
# except:
#     print("中途中断")
# df = pd.DataFrame(content_data)
# df.to_csv("paper_detail.csv",index=False, encoding='utf-8-sig')