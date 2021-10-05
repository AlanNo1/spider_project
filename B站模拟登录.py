# @ Time    : 2020/4/2 20:36
# @ Author  : JuRan
"""
找到张图图片
1.有缺口的图片
2.没有缺口的图片
3.截图两张图片
4.做对比,得到差异的像素位置
5.移动鼠标去滑块
"""

from selenium import webdriver
from io import BytesIO
import time
from PIL import Image
import random
from selenium.webdriver.common.action_chains import ActionChains


class BibiLogin(object):
    url = "https://passport.bilibili.com/login"

    def __init__(self):
        self.user_name = "13125104933"
        self.pass_wrod = "fls@132302007"
        self.driver = webdriver.Chrome()

    def crop_image(self, image_file_name):
        time.sleep(1)
        img = self.driver.find_element_by_class_name("geetest_canvas_img")
        # {'x': 1078, 'y': 283}
        location = img.location
        # print(location)
        size = img.size

        x1, y1 = location["x"], location["y"]
        x2, y2 = location["x"] + size["width"], location["y"] + size["height"]

        screen_shot = self.driver.get_screenshot_as_png()
        screen_shot = Image.open(BytesIO(screen_shot))

        captcha = screen_shot.crop((int(x1), int(y1), int(x2), int(y2)))
        captcha.save(image_file_name)
        return captcha

    def compare_pixel(self, image1, image2, i, j):
        pixel1 = image1.load()[i, j]
        pixel2 = image2.load()[i, j]
        threashold = 72
        # RGB
        if abs(pixel1[0] - pixel2[0]) < threashold and abs(pixel1[1] - pixel2[1]) < threashold and abs(pixel1[2] - pixel2[2]) < threashold:
            return True
        else:
            return False

    def check_login(self):
        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'创作中心')]")
            return True
        except Exception as e:
            return False


    def login(self):
        # 全屏浏览器
        try:
            self.driver.maximize_window()
        except Exception as e:
            pass

        while not self.check_login():
            # 打开浏览器
            self.driver.get(self.url)
            # 填写账号密码
            self.driver.find_element_by_id("login-username").send_keys(self.user_name)
            self.driver.find_element_by_id("login-passwd").send_keys(self.pass_wrod)

            # 点击登陆 弹出滑块验证码
            self.driver.find_element_by_class_name("btn-login").click()
            # self.driver.find_element_by_css_selector(".btn.btn-login")
            time.sleep(3)

            # 执行JS改变css样式
            self.driver.execute_script("document.querySelectorAll('canvas')[3].style=''")

            # 截取图片
            image1 = self.crop_image("captcha1.png")

            # 执行JS改变css样式
            self.driver.execute_script("document.querySelectorAll('canvas')[3].style='display: none;'")

            image2 = self.crop_image("captcha2.png")

            # 开始对比
            left =72#缺陷大小
            has_find = False

            for i in range(72, image1.size[0]):
                if has_find:
                    break
                for j in range(image1.size[1]):
                    if not self.compare_pixel(image1, image2, i, j):
                        left = i
                        has_find = True
                        break
            left -= 15

            # 移动滑块
            # 移动轨迹
            track = []
            # 当前位置
            current = 0
            # 减速值
            mid = left * 3/4
            # 时间
            t = 0.1
            v = 0

            while current < left:
                if current < mid:
                    a = random.randint(2, 3)
                else:
                    a = - random.randint(7, 8)

                v0 = v
                v = v0 + a*t
                # 移动距离   位移 = 初速度*时间 + 1/2*加速度*时间的平方
                move = v0*t + 1/2 * a*t*t

                current += move
                track.append(round(move))

            # 移动
            slider = self.driver.find_element_by_class_name("geetest_slider_button")
            # click_and_hold 点击按住
            ActionChains(self.driver).click_and_hold(slider).perform()

            for x in track:
                ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.5)
            # 松开鼠标
            ActionChains(self.driver).release().perform()
            time.sleep(2)
            # 打开浏览器
            self.driver.get(self.url)
            # 填写账号密码
            self.driver.find_element_by_id("login-username").send_keys(self.user_name)
            self.driver.find_element_by_id("login-passwd").send_keys(self.pass_wrod)

            # 点击登陆 弹出滑块验证码
            self.driver.find_element_by_class_name("btn-login").click()
            # self.driver.find_element_by_css_selector(".btn.btn-login")
            time.sleep(3)

            # 执行JS改变css样式
            self.driver.execute_script("document.querySelectorAll('canvas')[3].style=''")

            # 截取图片
            image1 = self.crop_image("captcha1.png")

            # 执行JS改变css样式
            self.driver.execute_script("document.querySelectorAll('canvas')[3].style='display: none;'")

            image2 = self.crop_image("captcha2.png")

            # 开始对比
            left = 60
            has_find = False

            for i in range(60, image1.size[0]):
                if has_find:
                    break
                for j in range(image1.size[1]):
                    if not self.compare_pixel(image1, image2, i, j):
                        left = i
                        has_find = True
                        break
            left -= 6

            # 移动滑块
            # 移动轨迹
            track = []
            # 当前位置
            current = 0
            # 减速值
            mid = left * 3 / 4
            # 时间
            t = 0.1
            v = 0

            while current < left:
                if current < mid:
                    a = random.randint(2, 3)
                else:
                    a = - random.randint(7, 8)

                v0 = v
                v = v0 + a * t
                # 移动距离   位移 = 初速度*时间 + 1/2*加速度*时间的平方
                move = v0 * t + 1 / 2 * a * t * t

                current += move
                track.append(round(move))

            # 移动
            slider = self.driver.find_element_by_class_name("geetest_slider_button")
            # click_and_hold 点击按住
            ActionChains(self.driver).click_and_hold(slider).perform()

            for x in track:
                ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.5)
            # 松开鼠标
            ActionChains(self.driver).release().perform()
            time.sleep(2)


if __name__ == '__main__':
    bibi = BibiLogin()
    bibi.login()


