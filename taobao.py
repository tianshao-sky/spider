import time

from selenium import webdriver

opt = webdriver.ChromeOptions()
opt.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(chrome_options=opt)

# 窗口最大化
driver.maximize_window()

driver.get('https://login.taobao.com/member/login.jhtml')

# 转账户密码登录
driver.find_element_by_xpath('//div[@class="login-switch"]').click()
time.sleep(1)

# 转微博登录
driver.find_element_by_xpath('//li[@id="J_OtherLogin"]/a[1]').click()
time.sleep(2)

# 输入微博号
driver.find_element_by_name('username').send_keys("微博号")
time.sleep(2)

# 输入微密码
driver.find_element_by_name('password').send_keys("微博密码")
time.sleep(2)

# 点击登录
driver.find_element_by_xpath('//span[@node-type="submitStates"]').click()
time.sleep(2)

# 获得cookie
cookies = driver.get_cookies()
print(cookies)

