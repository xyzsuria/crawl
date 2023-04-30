from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

# 设置代理 IP
proxy = 'http://<proxy_host>:<proxy_port>'
firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
firefox_capabilities['proxy'] = {
    'proxyType': 'manual',
    'httpProxy': proxy,
    'ftpProxy': proxy,
    'sslProxy': proxy
}

# 创建 Firefox Driver
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
browser = webdriver.Firefox(options=firefox_options, desired_capabilities=firefox_capabilities)

# 使用代理访问网站
browser.get('https://www.example.com')

# 关闭浏览器驱动
browser.quit()
