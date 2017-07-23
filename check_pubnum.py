#! /usr/bin/env python
# -*- coding:utf-8 -*-

import torndb, time

def get_app_info(weixin_name):
    return promote_db.get("select * from app_info where weixin_name=%(weixin_name)s limit 1", weixin_name=weixin_name)


def get_app_info1(originid):
    return promote_db.get("select * from app_info where originid=%(originid)s limit 1", originid=originid)

def update_sub(app_info, appid=4586095):
    sub = promote_db.get("select * from weixin_subscribe_config where appid = %(appid)s", appid=appid)
    if sub and sub.status == 1:
        print 'has_subed'
        return
    if sub and sub.status != 1:
        print 're_subed', datacenter_db.update("update weixin_subscribe_config set status =1 where weixin_craw_configid=%(wid)s",
                                            wid=sub.weixin_craw_configid)
        return
    print 'new_sub'
    datacenter_db.insert("insert into weixin_subscribe_config(appid, originid, status, app_infoid) values("
                      "%(appid)s, %(originid)s, 1, %(app_infoid)s)", appid=appid, originid=app_info.originid,
                      app_infoid=app_info.app_infoid)



idx = 0
for l in open('pubnum.txt'):
    items = l.split()
    weixin_name = items[0]
    app_name = items[1]
    desc = "".join(items[2:-1])
    app_info = get_app_info(weixin_name.strip())
    if not app_info:
        if not get_app_info1(weixin_name):
            print app_name, weixin_name
    print '-', idx
    idx += 1
    time.sleep(0.1)
