# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import os
import sys
import md5

# 登录和注销
def log_in(user, password, sta=0):
    #处理Cookie信息
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    #把密码进行MD5加密
    a = md5.new(password)
    pswd = a.hexdigest()
    login_pswd = pswd[8:-8]
    
    log_url = 'http://10.0.0.55/cgi-bin/do_login'#post_url
    login_info = {
        'drop' : sta,    #1为仅访问免费资源，0为可以使用国际流量
        'n' : 100,     #100为正常登陆，1为强制注销
        'password' : login_pswd,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(login_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()#读取返回信息
    if re.search('[^a-z]',revalue[0:1]): #登陆成功
        return 'succeed'
    else:
        return revalue

def log_out(user, password):
    log_url = 'http://10.0.0.55/cgi-bin/force_logout'
    logout_info = {
        'drop' : 0,     #1为仅访问免费资源，0为可以使用国际流量
        'n' : 1,        #100为正常登陆，1为强制注销
        'password' : password,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(logout_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()
    return revalue # 返回注销结果

user = '369479921'
pswd = '910918'

def main(argv):
    if argv[0] == 'in':
        if len(argv) == 2 and argv[1] == '1':
            print 'international website will not be available'
            print log_in(user, pswd, 1)
        else:
            print log_in(user, pswd)
    elif argv[0] == 'out':
        print log_out(user, pswd)
    else:
        print 'what do you want to do:in or out?'

if __name__ == '__main__':
    main(sys.argv[1:])
