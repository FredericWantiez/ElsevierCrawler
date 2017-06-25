from selenium import webdriver

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.javascriptEnabled"] = True
cap["phantomjs.page.settings.loadImages"] = True
cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

driver = webdriver.PhantomJS(desired_capabilities=cap)
driver.set_window_size(1120, 550)
driver.set_page_load_timeout(15)
driver.get("http://www.sciencedirect.com/science/article/pii/S0165168400001419")
mail_links = driver.find_elements_by_xpath('//a[*/span[contains(@class, "Icon Email")]]')
emails = list()
for elem in mail_links:
    elem.click()
    email = driver.find_element_by_xpath('//ul[@class="author-emails"]/li/a')
    tmp = email.get_attribute("href")
    emails.append(tmp.split(":")[-1])
print(emails)
driver.quit()

