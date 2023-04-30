# 点击进入“被引用次数”
# 获取：标题、简写作者、期刊、时间、出版商、简写摘要、引用、被引用次数、文献链接
from pyquery import PyQuery as pq 
import requests
import pandas as pd
import json
import os,time
from selenium import webdriver
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def clickButtonByID(driver,id_content_dict,value_dict):
    for id,content in id_content_dict.items():
        elem = driver.find_element_by_id(id)
        is_checked = elem.is_selected()
        if value_dict[content] != is_checked: 
            elem.click()

def clickButtonByCss(driver,css_content_dict,value_dict):
    for css,content in css_content_dict.items():
        if value_dict[content]:
            driver.find_element_by_css_selector(css).click()

driver_path = r'D:\rj\install_rj\PYTHON\chromedriver'
def citeSearch(url,stop_page,sort_dict,article_name):
    # 创建 Chrome 浏览器实例
    driver = webdriver.Chrome(executable_path=driver_path)
    # 访问要抓取的页面
    driver.get(url)
    time.sleep(25)
    # NOTE: 设置排序
    sort_css_content_dict = {"li.gs_ind.gs_bdy_sb_sel":"按相关性排序","li.gs_ind":"按日期排序"}
    clickButtonByCss(driver,sort_css_content_dict,sort_dict)

    # NOTE: 获取内容
    papers_dict = {"标题":[],"简写作者,期刊,时间,出版商":[],"简写摘要":[],"引用":[],"被引用次数":[],"文献链接":[]}
    paper_class_content_dict = {"gs_rt":"标题","gs_a":"简写作者,期刊,时间,出版商","gs_rs":"简写摘要"}
    flag = 1
    page = 1
    # 先到达停止的页面
    while stop_page > page:
        if stop_page-page > 3:
            n = 3
        else:
            n = stop_page-page
        driver.find_element_by_link_text(str(page+n)).click()
        page += n
    try:
        while flag:
            paperItems = driver.find_elements_by_css_selector("div.gs_r.gs_or.gs_scl")
            for paper in paperItems: 
                for classname, content in paper_class_content_dict.items(): 
                    text = paper.find_element_by_class_name(classname).text
                    if text:
                        papers_dict[content].append(text)
                    else:
                        papers_dict[content].append("无")
                    # print(content,text)
                    # 获取被引用次数
                try:
                    cite_time = paper.find_element_by_partial_link_text("被引用次数：")
                    _ = cite_time.text
                    if _:
                        papers_dict["被引用次数"].append(_.split("：")[-1])
                    else:
                        papers_dict["被引用次数"].append("无")
                except:
                    papers_dict["被引用次数"].append("无")
                try:
                    link_item = paper.find_element_by_partial_link_text("[PDF]")
                except:
                    link_item = ""
                if not link_item:
                    try:
                        link_item = paper.find_element_by_partial_link_text("[HTML]")
                    except:
                        link_item = ""
                if link_item:
                    link = link_item.get_attribute('href')
                else:
                    link = "没有链接"

                papers_dict["文献链接"].append(link)
                # print(link)
                # 点击引用
                paper.find_element_by_link_text("引用").click()
                time.sleep(3)
                three_cites = driver.find_elements_by_css_selector("div.gs_citr")
                try:
                    c = three_cites[-1].text
                except:
                    c = "无"
                papers_dict["引用"].append(c)
                time.sleep(2)  
                driver.find_element_by_id("gs_cit-x").click()
            # 获取本页的简写作者链接
            items = driver.find_elements_by_xpath("//div/div/div/div/div/a")
            # 获取下一页
            try:
                driver.find_element_by_link_text("下一页").click()
            except:
                flag = 0
            page += 1
        print("停止的页面：",page)
        max_length = max(len(i) for i in papers_dict.values())
        min_length = min(len(i) for i in papers_dict.values())
        if max_length != min_length:
            for k,v in papers_dict.items():
                papers_dict[k] = v+["补全"]*(max_length-len(v))
    except:
        print("停止的页面：",page)
        # 确保长度都一致
        max_length = max(len(i) for i in papers_dict.values())
        min_length = min(len(i) for i in papers_dict.values())
        if max_length != min_length:
            for k,v in papers_dict.items():
                papers_dict[k] = v+["补全"]*(max_length-len(v))
        df = pd.DataFrame(papers_dict)
        try:
            os.makedirs("cite")
        except:
            pass
    df.to_csv("cite/"+article_name+str(stop_page)+"-"+str(page)+".csv",index=False, encoding='utf-8-sig')


sort_dict = {"按相关性排序":False,"按日期排序":True}
files_list = os.listdir('./')
stop_page = 1
# 如果意外中断，可保存数据
try:
    for file in files_list:
        # 打开 json 文件
        if file[:2]=="引用" and file[-4:]=="json":
            with open(file) as f:
                data = json.load(f)
                for name,link in data.items():
                    print("论文名：",name)
                    citeSearch(link,stop_page,sort_dict,name)
except:
    print("中途中断")
