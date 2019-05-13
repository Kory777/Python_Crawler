import requests #导入requests 模块
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import random

#这是一个自动爬取 Unplash首页最高高清度图片的脚本
class BeautifulPicture():

    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    ]

    def search(self, path, name):
    #判断该图片是否存在于文件夹，存在的话就不下载了
        for root, dirs, files in os.walk(path):  # path 为根目录
            if name in dirs or name in files:
                flag = 1  # 判断是否找到文件
                root = str(root)
                dirs = str(dirs)
                return os.path.join(root, dirs)
        return -1

    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://unsplash.com'  #要访问的网页地址
        self.folder_path = '/Users/kory/Desktop/bizhi'  #设置图片要存放的文件目录

    def get_pic(self):
        print('开始网页get请求')
        r = self.request(self.web_url)
        base_url = 'https://unsplash.com/'
        print('开始获取所有a标签')
        all_div = BeautifulSoup(r.text, 'lxml').find_all('a', class_='_2Mc8_')#获取网页中的class为2Mc8的所有a标签
        # print('开始创建文件夹')
        self.mkdir(self.folder_path)  #创建文件夹
        # print('开始切换文件夹')
        os.chdir(self.folder_path)   #切换路径至上面创建的文件夹
        i = 1
        for div in all_div:
            url = "https://unsplash.com"+''+div['href']
            namelist = div['href']
            #获取图片的名字
            name = namelist.split('/')[-1]
            if(self.search(self.folder_path, str(name + '.jpg')) == -1):
                req = requests.get(url, headers={'User-Agent': random.choice(self.user_agent_list)})

                soup = BeautifulSoup(req.text, 'lxml').find('div', '_2yFK- IEpfq')
                img = soup.img
                if(img.has_attr('srcset')):
                    srcset = img['srcset']
                    srclist = srcset.split(',')
                    #选择最高清图片的url
                    last = srclist[-1]
                    image_url = last.split(' ')[1]
                    self.save_img(image_url, name)
            else:
                print("This file has exists")


    def save_img(self, url, name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        file_name = name + '.jpg'
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #返回网页的response
        headers = {'User-Agent': random.choice(self.user_agent_list)}
        r = requests.get(url, headers=headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
        else:
            print(path, '文件夹已经存在了，不再创建')

beauty = BeautifulPicture()  #创建类的实例
beauty.get_pic()  #执行类中的方法