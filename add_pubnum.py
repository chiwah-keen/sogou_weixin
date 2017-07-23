#! /usr/bin/env python
# -*- coding:utf-8 -*-

import torndb, time

def get_app_info(weixin_name):
    return promote_db.get("select * from app_info where weixin_name=%(weixin_name)s limit 1", weixin_name=weixin_name)

def get_app_info1(weixin_name):
    return promote_db.get("select * from app_info where originid=%(weixin_name)s limit 1", weixin_name=weixin_name)

def update_sub(app_info, appid=4586095):
    sub = datacenter_db.get("select * from weixin_subscribe_config where appid = %(appid)s and originid=%(originid)s limit 1",
                         appid=appid, originid=app_info.originid)
    if sub and sub.status == 1:
        print 'has_subed'
        return
    if sub and sub.status != 1:
        print 're_subed', datacenter_db.update("update weixin_subscribe_config set status =1 where weixin_craw_configid=%(wid)s",
                                            wid=sub.weixin_craw_configid)
        return
    print 'new_sub', app_info.originid
    datacenter_db.insert("insert into weixin_subscribe_config(appid, originid, status, app_infoid) values("
                      "%(appid)s, %(originid)s, 1, %(app_infoid)s)", appid=appid, originid=app_info.originid,
                      app_infoid=app_info.app_infoid)



for l in open('pubnum.txt'):
    items = l.split()
    weixin_name = items[0]
    app_name = items[1]
    app_info = get_app_info(weixin_name.strip())
    if not app_info:
        app_info = get_app_info1(weixin_name.strip())
        if not app_info:
            print "still no", weixin_name
            continue
    update_sub(app_info)
    time.sleep(1)
