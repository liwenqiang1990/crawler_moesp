from bs4 import BeautifulSoup
import requests
import re
import html.parser
import pdfkit
import os
import time

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<table>
<tr>
{content}
</tr>
</table>
</body>
</html>
"""


base_url = 'http://onsgep.moe.edu.cn/edoas2/website7/level2.jsp?infoid=1335254564530193&firstnum={firstnum}&maxnum=40&curpage={curpage}'


def get_url_list(base_url):
    """
    获取网页内容
    :param url:  基础url
    :return: 列表，元素为字典，[{'title':title,'url':url},]
    """
    info_list = []
    count = 1
    for i in range(1,6):   #1到5页
        url = base_url.format(firstnum=(i-1)*40,curpage=i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')
        links = soup.find_all(title=True)
        for items in links:
            title = items['title'].replace('<font color = "#ff0000"> New </font>','')
            title = title.replace(' ','')  #去除标题空格，遇到标题有空格会报错转换pdf时会出错
            title = str(count).rjust(3,'0')+'.'+ title   #序号格式 001，002
            count+=1
            url = items['href']
            info_list.append({'title':title,'url':url})   #直接构造字典并放入列表中
    return info_list

def get_content(url):
    """
    获取网页内容
    :param url:  网页网址
    :return: html文档
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    content = soup.find_all(style="padding-top:10px; font-family:仿宋;")

    html = html_template.format(content=content)
    html = html.replace('[','') #去掉列表转字符串时的[ ]
    html = html.replace(']','')
    
    return html


def save_pdf(html, filename):
    """
    把所有html文件保存到pdf文件
    :param html:  html内容
    :param file_name: pdf文件名
    :return:
    """
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }

    pdfkit.from_string(html, filename, options=options)


def parse_html_to_pdf(list_info):
    base_path = os.path.dirname(__file__)
    for items in list_info:
        title = items['title']
        url = 'http://onsgep.moe.edu.cn/edoas2/website7/'+items['url']
        html = get_content(url)
        path = os.path.join(base_path,title+'.pdf')
        save_pdf(html,path)
            


list_info = get_url_list(base_url)
parse_html_to_pdf(list_info)


