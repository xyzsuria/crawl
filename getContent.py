from pyquery import PyQuery as pq 
import pandas as pd
import time
from selenium import webdriver
import requests
import datetime
from selenium.webdriver.common.action_chains import ActionChains

# chromedriver.exe 所在的位置，在 python.exe 同级文件夹下
driver_path = r'D:\rj\install_rj\PYTHON\chromedriver'
# 输入要搜索的关键词
def searchKeyWord(url,page_dict):
    for arg, value in page_dict.items():
        print("开始：",datetime.datetime.now())
        print("要搜索的关键词：",arg)
        stop_page = getSearchPage(arg,value,url)
        page_dict[arg] = stop_page
        print(arg,":",stop_page)
        print("结束：",datetime.datetime.now())
    return page_dict

# 获取摘要和关键字
def GetAbstract(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    html = r.text
    doc = pq(html)
    
    abstract = doc(".abstract-text").text()
    key_words = doc(".keywords").text()
    if not abstract:
        abstract = "获取失败"
    if not key_words:
        key_words = "无"
    return abstract,key_words

def getSearchPage(key_word,page_num,url):
    # 创建 Chrome 浏览器实例
    driver = webdriver.Chrome(executable_path=driver_path)
    # 访问要抓取的页面
    driver.get(url)
    # 根据类名定位输入框和按钮
    search_content = driver.find_element_by_class_name("search-input")
    search_button = driver.find_element_by_class_name("search-btn")
    # 在输入框中填写搜索词，点击按钮
    search_content.send_keys(key_word)
    search_button.click()
    # 等待较长的时间
    driver.implicitly_wait(5)
    cur_num = 1
    if page_num != 1:
        while True:
            try:
                driver.find_element_by_id("page"+str(page_num)).click()
                time.sleep(5)
                break
            except:
                cur_num += 3
                driver.find_element_by_id("page"+str(cur_num)).click()
                time.sleep(10)
                # driver.implicitly_wait(2)
    # 分别对应的类名是：name author source date data quote(可能为空)
    data_dict = {"题名":[],"作者":[],"来源":[],"发表时间":[],"数据库":[],"被引":[],"下载":[],"摘要":[],"关键词":[]}
    article_link = {}
    try:
        while True:
            items = driver.find_elements_by_xpath('//tbody/tr')
            for item in items:
                name = item.find_element_by_class_name('name').text
                element = item.find_element_by_class_name('fz14')
                href = element.get_attribute('href')
                article_link[name] = href
                data_dict["题名"].append(name)
                try:
                    author = item.find_element_by_class_name('author').text
                except:
                    author = "无"
                data_dict["作者"].append(author)
                source = item.find_element_by_class_name('source').text
                data_dict["来源"].append(source)
                date = item.find_element_by_class_name('date').text
                data_dict["发表时间"].append(date)
                data = item.find_element_by_class_name('data').text
                data_dict["数据库"].append(data)
                quote = item.find_element_by_class_name('quote').text
                download = item.find_element_by_class_name('download').text
                if not quote:
                    data_dict["被引"].append(0)
                else:
                    data_dict["被引"].append(quote)
                if not download:
                    data_dict["下载"].append(0)
                else:
                    data_dict["下载"].append(download)
                # print("href：",href)
                # print("开始获取摘要：",datetime.datetime.now())
                abstract,key_words = GetAbstract(href)
                data_dict["摘要"].append(abstract)
                data_dict["关键词"].append(key_words)
                # print("获取摘要结束：",datetime.datetime.now())
                
            next_page = driver.find_element_by_id("PageNext")
            actions = ActionChains(driver)
            actions.move_to_element(next_page).click().perform()
            page_num += 1
            # next_page.click()
            time.sleep(5)
    except:
        driver.quit()
        print("点击下一页结束。")
        # print("data_dict:",data_dict)
        for key, value in data_dict.items():
            print(key, len(value))
        # 下面代码保证每个数据的长度一样，避免报错。 
        if len(data_dict["摘要"]) != len(data_dict["题名"]):
            data_dict["摘要"]+=["无"]*(len(data_dict["题名"])-len(data_dict["摘要"]))
            data_dict["关键词"]+=["无"]*(len(data_dict["题名"])-len(data_dict["关键词"]))
        if len(data_dict["发表时间"]) != len(data_dict["题名"]):
            data_dict["发表时间"]+=["无"]*(len(data_dict["题名"])-len(data_dict["发表时间"]))
        if len(data_dict["数据库"]) != len(data_dict["题名"]):
            data_dict["数据库"]+=["无"]*(len(data_dict["题名"])-len(data_dict["数据库"]))
        if len(data_dict["被引"]) != len(data_dict["题名"]):
            data_dict["被引"]+=["无"]*(len(data_dict["题名"])-len(data_dict["被引"]))
        if len(data_dict["下载"]) != len(data_dict["题名"]):
            data_dict["下载"]+=["无"]*(len(data_dict["题名"])-len(data_dict["下载"]))
        df = pd.DataFrame(data_dict)
        df.to_csv(key_word+".csv",index=False, encoding='utf-8-sig')
    return page_num 






url = "https://kns.cnki.net/kns8/defaultresult/index"
# stop_key_page = searchKeyWord(url,{"ChatGPT":1,"大语言模型":1,"人工智能内容生成":1})
# stop_key_page: {'ChatGPT': 6, '大语言模型': 3, '人工智能内容生成': 12}
# stop_key_page = searchKeyWord(url,{"ChatGPT":1,"人工智能内容生成":1})
stop_key_page = searchKeyWord(url,{"ChatGPT":1})
print("stop_key_page:", stop_key_page)
# searchKeyWord(url,"人工智能内容生成")
