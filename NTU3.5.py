import requests
import socket
import tkinter
import tkinter.messagebox
import configparser
import threading
import os
import time
import pywifi
from win10toast import ToastNotifier
from pywifi import const
from favicon import img
from tkinter import *

root= Tk()
# 生成ConfigParser对象
toaster = ToastNotifier()#生成win10提示对象
config = configparser.ConfigParser()
filename = 'C:\\NTU\\NTUconfig.ini'
#检查配置文件是否存在
ifpathcun=os.path.exists(filename)
changshi=0
if  ifpathcun == False :
    if os.path.exists('C:\\NTU') == False:
        os.makedirs('C:\\NTU')
    ifcj=open(filename,mode='w+')
    ifcj.close 
    config.read(filename, encoding='utf-8')
    config.add_section('NTU')
    config.set("NTU","user", "")
    config.set("NTU","password","" )
    config.set("NTU","fuwu", "")
    config.write(open(filename, 'w'))
elif ifpathcun == True:
    config.read(filename, encoding='utf-8')
# 读取配置文件
ntuusersid=config.get("NTU","user")
ntupassword=config.get("NTU","password")
fuwui = config.get("NTU","fuwu")
wifi = pywifi.PyWiFi()  # 创建一个wifi对象
ifaces = wifi.interfaces()[0]  # 取第一个无线网卡
ifaces.scan()
result=ifaces.scan_results()
trynum = 1
def connwifi():
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(0.3)  # 缓冲
    connectwifi()

def connectwifi():
    global trynum
    profile = pywifi.Profile()  # 配置文件
    profile.ssid = "NTU"  # wifi名称
    profile.auth = const.AUTH_ALG_OPEN  # 需要密码?
    profile.akm.append(const.AKM_TYPE_NONE)  # 加密类型
    profile.cipher = const.CIPHER_TYPE_NONE  # 加密单元
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    toaster.show_toast(u'NTUconnect',u'正在尝试连接NTU',icon_path="favicon.ico")
    ifaces.connect(tmp_profile)  # 连接
    time.sleep(1.5)  # 尝试能否成功连接
    if ifaces.status() == const.IFACE_CONNECTED:
        isok = True
    else:
        isok = False
    
    if isok :
        enter()
    elif "NTU" in result: 
        if isok==False and trynum<3:
            trynum = trynum + 1
            toaster.show_toast(u'NTUconnect',u'正在尝试第{trynum}'.format(),icon_path="favicon.ico")
            connectwifi()
        else:
            tkinter.messagebox.showinfo(title='NTU自动连接：错误提示！', message='wifi连接失败，原因：接入点无响应或被拒绝。')
    else:
        tkinter.messagebox.showinfo(title='NTU自动连接：错误提示！', message='wifi连接失败，请检查SSID=NTU的wifi是否在范围内')

