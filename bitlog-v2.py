# coding:utf-8
"""
Author: Liam  
E-mail: liamchzh@gmail.com
"""

import pygtk
import gtk
import urllib
import urllib2
import cookielib
import md5
import re
import os
import cPickle as pickle

class MainFrame(gtk.Window):
    def __init__(self):
        super(MainFrame, self).__init__() # 初始化

        self.set_title("BitLog") # 标题
        self.set_size_request(250, 150) # 窗口大小
        self.set_position(gtk.WIN_POS_CENTER) # 窗口位置
        self.connect("destroy", gtk.main_quit)
        self.set_icon_from_file("icon.png")
        
        #LOGO "BitLog"
        logo = gtk.Label() 
        logo.set_use_markup(gtk.TRUE)
        logo.set_markup('<span size="38000"><b>BitLog</b></span>')
        
        # 图标
        login_img = gtk.Image()
        login_img.set_from_file("login.png")
        logout_img = gtk.Image()
        logout_img.set_from_file("logout.png")
        setting_img = gtk.Image()
        setting_img.set_from_file("setting.png")
        about_img = gtk.Image()
        about_img.set_from_file("about.png")
        
        login_btn = gtk.Button() # 登录按钮
        login_btn.set_image(login_img)
        login_btn.connect("clicked", self.login)
        login_btn.set_tooltip_text(u"登录")
        login_btn.set_size_request(100, 40)

        logout_btn = gtk.Button() # 注销按钮
        logout_btn.set_image(logout_img)
        logout_btn.connect("clicked", self.logout)
        logout_btn.set_tooltip_text(u"注销")
        logout_btn.set_size_request(100, 40)

        setting_btn = gtk.Button() # 设置按钮
        setting_btn.set_image(setting_img)
        setting_btn.connect("clicked", self.Se)
        setting_btn.set_tooltip_text(u"设置")

        about_btn = gtk.Button() # 关于按钮
        about_btn.set_image(about_img)
        about_btn.connect("clicked", self.Ab)
        about_btn.set_tooltip_text("关于")

        # 控件布局
        fixed = gtk.Fixed()
        fixed.put(logo, 20, 20)
        fixed.put(setting_btn, 200,20)
        fixed.put(about_btn, 200, 50)
        fixed.put(login_btn, 20, 85)
        fixed.put(logout_btn, 130, 85)

        self.add(fixed)
        self.show_all()
    
        # 检查本地是否存有账号和密码
        global user, pswd, sta
        try:
            fuser = file('user.pkl','rb+')
            fpswd = file('pswd.pkl','rb+')
            fsta = file('sta.pkl','rb+')
            user = pickle.load(fuser)
            pswd = pickle.load(fpswd)
            sta = pickle.load(fsta)
        except:
            fuser = file('user.pkl','wb+')
            fpswd = file('pswd.pkl','wb+')
            fsta = file('sta.pkl','wb+')
            user = ''
            pswd = ''
            sta = 0
    
    # 登录
    def login(self, widget):
        if user == '' or pswd == '':
            settings()
        else:
            signal, info = log_in(user, pswd, sta)
            if signal: #登录成功
                self.iconify()
            else: #登录失败
                self.Message(self, info)

    def logout(self, widget):
        info  = log_out(user, pswd)
        self.Message(self, info)
        
    # 设置
    def Se(self, widget):
        settings()

    # 消息框
    def Message(self, widget, case):
        if case == 'username_error':
            info = u"用户名错误"
        elif case == 'password_error':
            info = u"密码错误"
        elif case == 'status_error':
            info = u"用户已欠费"
        elif case == 'available_error':
            info = u"用户已禁用"
        elif case == 'ip_exist_error':
            info = u"IP尚未下线，请稍后"
        elif case == 'usernum_error':
            info = u"用户数已达上限"
        elif case == 'online_num__error':
            info = u"登陆人数超过限额"
        elif case == 'logout_error':
            info = u"您不在线上"
        elif case == 'logout_ok':
            info = u"注销成功"
        elif case == 'ip_error':
            info = u"您的IP不合法"
        else:
            info = u"暂时无法完成操作"

        md = gtk.MessageDialog(self, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, info)
        md.run()
        md.destroy()
        
    # 关于框
    def Ab(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("BitLog")
        about.set_version("2.0")
        about.set_copyright("(c) Liam")
        about.set_comments(u"一款用于登录外网的开源客户端")
        about.set_website_label("http://liamchzh.com")
        about.run()
        about.destroy()

class settings(gtk.Window):
    def __init__(self):
        super(settings, self).__init__()
        
        self.set_title("Settings")
        self.set_default_size(250, 120)
        self.set_position(gtk.WIN_POS_CENTER)
        
        global user_entry, pswd_entry, sta

        
        user_label = gtk.Label(u"用户名")
        pswd_label = gtk.Label(u"密码")
        user_entry = gtk.Entry(40)
        pswd_entry = gtk.Entry(40)
        pswd_entry.set_visibility(False)# 密码文本框字符不可见
        user_entry.set_max_length(20) # 最大字符数
        pswd_entry.set_max_length(20)

        sta_btn = gtk.CheckButton(u"仅使用免费流量") # 是否国际流量
        sta_btn.connect("clicked", self.sta_change)
        
        save_btn = gtk.Button(u"保存") # 保存按钮
        save_btn.connect("clicked", self.save)
        save_btn.set_size_request(50, 30) # 按钮大小
        
        # 控件布局
        fixed = gtk.Fixed()
        fixed.put(user_label, 20, 25)
        fixed.put(pswd_label, 20, 55)
        fixed.put(user_entry, 70, 20)
        fixed.put(pswd_entry, 70, 50)
        fixed.put(sta_btn, 20, 85)
        fixed.put(save_btn, 180, 80)

        self.add(fixed)
        self.show_all()
    
        try:
            fuser = file('user.pkl','rb+')
            fpswd = file('pswd.pkl','rb+')
            fsta = file('sta.pkl','rb+')
            user = pickle.load(fuser)
            pswd = pickle.load(fpswd)
            sta = pickle.load(fsta)
        except:
            fuser = file('user.pkl','wb+')
            fpswd = file('pswd.pkl','wb+')
            fsta = file('sta.pkl','wb+')
            user = ''
            pswd = ''
            sta = 0

        user_entry.set_text(user)
        pswd_entry.set_text(pswd)
        if sta:
            sta_btn.set_active(True)

    def sta_change(self, widget):
        global sta
        if widget.get_active():
            sta = 1
        else:
            sta = 0

    def save(self, widget):
        global user, pswd, sta
        user = user_entry.get_text()
        pswd = pswd_entry.get_text()
        fuser = file('user.pkl','wb+')
        fpswd = file('pswd.pkl','wb+')
        fsta = file('sta.pkl','wb+')
        pickle.dump(user, fuser)
        pickle.dump(pswd, fpswd)
        pickle.dump(sta,fsta)
        self.destroy()

# 登录和注销
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
    revalue = resp.read()#读取返回信息
    if re.search('[^a-z]',revalue[0:1]): #登陆成功
        return True, 'succeed'
    else:
        return False, revalue

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

if __name__ == '__main__':
    MainFrame()
    gtk.main()
