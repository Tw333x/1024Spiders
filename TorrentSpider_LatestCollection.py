#!/usr/bin/python3
#-*-coding:utf-8 -*-
import _thread
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, parse_qs, urlsplit, urlunsplit
from urllib.request import urlretrieve
import urllib.request
import os
import time


# 1024 http request header
# 1024 网站请求头
proxt_1024_req_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    # 'Connection': 'keep - alive',
    'Cookie': '__cfduid=d7e5c699ef4d6599ef01239424b0e6cd71547705542; aafaf_lastvisit=0%09154' \
              '7705542%09%2Fpw%2Findex.php%3F; UM_distinctid=1685a707030539-0653970bbabd2b-46564b55' \
              '-1fa400-1685a707031a0a; CNZZDATA1261158850=317005769-1547705297-%7C1547705297',
    'Host': 'w3.jbzcjsj.pw',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    #'Referer': 'http://w3.afulyu.pw/pw/thread.php?fid=17&page=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                  '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116'
}
request_header = proxt_1024_req_header

# magnet-link website http request header
# 磁力链接网站网站请求头
proxt_torrent_req_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    # 'Connection': 'keep - alive',
    'Cookie': '__cfduid=d062c450fc125c2a02de05db8586dc1941547731587; UM_distinctid=1685bfdd4' \
              'd4854-0edeecf536f3fc-46564b55-1fa400-1685bfdd4d515b4; CNZZDATA1273152310=651528679' \
              '-1547731013-http%253A%252F%252Fw3.jbzcjsj.pw%252F%7C1547731013; _ga=GA1.2.845482462.' \
              '1547731588; _gid=GA1.2.2026642011.1547731588',
    'Host': 'www1.downsx.club',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://w3.jbzcjsj.pw/pw/html_data/3/1901/3855151.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
              '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116'
}
torrent_request_header = proxt_torrent_req_header
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
                  ' (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116')]
urllib.request.install_opener(opener)

# proxy settings
# 代理设置
proxies = {'http': '127.0.0.1:1080', "https": "127.0.0.1:1080", }
proxies_header = proxies
isProxy = False                                          # 是否设置代理

base_url = "http://w3.jbzcjsj.pw/pw/"                # 基础url
save_path = "D:/code/Pycharm/1024Spider/torrent"   # 存储图片路径
fid = 3                                                  # fid=3 表示最新合集
page_start = 1                                           # 爬取的开始页
page_end = 245                                           # 爬取的结束页
thread_num = 1                                           # 线程数


# conversion encode
# 转换编码
def Encode_Conversion(req):
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        return encode_content
    else:
        return ""


# save [content] to [path]
# 保存文本
def Save_Text(id, path, content):
    try:
        f = open(path, "w", encoding='utf-8')
        f.write(content)
    except IOError:
        print("[" + str(id) + "] IOError: File open failed.")
    except Exception as e:
        print("Save_Text Exception: " + str(e))
    else:
        # 内容写入文件成功
        print("[" + str(id) + "] Successfully save the file to " + path)
        f.close()


# torrent and magnet-link page
# 种子/磁力链接页面
def Prase_Torrent(id, url, folder_path):
    try:
        if (isProxy == True):
            req = requests.get(url, params=torrent_request_header, proxies=proxies_header)
        else:
            req = requests.get(url, params=torrent_request_header)

        # soup转换
        soup = BeautifulSoup(req.content, "html.parser")

        torrent_content = soup.select('.uk-button ')
        torrent_content_num = len(torrent_content)
        if torrent_content_num == 0:
            print("[" + str(id) + "] No match torrent.")
            return
        for content in torrent_content:
            str_content = str(content)
            # 匹配磁力链接
            matchObj = re.search(r'magnet(.*?)"', str_content)
            if matchObj:
                magnet_link = 'magnet' + matchObj.group(1)
                urlTemp = url
                strlist = urlTemp.split('/')
                strlen = len(strlist)
                if strlen != 0:
                    torrent_name = strlist[strlen - 1]
                    if torrent_name != "":
                        savePath = folder_path + "/" + str(torrent_name).replace(u'\0', u'').replace(u'\t',
                                                                                                      u'') + ".txt"
                        Save_Text(id, savePath, magnet_link)
            else:
                # 匹配失败
                print("[" + str(id) + "] No match: " + str_content)
    except Exception as e:
        print("[" + str(id) + "] Prase_Torrent Exception: " + str(e))


