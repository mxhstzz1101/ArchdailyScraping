#!python3
#coding:utf-8

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import urllib.request,time,socket,wget
from urllib.error import (
    HTTPError,
    URLError,
    ContentTooShortError
    )
# www.archdaily.com/800780/sunken-bath-project-studio-304-architecture
# 输入Archdaily项目网址
project_url = input('请输入Archdaily项目网址:')
# project_url = r'http://www.archdaily.com/800780/sunken-bath-project-studio-304-architecture'
# usr_url = 'http://' + project_url

# 获取需要下载的原始图片URL
soup = urlopen(project_url,timeout = 15)
Project_bs = BeautifulSoup(soup.read(), 'lxml')
pic_gallery = Project_bs.findAll('a',class_="gallery-thumbs-link")
pics_url = []
for i in pic_gallery:
    pics_url.append(i.img['data-src'].replace('thumb_jpg','large_jpg'))
    #print(i.img['data-src'], end='\n')

print('项目原图总数： ' + str(len(pics_url)) + '张')

# 定义创建项目文件夹目录函数
# 参考：http://www.qttc.net/201209207.html
def mkdir(path):
    import os
    # 去除首位空格
     #path = path.strip()
    # 去除尾部 \ 符号
     #path = path.retrip('\\')

    # 判断路径是否存在
    # 存在    True
    # 不存在  False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print (path+'目录创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+'目录已存在')
        return False


# 定义要创建的目录
# mkpath
# mkdir(mkpath)
project_name = Project_bs.find('h1', {"class": "afd-title-big afd-title-big--bmargin-small afd-relativeposition"}).get_text()
# 去除项目名称中的特殊字符
  # 去除首位空格
project_name = project_name.strip()
  # 去除特殊字符
#from string import maketrans
intab = ' /+'
outtab = '___'
trantab = project_name.maketrans(intab,outtab)
project_name = project_name.translate(trantab)
#print (project_name)
# 获取脚本所在文件夹//os.getcwd()
downloadDir = os.getcwd() + '\\Archdaily\\'
project_Dir = downloadDir + project_name
#调用自定义函数'mkdir'创建项目文件夹
print ('创建项目文件夹：' + project_Dir)
mkdir(project_Dir)
# filename = 'pic_' + '.jpg'
# print(project_Dir + '\\' + filename)


# 定义显示下载文件进度函数
# 参考：http://www.aichengxu.com/view/4955140
def Schedule(a,b,c):
  per = 100.0*a*b/c
  if per > 100:
      per = 100
  print ('%d%%' % per)


# 定义图片下载函数
def get_1(url,repeat = 3):
    index = 1
    total_num = 0
    url_fail = []
    socket.setdefaulttimeout(100)
    # 设置休眠时间
    sleep_download_time = 10
    for i in url:
        print('正在下载第 '+str(index)+' 个图片')
        time.sleep(sleep_download_time)
        # req = urllib.request.Request(url=i, headers=user_headers)
        try:
            filename = 'pic_' + str(index) + '.jpg'
            filepath = project_Dir + '\\' + filename
            urlretrieve(i, filepath,Schedule)
        except (HTTPError,URLError) as e:
            print('错误代码： %s' % e)
            print('图片下载错误，稍后自动重试')
            index += 1
            url_fail.append(i)
        except (ContentTooShortError) as e:
            print('错误代码： %s' % e)
            print('图片下载错误，稍后自动重试')
            index += 1
            url_fail.append(i)
        except socket.timeout as e:
            print('错误代码： %s' % e)
            print('图片下载错误，稍后自动重试')
            index += 1
            url_fail.append(i)
        else:
            index += 1
            total_num += 1
    print('完成下载图片数量: ' + str(total_num))
    print('下载失败链接数量：' + str(len(url_fail)))



def get_2(url,n=0):
    print('开始执行下载函数')
    # 设置全局超时时间
    timeout = 20
    socket.setdefaulttimeout(timeout)
    # 设置休眠时间
    sleep_download_time = 5
    # 初始化计数器
    index = 1
    # 添加'User-Agent'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    user_headers = {'Connection':'keep-alive',
                    'Host':'images.adsttc.com',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate, sdch',
                    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        }
    url_fail = []
    for i in url:
        req = urllib.request.Request(url=i, headers=user_headers)

        try:
            time.sleep(sleep_download_time)
            imgurl = urlopen(req)
            jpgpic = imgurl.read()
            imgurl.close()
        except (HTTPError, URLError) as e:
            print('错误代码： %s' % e)
            print('图片下载错误，稍后自动重试')
            index += 1
            url_fail.append(i)
        except socket.timeout as e:
            print('错误代码： %s' % e)
            print('图片下载错误，稍后自动重试')
            index += 1
            url_fail.append(i)
        else:
            filename = 'pic_' + str(n) + '_' + str(index) + '.jpg'
            imgfile = open(project_Dir + '\\' + filename, 'wb')
            print('Downloading: ' + '\\' + 'pic_' + str(index) + '.jpg')
            imgfile.write(jpgpic)
            imgfile.close()
            index += 1
    print('Total pics: '+str(index))
    print('下载失败链接数量： ' + str(len(url_fail)))


def get_3(url):
    index = 1
    for i in url:
        filename = 'pic_' + str(index) + '.jpg'
        filepath = project_Dir + '\\' + filename
        file = wget.download(i,filepath)
        index += 1
        print(filename+'下载完毕')
        time.sleep(3)



# get_1(pics_url)
# get_2(pics_url)
get_3(pics_url)
print('项目原图下载完毕')
input(r"按'回车键'退出!")