def enter():
    #获取本机的IP地址
    try: 
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        s.connect(('8.8.8.8',80)) 
        ipaddr = s.getsockname()[0] 
    finally: 
        s.close() 
        reuserid=text2.get()
        reuserpassword=text3.get()

    if reuserid == '' :
        enuserid=ntuusersid
        enuserpassword=ntupassword
        fuwus=fuwui
    elif reuserid != '' :
        enuserid=reuserid
        enuserpassword=reuserpassword
        fuwus=v.get()
    
    get_addr="http://210.29.79.141:801/eportal/?"
    params = {
    'c' : 'Portal',
    'a' : 'login',
    'callback':'dr1003',
    'login_method' : '1',
    'user_account' : ',0,'+enuserid+'@'+fuwus,
    'user_password' : enuserpassword,
    'wlan_user_ip' : ipaddr,
    'wlan_user_ipv6' : '',
    'wlan_user_mac' : '000000000000',
    'wlan_ac_ip' : '',
    'wlan_ac_name' : '',
    'jsVersion' : '3.3.2',
    'v' : '3568'
    }
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'}
    res = requests.get(url=get_addr,headers=headers,params=params)
    if '"msg":""' in res.text:
        lable7.configure(text='状态：您已经登录！')
        tkinter.messagebox.showinfo(title=ipaddr, message='您已经登录！请勿重复操作') 
    elif '"result":"1"' in res.text:
        lable7.configure(text='状态：登录成功！')
        tkinter.messagebox.showinfo(title=ipaddr, message='登录成功！') 
        config.set("NTU","user", enuserid)
        config.set("NTU","password", enuserpassword)
        config.set("NTU","fuwu", fuwus)
        config.write(open(filename, 'w'))
        lable5.configure(text="上 一 次 账 号： "+ntuusersid)
        lable6.configure(text="上 一 次 密 码： "+ntupassword[:2]+"***"+ntupassword[10:])
        lable8.configure(text="上 一 次 服 务 商： "+fuwui)
    elif '"msg":"bGRhcCBhdXRoIGVycm9y"' in res.text:
        lable7.configure(text='状态：密码错误！')
        tkinter.messagebox.showinfo(title=ipaddr, message='密码错误！') 
    elif '"msg":"dXNlcmlkIGVycm9yMQ=="' in res.text:
        lable7.configure(text='状态：账号错误！')
        tkinter.messagebox.showinfo(title=ipaddr, message='账号错误！') 
    elif '"msg":"QXV0aGVudGljYXRpb24gZmFpbA=="' in res.text:
        lable7.configure(text='状态：参数异常！')
        tkinter.messagebox.showinfo(title=ipaddr, message='参数异常！') 
    elif '"msg":"QXV0aGVudGljYXRpb24gRmFpbCBFcnJDb2RlPTA1"' in res.text:
        lable7.configure(text='状态：运营商错误！')
        tkinter.messagebox.showinfo(title=ipaddr, message='运营商错误！') 

def hander(e):
    pac=threading.Thread(target=connwifi,name="connwifi")
    pac.start()

#制作窗体

root.title('NTU自动登录系统 by：nkdns')
root.geometry('340x200+500+300')
try:
    root.wm_iconbitmap('favicon.ico')
except BaseException:
    print('图标未加载')
finally:
    v=StringVar()
    if fuwui=='':
        v.set('1')
    elif fuwui !='':
        v.set(fuwui)
    side1=Frame(root);side1.pack()
    side2=Frame(root);side2.pack()
    side3=Frame(root);side3.pack()
    side4=Frame(root);side4.pack()
    side5=Frame(root);side5.pack()
    side6=Frame(root);side6.pack()
    side7=Frame(root);side7.pack()

    r1=Radiobutton(side1, text='中国电信', variable=v, value='telecom')
    r1.pack(side=LEFT)
    r2=Radiobutton(side1, text='中国移动', variable=v, value='cmcc')
    r2.pack(side=LEFT)
    r3=Radiobutton(side1, text='中国联通', variable=v, value='unicom')
    r3.pack(side=RIGHT)
    lable2=Label(side2,text="账 号：   ")
    lable2.pack(side=LEFT)
    text2=Entry(side2)
    text2.pack(side=RIGHT)
    lable3=Label(side3,text="密 码：   ")
    lable3.pack(side=LEFT)
    text3=Entry(side3)
    text3.pack(side=RIGHT)
    buttom1=Button(side4)
    buttom1.pack(side=LEFT)
    buttom1["text"]="登 录"
    buttom1.bind('<Button -1>',hander)
    lable5=Label(side5,text="上 一 次 账 号： "+ntuusersid)
    lable5.pack(side=LEFT)
    lable6=Label(side6,text="上 一 次 密 码： "+ntupassword[:2]+"***"+ntupassword[10:])
    if(ntupassword==''):
        lable6=Label(side6,text="上 一 次 密 码： ")
    lable6.pack()
    lable8=Label(side6,text="上 一 次 服 务 商： "+fuwui)
    lable8.pack()
    lable7=Label(side7,text="状态：请操作。。。",font=('Arial', 12))
    lable7.pack(side=LEFT)
    root.resizable(0,0)
    if fuwui != '':
       hander(1)
    root.mainloop()