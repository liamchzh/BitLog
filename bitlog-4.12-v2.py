# -*- coding:utf-8 -*-
import Tkinter
import urllib
import urllib2
import cookielib
import md5
import re
import cPickle as pickle
import tkMessageBox as box
import Pmw
def log_in(user, password, sta):
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
    revalue = resp.read()
    print revalue
    if re.search('[^a-z]',revalue[0:1]):#登陆成功
        pass#最小化
    else:
        onError(revalue)

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
    onError(revalue)
    

def onError(case):
    if case == 'username_error':
        box.showerror("ERROR", "用户名错误")
    elif case == 'password_error':
        box.showerror("ERROR","密码错误")
    elif case == 'status_error':
        box.showerror("ERROR","用户已欠费")
    elif case == 'available_error':
        box.showerror("ERROR","用户已禁用")
    elif case == 'ip_exist_error':
        box.showerror("ERROR","您的IP尚未下线，请稍后")
    elif case == 'usernum_error':
        box.showerror("ERROR","用户数已达上限")
    elif case == 'online_num__error':
        box.showerror("ERROR","登陆人数超过限额")
    elif case == 'logout_error':
        box.showerror("ERROR","您不在线上")
    elif case == 'logout_ok':
        box.showerror("OK","注销成功")
    else:
        box.showerror("ERROR","暂时无法连接服务器")

class MyDialog:
    def __init__(self, root):
        self.top = Tkinter.Toplevel(root)
        #账号
        u = Tkinter.StringVar()
        u.set(user)
        self.user = Tkinter.Entry(self.top, textvariable = u, width = 15)
        userlabel = Tkinter.Label(self.top, width = 10, text = u"账号")
        userlabel.pack(side = "left", pady = 8)
        self.user.pack(side = "left")
        
        #密码
        p = Tkinter.StringVar()
        p.set(pswd)
        self.pswd = Tkinter.Entry(self.top, textvariable = p, width = 15)
        pswdlabel = Tkinter.Label(self.top, width = 10, text = u"密码")
        pswdlabel.pack(side = "left", pady = 8)
        self.pswd.pack(side = "left")
        self.pswd['show'] = '*'
        #保存按钮
        save_but = Tkinter.Button(self.top, text = u"保存1", command = self.save)
        save_but.pack()
        #是否使用国际流量
        global v
        v = Tkinter.IntVar()
        v.set(sta)
        self.check_but = Tkinter.Checkbutton(self.top, variable = v, text = u'仅使用免费流量', command = self.checkbutton)
        self.check_but.pack(side = "left")

    def checkbutton(self):#判断是否使用国际流量
        if sta == 0:
            v.set(1)
        else:
            v.set(0)

    def save(self):
        global user
        global pswd
        global sta
        user = self.user.get()
        pswd = self.pswd.get()
        sta = v.get()
        print sta
        fuser = file('user.pkl','wb+')
        fpswd = file('pswd.pkl','wb+')
        fsta = file('sta.pkl','wb+')
        pickle.dump(user, fuser)
        pickle.dump(pswd, fpswd)
        pickle.dump(sta,fsta)
        self.top.destroy()
    def get(self):
        return self.input

class MyButton():
    def __init__(self, root, type):
        self.root = root
        
        if type == 0:
            self.button = Tkinter.Button(root,command = self.data, bitmap = 'info')
        elif type == 1:
            global img_left
            img_left = Tkinter.PhotoImage(file = 'arrow_left.gif')
            self.button = Tkinter.Button(root, text = u"登陆", command = self.login, image = img_left)
        elif type == 2:
            global img_right
            img_right = Tkinter.PhotoImage(file = 'arrow_right.gif')
            self.button = Tkinter.Button(root, text = u"注销", command = self.logout, image = img_right)
        elif type == 3:
            self.button = Tkinter.Button(root, command = self.aboutdia, bitmap = 'hourglass')
        self.button.pack()
    def data(self):
        d = MyDialog(self.root)

    def login(self):
        ##print user + ':' + pswd
        if user == '' or pswd == '':
            d = MyDialog(self.root)
        else:
            try:
                log_out(user, pswd)
                print 'log_in'
                self.root.wm_iconify()#最小化
            except:
                onError("url_error")
    def logout(self):
        if user == '' or pswd == '':
            d = MyDialog(self.root)
        else:
            try:
                log_in(user, pswd, sta)
            except:
                onError("url_error")
    def aboutdia(self):
        #Pmw.initialize()
        Pmw.aboutversion('1.0')
        Pmw.aboutcopyright('Liam 2012')
        Pmw.aboutcontact(
            '关于BitLog请访问：\n'+
            'www.liamchzh.co.cc\n'+
            '问题反馈或提出建议:\n'+
            'Email: liamchzh@gmail.com'
            )
        about = Pmw.AboutDialog(root, applicationname = 'BitLog')
        
if __name__ == '__main__':
    root = Tkinter.Tk()
    #设置软件尺寸
    root.geometry("300x400+100+100")
    global user
    global pswd
    global sta
    try:
        fuser = file('user.pkl','rb+')
        fpswd = file('pswd.pkl','rb+')
        fsta = file('sta.pkl','rb+')
        user = pickle.load(fuser)
        pswd = pickle.load(fpswd)
        sta = pickle.load(fsta)
        print 'user&pswd can be read:' + user + pswd + ':' + str(sta)
    except IOError:
        fuser = file('user.pkl','wb+')
        fpswd = file('pswd.pkl','wb+')
        fsta = file('sta.pkl','wb+')
        print 'user&pswd can\'t be read'
        user = ''
        pswd = ''
        sta = 0
    MyButton(root, 0)#修改账号密码
    MyButton(root, 1)#登陆按钮
    MyButton(root, 2)#注销按钮
    MyButton(root, 3)#关于页面
    root.mainloop()
