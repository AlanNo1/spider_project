from selenium import webdriver
import time
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class LagouSpider(object):
    def __init__(self):
        self.url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Chrome(options=options)

    def run(self):
        self.driver.get(self.url)
        # 取消页面弹出框
        while True:
            # 获取页面源代码
            sourse = self.driver.page_source
            self.parse_list_page(sourse)

            time.sleep(1)
            next_btn = WebDriverWait(driver=self.driver, timeout=60).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'pager_next')]"))
            )

            # 翻页,点击下一页
            # self.driver.find_element_by_class_name('pager_next ').click()
            # 判断当前页面有没有最后一页的class pager_next pager_next_disabled
            # self.driver.find_element_by_xpath("//span[contains(@class, 'pager_next')]").click()
            if "pager_next pager_next_disabled" in next_btn.get_attribute('class'):
                break
            else:
                # 模糊定位
                next_btn.click()

    def parse_list_page(self, sourse):
        html = etree.HTML(sourse)

        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.requests_detail_page(link)
            time.sleep(1)

    def requests_detail_page(self, link):
        self.driver.get(link)
        sourse = self.driver.page_source
        self.parse_detail_page(sourse)

    def parse_detail_page(self, sourse):
        html = etree.HTML(sourse)
        # data = []
        # job = {}
        job_name = html.xpath("//div[@class='job-name']/h1/text()")[0]
        job_detail = html.xpath("//div[@class='job-detail']/p/text()")
        print(job_name, job_detail)  # [{python,xxxx}]
        # job['job_name'] = job_name


if __name__ == '__main__':
    lg = LagouSpider()
    lg.run()
