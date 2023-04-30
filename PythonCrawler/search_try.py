from pyquery import PyQuery as pq 
import pandas as pd
import time
from selenium import webdriver
import requests
import datetime
import zipfile
import string
import requests
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
def create_proxyauth_extension(proxy_host, proxy_port, proxy_username, proxy_password,scheme='http', plugin_path=None):

    if plugin_path is None:
        plugin_path = '../chrome_proxyauth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def clickButtonByID(driver,id_content_dict,value_dict):
    for id,content in id_content_dict.items():
        elem = driver.find_element_by_id(id)
        is_checked = elem.is_selected()
        if value_dict[content] != is_checked: 
            elem.click()

def clickButtonByClass(driver,class_content_dict,value_dict):
    for classname,content in class_content_dict.items():
        if value_dict[content]:
            driver.find_element_by_class_name(classname).click()

def clickButtonByCss(driver,css_content_dict,value_dict):
    for css,content in css_content_dict.items():
        if value_dict[content]:
            driver.find_element_by_css_selector(css).click()


driver_path = r'D:\rj\install_rj\PYTHON\chromedriver'
def startSearch(url,stop_page,setting_lang_dict,input_dict,sort_dict,radio_dict,include_dict):
    # 创建 Chrome 浏览器实例
    ipurl="http://api.tianqiip.com/getip?secret=x7zymhli1suaooex&num=1&type=txt&port=1&time=3&mr=1"
    sj = requests.get(ipurl).text.strip('\r\n').split(":")
    print(sj)
    co = ChromeOptions()
    co.add_argument("start-maximized")
    # Avoiding detection
    co.add_argument('--disable-blink-features=AutomationControlled')
    co.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"')
    co.add_experimental_option('detach', True)
    co.add_argument('--start-maximized')
    co.add_experimental_option("excludeSwitches", ["enable-automation"])
    co.add_experimental_option('useAutomationExtension', 'False')
    proxyauth_plugin_path = create_proxyauth_extension(
        proxy_username='customer-92d60a',  # 我们是白名单验证和账密验证都支持，如果传的ip在前，会优先走白名单验证，导致走不了账密，所以账密需要写在代理ip前。9iizlh
        proxy_password='b1d14a22',  # lu5aoqh3
        proxy_host='proxy.ipipgo.com',
        proxy_port='31212'
    )
    co.add_extension(proxyauth_plugin_path)
    driver = Chrome(options=co)
    driver.get(url)

    # 访问要抓取的页面
    driver.get(url)
    elem = ""
    while not elem:
        elem = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "gs_hdr_mnu")))
    # driver.implicitly_wait(50)
    # 点击左侧边栏
    driver.find_element_by_id("gs_hdr_mnu").click()
    # 点击设置
    driver.find_element_by_css_selector("a.gs_btnP.gs_in_ib.gs_md_li.gs_md_lix.gs_in_gray").click()
    # time.sleep(25)
    time.sleep(5)
    # NOTE: 点击设置下的语言选项，用于搜索结果选择中文和英文
    driver.find_element_by_id("gs_settings_tab_langs").click()
    lang_id_content_dict = {"gs_settings_lr_all":"所有语言","gs_lr_en":"英文","gs_lr_zh-CN":"中文"}
    # for id,content in lang_id_content_dict.items():
    #     if setting_lang_dict[content]:
    #         driver.find_element_by_id(id).click()
    clickButtonByID(driver,lang_id_content_dict,setting_lang_dict)
    # 点击保存，然后返回
    driver.find_element_by_name("save").click()
    time.sleep(3)
    # 回到左侧边栏
    driver.find_element_by_id("gs_hdr_mnu").click()
    # # 等待指定 ID 元素出现
    # wait = WebDriverWait(driver, 10)
    # elem = wait.until(EC.presence_of_element_located((By.ID, "gs_res_drw_adv")))
    # NOTE: 点击高级搜索
    driver.find_element_by_css_selector("a.gs_btnADV.gs_in_ib.gs_md_li.gs_md_lix.gs_in_gray").click()
    time.sleep(3)    
    input_id_content = {"gs_asd_q":"包含全部字词","gs_asd_epq":"包含完整字句","gs_asd_oq":"包含至少一个字句","gs_asd_eq":"不包含字词","gs_asd_sau":"显示以下作者所著的文章","gs_asd_pub":"显示以下刊物上的文章","gs_asd_ylo":"开始时间","gs_asd_yhi":"结束时间"}
    radio_id_content = {"gs_asd_occt_a":"文章中任何位置","gs_asd_occt_t":"位于文章标题"}
    # 根据输入的dict填写内容
    for id,content in input_id_content.items():
        i = driver.find_element_by_id(id)
        i.send_keys(input_dict[content])
    # for id,content in radio_id_content.items():
    #     if radio_dict[content]:
    #         driver.find_element_by_id(id).click()
    clickButtonByID(driver,radio_id_content,radio_dict)
    # 点击搜索按钮
    driver.find_element_by_class_name("gs_wr").click()
    # 等待 4 秒钟
    time.sleep(4)
    # NOTE: 设置排序
    sort_css_content_dict = {"li.gs_ind.gs_bdy_sb_sel":"按相关性排序","li.gs_ind":"按日期排序"}
    clickButtonByCss(driver,sort_css_content_dict,sort_dict)
    # NOTE: 设置
    for k, v in include_dict.items():
        if (k == "包括专利" and v) or (k=="包括引用" and not v):
            link_elem = driver.find_element_by_link_text(k)
            link_elem.click()

    # NOTE: 获取内容
    papers_dict = {"标题":[],"简写作者,期刊,时间,出版商":[],"简写摘要":[],"引用":[],"被引用次数":[],"文献链接":[]}
    paper_class_content_dict = {"gs_rt":"标题","gs_a":"简写作者,期刊,时间,出版商","gs_rs":"简写摘要"}
    # artile:link
    article_dict = {}
    # article:cite link
    cite_link_dict = {}
    # writer:link
    writer_link_dict = {}
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
                    cite_link_dict[papers_dict["标题"][-1]] = cite_time.get_attribute('href')
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

                if "arxiv.org" in link:
                    article_dict[papers_dict["标题"][-1]]=link
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
            for i in items:
                writer_link_dict[i.text]=i.get_attribute('href')
                print("作者：",i.text)
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
        df = pd.DataFrame(papers_dict)
        df.to_csv("gpt.csv",index=False, encoding='utf-8-sig')
        return  article_dict,cite_link_dict,writer_link_dict
    except:
        print("停止的页面：",page)
        # 确保长度都一致
        max_length = max(len(i) for i in papers_dict.values())
        min_length = min(len(i) for i in papers_dict.values())
        if max_length != min_length:
            for k,v in papers_dict.items():
                papers_dict[k] = v+["补全"]*(max_length-len(v))
        df = pd.DataFrame(papers_dict)
        df.to_csv("gpt_"+str(stop_page)+"-"+str(page)+".csv",index=False, encoding='utf-8-sig')
        return  article_dict,cite_link_dict,writer_link_dict
    



