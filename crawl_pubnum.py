#! /usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
import time, re


browser = webdriver.Firefox()
url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query={query}" \
      "&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=1655&sst0=1500629431507&lkt=0%2C0%2C0"
browser.get(url.format(query=''))


def get_biz_originid(content):
    bizgroup = re.search(r"var appuin = \"(.*)\"\|\|\"(.*)\";", content)
    biz = bizgroup.group(1) if not bizgroup and bizgroup.group(1) else bizgroup.group(2)
    oidgroup= re.search(r"var user_name = \"(.*)\";", content)
    originid = oidgroup.group(1) if oidgroup else ''
    return biz, originid

for l in open('nopubnum.txt'):
    app_info = dict()
    items = l.split()
    nick_name = items[0]
    weixin_name = items[1]
    browser.get(url.format(query=weixin_name))
    try:
        news_boxs = browser.find_element_by_class_name('news-list2')
    except:
        print ("find_no_artucle_url", weixin_name)
        continue
    for app in news_boxs.find_elements_by_tag_name('li'):
        try:
            imgbox = app.find_element_by_class_name('img-box')
            app_info['head_img_url'] = imgbox.find_element_by_tag_name('img').get_attribute('src')
            txtbox = app.find_element_by_class_name('txt-box')
            wxnamebox = txtbox.find_element_by_class_name('tit')
            app_info['nick_name'] = wxnamebox.text
            infobox = txtbox.find_element_by_class_name('info')
            app_info['weixin_name'] = infobox.find_element_by_tag_name('label').text
            for item in app.find_elements_by_tag_name('dl'):
                if '最近文章' not in item.text:
                    continue
                app_info['article_url'] = item.find_element_by_tag_name('a').get_attribute('href')
                break
            if 'article_url' not in app_info:
                print ("find_no_artucle_url", weixin_name)
                continue
            time.sleep(2)
            browser.get(app_info['article_url'])
            biz, originid = get_biz_originid(browser.page_source)
            app_info['biz'] = biz
            app_info['originid'] = originid
            print (app_info)
            time.sleep(3)
        except:
            break
