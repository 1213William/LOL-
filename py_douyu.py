import requests

from bs4 import BeautifulSoup

from operator import itemgetter, attrgetter


def get_html_content(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)


def get_link_list(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.select('div.DyListCover')


def get_data(link_list):
    base_url = 'https://www.douyu.com'
    lst = []
    for i in link_list:
        # print(i)
        link = base_url + i.contents[0].get('href')
        title_element = i.select('div.DyListCover-content')
        for i in title_element:
            logo = i.contents[0].contents[0].text
            people = i.contents[1].contents[0]
            title_el = i.contents[1].contents[1]
            title = title_el.text
            people = people.text
            # print('%s --> %s --> %s' % (logo, title, people))
            info = {
                '主播名-->': title,
                '人气 -->': people,
                '播出 -->': logo,
                '链接 -->': link
            }
            lst.append(info)
    return lst


def sort(data):

    # return sorted(data, key=itemgetter('人气 -->'))  # 这个返回的只是根据人气里面的第一个数字开始比较的，后面的是要发生了重复就会发生重叠了，所以要将那个万改成数字类型的
    res = sorted(data, key=lambda num: [(float(i['人气 -->'].strip('万')) * 10000) for i in data if i['人气 -->'].endswith('万')])
    return res


def main():
    url = 'https://www.douyu.com/g_LOL'  # 如果想要别的种类多视频的话，可以通过修改这个url来进行修改
    html = get_html_content(url)
    res = get_link_list(html)
    res = get_data(res)
    # print(res)
    for i in sort(res):
        print(i)


if __name__ == '__main__':
    main()
