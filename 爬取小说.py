# @ Time    : 2020/1/16 20:33
# @ Author  : JuRan

import requests
import re
import time
import random

"""
1 获取小说列表页面源代码
2 获取每章的URL
3 获取每章的HTML
4 通过正则表达式去匹配小说内容
"""

def get_book_content():
    """爬取小说"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
    }
    burl = "http://www.quannovel.com/read/620/"
    cookie_text='UM_distinctid=17b4a0f72af461-0665a00a7196a2-7868786b-e1000-17b4a0f72b095b; CNZZDATA1261853701=1772337853-1629033664-https%3A%2F%2Fwww.baidu.com%2F|1629033664; history=[{art_tit:"我活了几千年",art_url:"http://www.quannovel.com/book/620.htm",chp_tit:"正文 第29章 阴谋",chp_url:"http://www.quannovel.com/read/620/246784.html"}]; PHPSESSID=9e8ec651d88bab9dd88a8afb02366970; jieqi_uv_cookie={"md5":"64b2398967c5cf52999457e0e0b19d38","time":"20210815"}'.encode("utf-8").decode("latin1")
    cookies = {}  # 初始化cookies字典变量
    for line in cookie_text.split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容

    response = requests.get(burl, headers=header,cookies=cookies)
    response.encoding = 'gbk'
    html = response.text
    reg = r'<span class="time">.*?</span>.*?<a href="(.*?)" title=".*?">(.*?)</a></li>'
    # 提高效率
    # pat = re.compile(reg)
    urls = re.findall(reg, html,re.S)
    print(urls)
    i = 1
    for url in urls:
        novel_url, novel_name = url
        chapt = requests.get(r'http://www.quannovel.com/read/620/'+novel_url,cookies=cookies,headers=header)
        chapt.encoding = 'gbk'
        chapt_html = chapt.text

        reg = r'</script>&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<script type="text/javascript">'
        # reg = re.compile(reg, re.S)
        chapt_content = re.findall(reg, chapt_html, re.S)


        # 处理小说内容
        chapt_content = chapt_content[0].replace('&nbsp;&nbsp;&nbsp;&nbsp;', "")
        chapt_content = chapt_content.replace('<br />', "")

        print("正在保存 %s" % novel_name)
        time.sleep(random.random())
        with open("novel/第{}章.txt".format(i), 'w') as f:
            f.write(chapt_content)
        i += 1

if __name__ == '__main__':
    get_book_content()