# TODO: 获取文献要素
# 如果是 arXiv,则进入文献链接
def getDetail(article_dict):
    for i in article_dict:
        print(i)

def SaveJson(name,data):
    with open(name+".json","w") as f:
        json.dump(data,f)



# TODO: 引注文献
# 从 cite_link_dict 中获取

googleScholarUrl = "https://scholar.google.com/?hl=zh-CN"
# googleScholarUrl = "https://baidu.com"
start_page = 1
radio_dict = {"文章中任何位置":True,"位于文章标题":False}
setting_lang_dict = {"所有语言":True,"英文":True,"中文":True}
input_dict = {"包含全部字词":"gpt","包含完整字句":"","包含至少一个字句":"","不包含字词":"","显示以下作者所著的文章":"","显示以下刊物上的文章":"","开始时间":"","结束时间":""}
sort_dict = {"按相关性排序":False,"按日期排序":True}
include_dict = {"包括专利":True,"包括引用":True}
article_dict,cite_link_dict,writer_link_dict = startSearch(googleScholarUrl,start_page,setting_lang_dict,input_dict,sort_dict,radio_dict,include_dict)
SaveJson("文章—链接"+str(start_page),article_dict)
SaveJson("引用—链接"+str(start_page),cite_link_dict)
SaveJson("作者—链接"+str(start_page),writer_link_dict)