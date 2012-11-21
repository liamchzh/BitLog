# -*- coding:utf-8 -*-
import Tkinter
import urllib
import urllib2
import cookielib
import md5
root = Tkinter.Tk()

def log_in(user, password):
    #处理Cookie信息
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    #把密码进行MD5加密
    a = md5.new(password)
    pswd = a.hexdigest()
    login_pswd = pswd[8:-8]
    
    log_url = 'http://10.0.0.55/cgi-bin/do_login'
    login_info = {
        'drop' : 1,    #1为仅访问免费资源，0为可以使用国际流量
        'n' : 100,     #100为正常登陆，1为强制注销
        'password' : login_pswd,
        'type': 1,
        'username' : user}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(login_info))
    resp = urllib2.urlopen(req)
    revalue = resp.read()
    print revalue

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
    print revalue    
#设置软件尺寸
root.geometry("300x400+100+100")

class MyDialog:
    def __init__(self, root):
        self.top = Tkinter.Toplevel(root)
        #账号
        self.user = Tkinter.Entry(self.top, width = 15)
        userlabel = Tkinter.Label(self.top, width = 10, text = u"账号")
        userlabel.pack(side = "left", pady = 8)
        self.user.pack(side = "left")
        #密码
        self.pswd = Tkinter.Entry(self.top, width = 15)
        pswdlabel = Tkinter.Label(self.top, width = 10, text = u"密码")
        pswdlabel.pack(side = "left", pady = 8)
        self.pswd.pack(side = "left")

        save_but = Tkinter.Button(self.top, text = u"保存1", command = self.save)
        save_but.pack()
    def save(self):
        global user
        global pswd
        user = self.user.get()
        pswd = self.pswd.get()
        self.top.destroy()
    def get(self):
        return self.input

class MyButton():
    def __init__(self, root, type):
        self.root = root
        if type == 0:
            self.button = Tkinter.Button(root, text = u"账号密码", command = self.data)
        elif type == 1:
            self.button = Tkinter.Button(root, text = u"登陆", command = self.login)
        else:
            self.button = Tkinter.Button(root, text = u"注销", command = self.logout)
        self.button.pack()
    def data(self):
        d = MyDialog(self.root)

    def login(self):
        print user + ':' + pswd
        log_in(user, pswd)
        
    def logout(self):
        log_out(user, pswd)
        
if __name__ == '__main__':
    MyButton(root, 0)#修改账号密码
    MyButton(root, 1)#登陆按钮
    MyButton(root, 2)#注销按钮
    root.mainloop()
