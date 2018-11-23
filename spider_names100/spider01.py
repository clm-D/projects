import re

from lxml import etree
import requests
from lianjie_mysql import MyMySql
import threading


def get_page(str1):
    url = 'http:' + str1
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


def parse_xpath(html):
    etree_html = etree.HTML(html)

    # xing_dict = {}
    # a_labels = etree_html.xpath('//a[@class="btn btn2"]')
    # for a_label in a_labels:
    #     xing = a_label.xpath('./text()')[0]
    #     xing = str(xing)
    #     xing = xing.replace('姓名字大全', '')
    #     nums = a_label.xpath('./@title')[0]
    #     nums = str(nums)
    #     num = re.findall(r'\d+', nums)[0]
    #     xing_dict[xing] = num
    # return xing_dict

    hrefs = etree_html.xpath('//a[@class="btn btn2"]/@href')
    return hrefs


def parse_xpath3(html):
    etree_html = etree.HTML(html)
    name_dict = {}

    name = etree_html.xpath('//div[@class="col-xs-12"]//ul[@class="nav navbar-nav"]/li/a/text()')[0]
    name = str(name)
    name = name.replace('我也叫', '')
    name_dict['name'] = name
    # print(name)

    xing = etree_html.xpath('//div[@id="head_"]//div[@class="navbar-header"]/a/div/text()')[0]
    xing = str(xing)
    xing = xing.replace('姓之家', '')
    name_dict['xing'] = xing

    nums = etree_html.xpath('//div[@class="col-xs-12"]//div[@class="navbar-brand"]/text()')[0]
    nums = str(nums)
    num = re.findall(r'\d+', nums)[0]
    name_dict['num'] = num
    # print(num)

    girl_progress = etree_html.xpath('//div[@class="progress-bar progress-bar-warning"]/text()')[0]
    girl_progress = str(girl_progress)
    girl_progress = float(girl_progress.split('%')[0])
    boy_progress = round((100 - girl_progress), 2)
    name_dict['boy_progress'] = str(boy_progress) + '%'
    name_dict['girl_progress'] = str(girl_progress) + '%'
    # print(boy_progress)
    # print(girl_progress)
    try:
        zongjie = etree_html.xpath('//div[@class="col-xs-4 col-mx-12"]//div[@class="panel-body"]/strong/text()')[0]
        name_dict['zongjie'] = zongjie
    except:
        zongjie = ''
        name_dict['zongjie'] = ''
    # print(zongjie)

    fenxis = etree_html.xpath('//div[@class="col-xs-8 col-mx-12"]//div[@class="col-xs-6"]/blockquote/text()')[0]
    name_dict['fenxis'] = fenxis
    # print(fenxis)

    # print(name_dict)
    bjx = MyMySql('names100')
    sql = 'select name from names where name = "%s"' % name
    ret = bjx.search(sql)
    if not ret:
        sql = 'insert into names(name, surname, nums, boy_progress, girl_progress, total_solution, wuxing) ' \
              'values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
              (name, xing, num, boy_progress, girl_progress, zongjie, fenxis)
        print(sql)
        bjx.insert(sql)
    bjx.close()


def parse_xpath2(html):
    etree_html = etree.HTML(html)
    names_dict = {}

    try:
        a_labels = etree_html.xpath('//div[@class="col-xs-12"]/a[@class="btn btn-link"]')
        for a_label in a_labels:
            names_dict[a_label.xpath('./text()')[0]] = a_label.xpath('./@href')[0]
            # print(names_dict)

        return names_dict
    except:
        return names_dict


def main():
    html1 = get_page('//www.resgain.net/xmdq.html')
    # print(html)

    # 插入surnames表
    # xing_dict = parse_xpath(html1)
    # bjx = MyMySql('names100')
    # for v, k in xing_dict.items():
    #     sql = 'insert into surnames(surname, nums) values ("%s", "%s")' % (v, k)
    #     print(sql)
    #     bjx.insert(sql)
    # bjx.close()


    hrefs = parse_xpath(html1)
    th_start(hrefs)
    # print(hrefs)

def fen_url(hrefs):
    urls = hrefs
    big_list = [url for url in urls]
    n = 15
    url_list = [big_list[i:i + n] for i in range(0, len(big_list), n)]
    return url_list


def thread_dd(url_list):
    for item in url_list:
        names_dict = {}
        item2 = str(item)
        # print(item2)
        for i in range(1, 11):
            item3 = item2.replace('.html', '_%d.html') % i
            # print(item3)
            html2 = get_page(item3)
            # parse_xpath2(html2, item2)
            names_dict.update(parse_xpath2(html2))
        # print(len(names_dict))
        item2 = str(item)
        item2 = item2.split('/')
        for v, k in names_dict.items():
            url = '//' + item2[2] + k
            # print(url)
            html = get_page(url)
            parse_xpath3(html)


def th_start(hrefs):
    url_lists = fen_url(hrefs)
    threads = []
    for url_list in url_lists:
        # print(item)
        t = threading.Thread(target=thread_dd, args=(url_list,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print('*************************')


if __name__ == '__main__':
    main()
