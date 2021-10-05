import requests
from lxml import etree
from urllib import request
import threading
from queue import Queue


class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Host': 'www.doutula.com',
        'Cookie': '__cfduid=d0482fd98715b92c3742dd452c58abe991582206241; UM_distinctid=17062d74e572d0-06f72cf9e39479-2393f61-1fa400-17062d74e595e0; CNZZDATA1256911977=1187705542-1582204806-%7C1582204806; _ga=GA1.2.188432079.1582206243; _gid=GA1.2.321283468.1582206243; __gads=ID=b074b5de9483e3e6:T=1582206242:S=ALNI_MY0LJl_kXttlOHBqkHIVODQTtkVmQ; _agep=1582206244; _agfp=698bc2e12789df094f2cdcc72a7f6225; _agtk=e92fbe464dff15783076bd9190dd965b; XSRF-TOKEN=eyJpdiI6IktrNHNhRUdBNDNtbENxOU5TdnBZUXc9PSIsInZhbHVlIjoiVTE5eVZTbWdTNTJyRmJwdnBcLzhieVlSb2YzMFNjQlNzMEN6YlNiSXJ0NXpBNnA3YjNwcUxNTFFGdEpjbWRDenUiLCJtYWMiOiI0MWFjYzRkN2RlYjMwNDI0OWI2YTc0Y2VhNjQ4ZTkyNGZkOGFmYmU4YTk5ZTUzNzU4M2FhYjMzMzEzOTk3MWZlIn0%3D; doutula_session=eyJpdiI6InRaa09IWis4K0Jic2pIdm9tNnlJWUE9PSIsInZhbHVlIjoianc5QUV4WGYrMFA1R2g1S3pNU2tGU2g5b1RPVG8yaDEwenRuXC9Vdk8rZW5MN0dqbTNNSUpsWjVIMmhDWHJPcjkiLCJtYWMiOiI0OTUxZDQxMThmMmFhMDcyZDAwZGYxNGViY2JhOGQ3Mjg0MzY0MDgxNjExMTE5NGQ3NmYwMGEwNTYzMDM3MDEwIn0%3D'
    }

    def __init__(self, page_queue, img_queue):
        super().__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img")
        # print(imgs)
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            # request.urlretrieve(img_url, 'images/{}.jpg'.format(alt))
            # print("正在下载-{}".format(alt))
            # print(img_url, alt)
            self.img_queue.put((img_url, alt))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue):
        super().__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:

            if self.page_queue.empty() and self.img_queue.empty():
                break

            img = self.img_queue.get()
            print(img)
            img_url, filename = img
            print(img_url)
            request.urlretrieve(img_url, 'images/{}.jpg'.format(filename))
            print("正在下载-{}".format(filename))


def main():
    page_queue = Queue(100)
    img_queue = Queue(500)
    for page in range(1, 101):
        url = 'http://www.doutula.com/photo/list/?page={}'.format(page)
        # parse_page(url)
        page_queue.put(url)
        # break

    for i in range(5):
        t = Producer(page_queue, img_queue)
        t.start()

    for i in range(5):
        # print('juran')
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()