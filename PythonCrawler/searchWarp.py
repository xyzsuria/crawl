from warp import WarpedBrowser
browser = WarpedBrowser()
browser.open("https://www.baidu.com/")
input_box = browser.find_element_by_css_selector('#kw')
input_box.send_keys('warp 自动化测试')
search_button = browser.find_element_by_css_selector('#su')
search_button.click()

browser.wait_for_page_to_load(10)
results = browser.find_elements_by_css_selector('.result h3 a')
for result in results:
    print(result.text)
    print(result.get_attribute('href'))
browser.quit()