# each post page
# 每个帖子页面
def Prase_Post(id, url, folder_name):
   try:
       if (isProxy == True):
           req = requests.get(url, params=request_header, proxies=proxies_header)
       else:
           req = requests.get(url, params=request_header)

       # 转换编码
       encode_content = Encode_Conversion(req)
       # soup转换
       soup = BeautifulSoup(encode_content, "html.parser")

       post_content = soup.select('div[id="read_tpc"]')
       post_content_num = len(post_content)
       if post_content_num == 0:
           print("[" + str(id) + "] No match post.")
           return

       # 创建保存的文件夹
       folder_path = save_path + '/' + folder_name
       folder = os.path.exists(folder_path)
       if not folder:
           os.makedirs(folder_path)
           print("[" + str(id) + "] Created folder " + folder_name)

       # 保存文本内容
       result = post_content[0].text
       Save_Text(id, folder_path + '/index.txt', result)
       for content in post_content:
           str_content = str(content)

           # 匹配种子
           matchObj = re.findall(r'href="(.*?)"', str_content)
           if matchObj:
               for obj in matchObj:
                   Prase_Torrent(id, obj, folder_path)
           else:
               # 匹配失败
               print("[" + str(id) + "] No match: " + str_content)

           # 匹配图片
           matchObj = re.findall(r'window.open\(\'(.*?)\'\);', str_content)
           if matchObj:
               for obj in matchObj:
                   objTemp = obj
                   strlist = objTemp.split('/')
                   strlen = len(strlist)
                   if strlen != 0:
                       img_name = strlist[strlen - 1]
                       try:
                            urllib.request.urlretrieve(obj, folder_path + '/' + img_name)
                       except Exception as e:
                            print("[" + str(id) + "] Download the picture Exception: " + str(e))
                       else:
                           print("[" + str(id) + "] Successfully save the image to " + folder_path + '/' + img_name)
           else:
               # 匹配失败
               print("[" + str(id) + "] No match: " + str_content)
   except Exception as e:
       print("[" + str(id) + "] Prase_Post Exception: " + str(e))


# post list page
# 帖子列表页面
def Post_list(id, page):
    try:
        post_url = base_url + 'thread-htm-fid-' + str(fid) + '-page-' + str(page) + '.html'
        print('[' + str(id) + '] clicked: ' + post_url)

        if (isProxy == True):
            req = requests.get(post_url, params=request_header, proxies=proxies_header)
        else:
            req = requests.get(post_url, params=request_header)

        # 转换编码
        encode_content = Encode_Conversion(req)

        # soup转换
        soup = BeautifulSoup(encode_content, "html.parser")
        # 获取帖子名称
        post_list = soup.select('tr[class="tr3 t_one"] h3 a')
        post_num = len(post_list)
        if post_num == 0:
            print("[" + str(id) + "] No match post_list.")
            return
        for post in post_list:
            str_post = str(post)
            # 帖子网页的匹配
            matchObj = re.match(r'(.*)href="(.*)" id=(.*)>(.*?)</a>', str_post, re.M | re.I)
            if matchObj:
                post_url = matchObj.group(2)  # URL
                post_name = matchObj.group(4)  # 文件夹名
                if post_name != '':
                    # 匹配每个帖子
                    Prase_Post(id, base_url + post_url,
                               post_name.replace(u'\0', u'').replace(u'/', u'.').replace(u'?',
                                                                                         u'').replace(u'*',
                                                                                                      u''))
            else:
                # 匹配失败
                print("[" + str(id) + "] No match: " + str_post)
    except Exception as e:
        print("[" + str(id) + "] Post_list Exception." + str(e))


# multi-threaded, the parameter [id] is the thread id
# 多线程，参数 [id] 为线程 id
def Work_thread(id):
    try:
        if id <= page_end:
            prase_num = 0
            prase_more_one = 0
            page_num = abs(page_end - page_start) + 1
            if id <= int(page_num % thread_num):
                prase_more_one = 1
            page_num_each_thread = int(page_num / thread_num) + prase_more_one
            for each_page in range(page_start + id - 1, page_end + 1, thread_num):
                Post_list(id, each_page)
                prase_num += 1
                print('[' + str(id) + '] [ ' + "{:.1f}".format(
                    prase_num / page_num_each_thread * 100) + '% page completed ] ')
            print('[' + str(id) + '] completed !!!!!')
    except Exception as e:
        print("[" + str(id) + "] Work_thread Exception." + str(e))


if __name__ == "__main__":
    # single thread # 单线程
    # Work_thread(1)
    # multithreading # 多线程
    try:
        for i in range(1, thread_num + 1):
            _thread.start_new_thread(Work_thread, (i,))
    except Exception as e:
        print("Start_new_thread Exception: " + str(e))
    while 1:
        pass
