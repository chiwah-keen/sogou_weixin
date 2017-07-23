#! /usr/bin/env python
# -*- coding:utf-8 -*-

import torndb, time, json


def insert_app(app):
    promote_db.insert("insert into app_info(nick_name, weixin_name, head_img_url, originid, biz) "
                      "values(%(nick_name)s, %(weixin_name)s, %(head_img_url)s, %(originid)s, %(biz)s)",
                      nick_name=app.get('nick_name'), weixin_name=app.get('weixin_name'), head_img_url=app.get('head_img_url'),
                      biz=app.get('biz'), originid=app.get('originid'))


def get_app(originid):
    return promote_db.get("select * from app_info where originid=%(originid)s", originid=originid)

for l in open('pubnums.txt'):
    app = json.loads(l)
    if not get_app(app.get('originid')):
        print (app)
        insert_app(app)
        continue
    print ("has_")
