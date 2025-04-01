try:
    from pyautogui import keyDown,keyUp,press
    from pynput.keyboard import Listener
    import threading
    import time
    import re
    import os
    import win32process
    import psutil
    import tkinter as tk  
    from tkinter import messagebox
    import keyboard
    import win32gui
    from win10toast import ToastNotifier
    from tkinter import font
    import pygame
    print('依赖库正常导入')
    import sys
    import json
except ImportError as ms:
    import time
    print(f'无法找到依赖库{ms}')
    install = str(input('获取请输入Y/y')).lower()
    name = re.search(r"'([^']*)'",str(ms))
    N1 = f'pip install {ms}'
    schedule = 0
    if install == 'y':
        os.system(N1)
    time.sleep(4)
from FreePlay import Listener_listen_key_test
script_path = os.path.abspath(sys.argv[0])
# 获取脚本文件所在的目录
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)
#弹窗提示
def show_message_box(title,add):
    root = tk.Tk()
    root.wm_attributes('-topmost',1)
    # 隐藏主窗口  
    root.withdraw()
    messagebox.showinfo(title, add)
    root.destroy()
#弹窗错误
def show_error(title,add):
    root = tk.Tk()
    root.wm_attributes('-topmost',1)
    root.withdraw()
    messagebox.showerror(title=title+"错误", message=add)
    root.destroy()
#Windows弹窗消息
def xiaoxi(title,message):
    show_message_box(title,message)
def count_elements(lst):
    count = 0
    for item in lst:
        if isinstance(item, list):
            count += count_elements(item)  # 递归调用处理嵌套列表
        else:
            count += 1  # 处理非列表元素
    return count

from colorama import Fore, Back, Style, init
class RealTimeProgress:
    """## 实时进度条
    - `progress()`方法启动进度条线程
    - 更新内部`timer`成员以更新进度条
    - `timer`值`min=0,max=100`
    - 设置颜色值`ps_font_color,txt_font_color,num_font_color`
    - 设置进度条符号`font,stop,title`
    """
    def __init__(self):
        self.stop_event = threading.Event()
        self.timer = 0#实时进度
        self.ontime = 0#上次进度
        self.thread = None#线程启动
        self.ProgressStatus = 0#进度状态
        self.mount = 0#挂载进度
        self.title = '播放进度'
        self.stop = '播放结束'
        self.font = "▓"
        self.ps_font_color = Fore.RED
        self.txt_font_color = Fore.GREEN
        self.num_font_color = Fore.BLUE
    def progress(self):
        """### 进度条启动"""
        def run():
            while self.timer < 100:
                if self.ProgressStatus != self.timer:
                    self.update_progress(self.ProgressStatus,self.timer)
                time.sleep(1)
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
    def update_progress(self,PStatus:int|None=None,new_progress:int=100):
        """### 成员方法,`不建议使用主动更新`"""
        ls = ''
        bandPStatus = self.ontime if PStatus == None else PStatus
        for long in range(bandPStatus,new_progress+1):
            l = 50 - long // 2
            c = '-' * l
            if long == 100:
                ls = self.stop
            print("\r{}: {}%:{}{}%{}{}{} ".format(self.txt_font_color+self.title,self.num_font_color+str(long),self.ps_font_color+'[',self.ps_font_color+self.font * (long // 2),c,self.ps_font_color+']',self.txt_font_color+ls), end="")
            time.sleep(0.05)
        self.ProgressStatus = new_progress

xiaoxi("[Yuan_Qin]》》", "应用已运行||局内按键使用\nF1暂停/继续演奏       F2速度-0.2\nF3速度+0.2     F4结束演奏")
version = 3.15
versionid = 4
print(f'''******************************欢迎使用键琴演奏******************************
                       当前版本:Yuan_Qin-version:{version}
                                  迭代ID:{versionid}
                            ******使用须知******
                            使用自创乐谱请规范格式
                            详细请看自带乐谱起风了.yq
---版本计划://1.12进行按键同步优化,2.13创作功能大更新,3.14新用户界面大更新,3.15新创作模式游戏乐曲离线播放--自此版本//
---4.16大更新接入HTML网页,5.17深度代码层优化,9.1最终优化,11.1乐谱纠错和创造模式接入AI,19.10最终版本
局内按键使用:F1暂停/继续演奏       F2速度-0.2      F3速度+0.2     F4结束演奏''')
class musickey:
    def __init__(self,fun=None,fun2=None,fun3=None):
        #局内调整器
        # self.status = True    #进程
        # self.speed = 1000    #速度
        # self.processDown = 'run'    #进程结束
        self.stop_event = threading.Event()#线程1
        self.stop_event2 = True#线程2
        # self.jstatus = 0#应用状态
        self.Last_time_key = None#创作键位
        # self.txif = False#开头等待
        # self.datestop = None#是否需要开头等待
        self.thread = None#线程1
        self.thread2 = None#线程2
        # self.Back = None#前后
        # self.tstatus = False#是否退出
        # self.local = False#是否离线模式
        if fun != None and fun2 != None and fun3 != None:
            self.fun = fun
            self.fun2 = fun2
            self.fun3 = fun3
        else:
            self.fun = None
            self.fun2 = None
            self.fun3 = None
        self.state = {"yan":{"status":True,"tstatus":False,"speed":1000,"processDown":"run","local":False,"jstatus":0},"txif":False,"datestop":None,"Back":None}#全局状态管理
    #乐谱导入处理
    def txtimport(self,file):
        try:
            with open(file,'r+',encoding='utf-8') as f:
                txt = f.read()
            #处理乐谱
            txt_split = txt.split('\n')
            # music = []
            music = [[detection for detection in txtn.split(' ') if detection != ''] for txtn in txt_split]
            # for txtn in txt_split:
            #     MusicList = txtn.split(' ')
            #     temporarily = []
            #     for detection in MusicList:
            #         if detection != '':
            #             temporarily.append(detection)
            #     music.append(temporarily)
            music2 = []
            musictext = ''
            self.words = []
            onquet = ''
            for ky in music:
                if re.findall(r'[\u4e00-\u9fff]',''.join(ky)):
                    onquet = ''.join(ky)
                else:
                    temporarily2 = []
                    for key in ky:
                        if re.match(r'[a-zA-Z]',key):
                            musictext = musictext+key
                        else:
                            temporarily2.append(''.join(f'{c}+' if i < len(musictext.lower())-1 else c for i, c in enumerate(musictext.lower())))
                            temporarily2.append(key)
                            musictext = ''
                    if len(temporarily2) > 0:
                        music2.append(temporarily2)
                        self.words.append(onquet)
            if self.state["txif"] == False:
                date = input('[Yuan_Qin]》》乐谱已处理完成,请输入等待开始时间')
                if date == '':
                    date = 2
            elif self.state["txif"] == True:
                date = self.state["datestop"]
                if date == None:date = 0
            time.sleep(float(date))
            return music2
        except UnicodeDecodeError as t2:
            print('[Yuan_Qin]》》无法打开文件,请确保文件内容只有字键和数字,返回错误:',t2)
            show_error('[Yuan_Qin]','无法打开文件,请确保文件内容只有字键和数字,返回错误:'+t2)
            return -1
        except FileNotFoundError as t1:
            print('[Yuan_Qin]》》文件地址错误无法打开返回错误:',str(t1))
            show_error('[Yuan_Qin]','文件地址错误无法打开返回错误:'+str(t1))
            return -1
    #获取当前窗口进程
    def windows(self):
        # 获取当前激活窗口的句柄
        hwnd = win32gui.GetForegroundWindow()
        # 获取与激活窗口关联的进程ID
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        # 使用进程ID查找进程对象
        try:
            if not isinstance(pid, int) or pid <= 0:
                print('无效的进程ID')
            process = psutil.Process(pid)
            # 获取进程的名称
            process_name = process.name()
        except psutil.NoSuchProcess as f:
            process_name = 'none.exe'
        except ValueError:
            # 处理pid不是正整数的情况
            print("Error: PID must be a positive integer.")
            process_name = 'invalid_pid'  # 或者设置为其他适当的默认值
        except Exception as e:
            # 捕获其他可能发生的异常（可选）
            print(f"An unexpected error occurred: {e}")
            process_name = 'unknown_error'  # 或者设置为其他适当的默认值
        return process_name
    #获取所有窗口进程
    def windows_all(self):
        windosAll = []
        def winEnumHandler(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid > 0:
                    try:
                        process = psutil.Process(pid)
                        process_name = process.name()
                    except psutil.NoSuchProcess as f:
                        process_name = "Unknown"
                else:
                # print(f"窗口: {window_text}, 进程名称: {process_name}")
                    windosAll.append([None,None])
        win32gui.EnumWindows(winEnumHandler, None)
        return windosAll
    #主线程启动支持应用判断
    def ifwindowsON(self):
        windosw = self.windows_all()
        support = 0
        for a in windosw:
            if a[1] == 'YuanShen.exe':
                support+=1
        if support == 0:
            xiaoxi('Unable to find supporting applications','无法找到支持应用,请确保支持应用已开启或无视该信息继续使用')
        if support == 1:
            xiaoxi('welcome','系统已检测到支持应用打开')
    #倒计时计数器
    def timeon(self,go,to,txt):
        for quits in range(go,to):
            nums = to - quits
            print("\r",txt,"{}".format(nums),end="")
            time.sleep(1)
        print('\n')
    #键盘监听器
    def on_press(self,key):
        #功能列表
        functionset = ['Key.f1','Key.f2','Key.f3','Key.f4','Key.f5','Key.f6','Key.f7','Key.f8','Key.f9','Key.f10']
        keyname = str(key)
        if keyname in functionset:
            # try:
            #     b = ('{0}字符键'.format(keys.char))
            #     pass
            # except AttributeError:  
            # print('{0} 功能键'.format(keys))
            #F1方法定义
            if keyname == functionset[0]:
                self.state["yan"]["status"] = not self.state["yan"]["status"]
            #F2方法定义
            elif keyname == functionset[1]:#加速
                self.state["yan"]["speed"] += 50
                if self.fun2 != None:
                    self.fun2(self.state["yan"]["speed"])
                else:
                    print('\r                     |[Yuan_Qin]》》当前速度:,{}'.format(self.state["yan"]["speed"]),end='')
            #F3方法定义bsw
            elif keyname == functionset[2]:#减速
                if self.state["yan"]["speed"] >250:
                    self.state["yan"]["speed"] -= 50
                    if self.fun2 != None:
                        self.fun2(self.state["yan"]["speed"])
                    else:
                        print('\r                     |[Yuan_Qin]》》当前速度:,{}'.format(self.state["yan"]["speed"]),end='')
                elif self.state["yan"]["speed"] < 3500:
                    show_message_box('[Yuan_Qin]','当前速度已为最大')
            #F4方法定义
            elif keyname == functionset[3] and self.state["yan"]["tstatus"] == True:
                self.state["yan"]["processDown"] = 'quit'
            elif keyname == functionset[6] or keyname == functionset[7] or keyname == functionset[8] or keyname == functionset[9]:
                self.Last_time_key = keyname
            elif keyname == functionset[4] or keyname == functionset[5]:
                self.state["Back"] = 'Front' if keyname == functionset[4] else 'back'
                # show_message_box('key',self.Last_time_key)
    # 创建一个键盘监听器实例
    def listen_start(self):
        def listen():
            # a = True
            # while a == True:
            #     print('=-================')
            with Listener(
                on_press=self.on_press) as listener:  
                self.stop_event.wait()
                pass
        if self.thread is None:
            self.thread = threading.Thread(target=listen, daemon=True)
            self.thread.start()
    #窗口监听器实例
    def listfo_start(self):
        def listen2():
            while self.stop_event2:
                Check = self.windows()
                # print(Check)
                if Check != 'YuanShen.exe' and self.state["yan"]["jstatus"] == 0:
                    self.state["yan"]["status"] = False
                    self.state["yan"]["jstatus"] = 1
                elif Check == 'YuanShen.exe' and self.state["yan"]["jstatus"] == 1:
                    self.state["yan"]["status"] = True
                    self.state["yan"]["jstatus"] = 0
                time.sleep(0.5)
            self.state["yan"]["status"] = True
            self.state["yan"]["jstatus"] = 0
            self.stop_event2 = True
            # self.stop_event2.wait()CNA
        if self.thread2 is None:
            self.thread2 = threading.Thread(target=listen2,daemon=True)
            self.thread2.start()
    #关闭所有线程
    def stop(self):
        self.stop_event.set()
        self.stop_event2 = False
    #计算调整乐谱进度
    def jinduJS(self, jd, total_sum=None, data=None):
        if total_sum is None:
            total_sum = self.allkey  # 假设 self.allkey 是乐谱总长度或总音符数
        if data is None:
            data = self.musicup2  # 假设 self.musicup2 是乐谱数据的列表
    
        threshold = total_sum * (jd * 0.01)  # 计算达到当前进度百分比的音符总数
        current_sum = 0  # 当前已处理的音符总数
        index = -1  # 当前乐谱的索引，初始化为-1表示尚未找到
    
        # 遍历乐谱数据，找到达到或超过阈值的乐谱位置
        for i, sublist in enumerate(data):
            list_sum = len(sublist)  # 当前乐谱的音符数
            current_sum += list_sum  # 累加当前乐谱的音符数到已处理总数
            if current_sum >= threshold:
                self.index = i  # 更新当前乐谱索引
                js = list_sum - (threshold - current_sum)
                self.start = js if js >= 0 else 0
                break  # 找到后退出循环
        else:
            # 如果没有找到达到阈值的乐谱，则 self.index 可能保持为初始值或进行其他处理
            print("未达到乐谱末尾或指定进度百分比。")

    #开始演奏
    def musicstart(self,txt:list):

        if self.state["yan"]["local"] == True:
            pygame.init()
            # 初始化 mixer 模块，设置音频通道数和缓冲区大小（可选）
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(30)
            def play_local(play):
                local = [localkey for localkey in play if re.match(r'[a-zA-Z]',localkey)]
                for key in local:
                    sound = pygame.mixer.Sound(f"Audio/{key.upper()}.wav")
                    sound.play(loops=0)
        else:
            def play_local(play):
                keyboard.press_and_release(play)

        if self.fun is not None:
            def play_fun(funlist,funnum,play):
                funlist[funnum-1] = f'{funlist[funnum-1][0:-1]}>'
                ci2 = self.words[self.index]
                ci = ci2+'\n' if ci2!='' else ""
                self.fun(f'《《当前{self.index}行》》\n{ci}'+"".join(funlist))  # 假设这里调用 fun 并传入一个参数
        else:
            def play_fun(funlist,funnum,play):
                print('\033[2K\r当前行》》{}词:{}当前键符》》{}'.format(self.index,self.words[self.index],play),end='')
                #兼容性方法二
                # max_length = 50
                # print('\r当前行》》{}词:{}当前键符》》{}'.format(self.index, self.words[self.index], play).ljust(max_length), end='')


        if self.fun3 is not None:
            timers = RealTimeProgress()
            timers.progress()
            def fun3(js):
                self.fun3(js)
            def update_progress(times):
                timers.timer = js
        else:
            def fun3(js):
                pass
            def update_progress(times):
                pass

        os.system('cls')
        self.musicup2 = txt
        self.index = 0
        print('演奏已开始运行')
        # print('当前全局属性:',self.state)
        self.state["yan"]["tstatus"] = True
        self.allkey = count_elements(self.musicup2)
        while self.index < len(self.musicup2):
            allkey2 = count_elements(self.musicup2[0:self.index])
            if self.state["Back"] != None:
                if self.state["Back"] == 'Front':
                    if self.index + 3 <= len(self.musicup2)-1:self.index += 3
                elif self.state["Back"] == 'back':
                    if self.index - 3 >= 0:self.index -= 3
                self.state["Back"] = None
                continue
            play1 = self.musicup2[self.index]
            funlist = [item.replace('+', '')+'-▓' for item in play1 if not item.isdigit() and item != '']
            funnum = 0
            self.start = 0
            for i in range(self.start,len(play1)):
                if self.start != 0:
                    break
                allkey2 +=1
                js = int(allkey2 /self.allkey * 100)
                update_progress(js)
                fun3(js)
                if self.state["Back"] != None:break
                play = play1[i]
                # if self.gui:
                #     self.gui.key = play
                #演奏过程
                if re.match(r'[a-zA-Z]',play):
                    play_local(play)
                    # time.sleep(0.000001)
                    funnum += 1
                    play_fun(funlist,funnum,play)
                    # print('\r{}'.format('\n'),end='')
                    # print('\n')   
                elif play.isnumeric() == True:
                    # print(play)
                    # print(self.speed)
                    date = int(play)/self.state["yan"]["speed"]
                    time.sleep(date)
                #演奏退出
                if self.state["yan"]["processDown"] == 'quit':
                    break
                #演奏等待
                while self.state["yan"]["status"] == False:
                    if self.state["yan"]["processDown"] == 'quit':
                        break
                    time.sleep(0.5)
                self.start = 0
            if self.state["yan"]["processDown"] == 'quit':
                break
            self.index += 1
            funnum = 0
        if self.fun is not None:
            self.fun('《《演奏结束》》')
        self.state["yan"]["processDown"] = 'run'
        self.state["yan"]["tstatus"] = False
        # self.state["yan"]["local"] = False
        print('[Yuan_Qin]》》演奏已结束')
        return True
def music1():
#自带音乐起风了
    txt = """q 600 W 600 
B 300 D 300 E 300 R 300 E 300 
 V J 300 Z W  300 E 300 N 300 G 300 T 300 E 300 
 B W 300 X 300 M 300 W 300 E 300 
 N Y  300 E 300 W 300 H 300 D 300 N 300 S 300 D 300 
 N D H  600 
 Z G W 300 B 300 Q 300 A W 300 S 300 Q 300 
W 300 E 300 D T 300 E 300 
 M G W 300 B 300 Q 300 M W 300 S 300 Q 300 
W 300 E 300 W 280 Q 280 G 600 
 M G W 300 B 300 Q 300 M W  300 S 300 Q 300 
W 300 E 300  D T  300 E 300 

 V G W  300 A 300 E 300  G W  300  H Q  300 W 300 
W 600 
 X W  300 N 300 Q 300  F W  300 N 300 Q 300 
 B W  280 X E  280  M T  300 E 300 
 N W  300 C 300 E 320  M W  310 A Q 270 
 D H  600 E 270 W 270 Q 270 W 285 

 V Q  300 A 300 F 300  G E  300  H W  300 Q 300 W 300 
 B Q  300 X 300 B 300 M 300 D 300 S 300 A 300 
 Z S  300  B A  280 S 280 D 280 
 B A  280 S 300  Z M D  300 A 270 
 V D H  300  A G  300 H 300 H 600 A 340 
 B G J  285  X H  287 J 294 M 600 

 C G J  300  M H  300 J 300 G 300  M D  300 
 N Q 300 C 300 Q 300 A 300 H  300 G 300 
 V D H  300  Z G  300 H 300 N 300 G 300  A H  300 G 300 
 B H  300  X G  300 S 300 M 300 G 310 
 Z D  300 B 300 S 300 B 300 
A 300 S 300  Z M D  300 A 300 

 V D H  300  Z G  300 H 300 N 310 A 300 
 B G J  300  X H  300 J 300 M 600 
 C S G J  300 H 300  G J  300 B 300 D 300 
 N 300 G 300 Q 300 C 300 Q 300 A 300 H 300 G 300 
 V D H  300  Z E  300 E 300 N 300 G 300 
 B S H  300  X E  300 E 300 M 300 G 300 

 N D H  300 C 300 N 300 M 300 
 A D  600  N G Q  300 W 300 
 V H Q E  300  Z Y  300 T 300 N 300  Z Y  300  W T 
B 300  X Y  B 300 T 300 S 300 W  300 G 300 M
 C G E  300  C Y  300 T 300 B 300  M Y  300  Q T 
N 300  C Y  300 T 300 A 300 E 310 

 V G W  300  Z Q  300 H 300 N 300 Q 300 A 300 Q 300 
 B F W  300  X Q  300 H 300 M 300 Q 300 
 Z Q E  300 B 300 A 300 S 300  D R  300  G E  300 W 300 
 C E  300 W 300 C 300 B 300  M G Q  300 S 300 W 300 B 300 

 V H Q E  300  Z Y  300 T 300 N 300  Z Y  300  W T 
B 300  X Y  300  B W T  300 N 300 M 300 S 300 G 300 
 C G E  300  B Y  300  W T  300 S 300 Y 300  Q T 
N 300  C Y  300  M T 300 D E  300 H 300 D  300 

 V G W  300  Z Q  300 H 300 N 300 E 310 
 B G W  300 Q 300 H 300 Q 300 q 
  600 
V J 300 A W 300 E 300 F 300 G 300 T 300 E 300 
B W 300 S 300 G 600 

C J 300 M W 300 E 300 S 300 G 300 T 300 E 300 
N W 300 C Q 300 A J 300 Q 300 G 300 
V J 300 Z W 300 E 300 N 300 G 300 T 300 E 300 
B W 300 X 300 M 600 

C J 300 M W 300 Exbjw 300 S 300 G 300 T 300 E 300 
N W 300 C Q 300 A J 300 Q 300 W 300 T 300 
V J 300 A W 300 F E 300 G 300 T 300 E 300 
B W 300 S 300 G 600 

C J 300 M W 300 S E 300 G 300 T 300 E 300 
N W 300 C Q 300 A J 300 Q 300 G 300 
V J 300 Z W 300 N E 300 G 300 T 300 E 300 
B W 300 X 300 M 600 

C J 300 M W 300 S E 300 G 300 T 300 E 300 
N W 300 E 300 Q 300 W 300 J 300 Q 300 W 300 E 300 
W T U 600
    """
    with open('起风了.yq','w') as f:
        f.write(txt)
def music2():
    txt = """可莉：当你的天空突然下起了大雨
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 
b s q 270 100 100 50 w 270 100 100 z b q
270 w 270 e 270 r 270 e 270 100 50
可莉：那是我在为你炸乌云
w 270 q 270 v a q 270 270 t 270 270 v s q 
270 270 t 270 270 z b q 270 270 h 270 g 270
g 270 100
温迪：当你的发丝微乱有阵风吹过
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 
b s q 270 100 100 50 w 270 100 100 z b q 270 
w 270 e 270 r 270 e 270 100 50
温迪：那是我在远处想念你
w 270 q 270 v a q 270 270 t 270 270 v s q 
270 270 t 270 270 z b q 270 270 w 270 270
q 270 100 270 270
间奏~
v a q 270 100 270 v a 270 b s t 270 100
100 r 270 e 270 z b 270 270 z b 270 q 270 
w 270 e 270 q 270 v a q t 270 100 270 v a 270 b 
s 270 270 q y 270 q t 270 z b q y 270 q t 270 z b
270 q 270 w 270 e 270 t 270 v a q t 270 100 
270 v a 270 b s 270 270 q r 270 q e 270 z b 270 270
z b 270 q 270 w 270 e 270 q 270 v a q e 270 270
v a 270 b s 270 r 270 e 270 q 270 z b 270
270 270 270 270
可莉：你还在忙吗，还是在摸鱼，我看看！
a d 270 100 100 q 270 100 100 a d 270 q 270 100
a d 270 a s 270
可莉：哇！好大一条！
q 270 100 h 270 q a s 270 w 270 q 270 270
可莉：内个~摸完能不能借我炸一下！嘻嘻
a f 270 100 100 q 270 100 100 a f 270 q 270 
100 a f 270 a d 270 q 270 100 h 270 q a d 270 
w 270 q 270 270
可莉：看起来你怎么不开心
z 270 t 100 e 100 50 50 25 z e 100 25 e 100 50 50 50 
b w 100 50 50 e 100 50 w 100 50 b 100 50 50 q 100 50 
q 270
可莉：虽然不知道发生了什么
z 270 t 100 e 100 50 50 25 z e 100 25 e 100 50 50 50
b w 100 50 50 e 100 50 w 100 50 b 100 50 50 q 
100 50 q 270
可莉：吃饱了再去想吧
v a 270 g 270 v a h 270 q 270 b s r 270
魈：这东西，能吃么？
e 270 z b w 270 q 270 270 100
合：烦恼都走开，烦恼都走开！
q 100 50 q 50 100 v a q 100 50 q 100 50 t 270 b 
s q 100 50 q 100 50 q 50 100 q 100 50 b s t 270 270
合：加班都走开，加班都走开！
z b 100 100 q 100 50 q 50 100 z b q 100 50 q 100 50
t 270 z b q 100 50 q 100 50 q 50 100 q 100 50
z b t 270 270
合：倒霉都走开，倒霉都走开！
v a 100 100 q 100 50 q 50 100 v a q 100 50 q 100
50 t 270 b s q 100 50 q 100 50 q 50 100 q 100
50 b s t 270 270
合：呼~~~
z b 270 g 270 z b h 270 q 270 z b r 270 e 270 z
b w 270 q 270
合：坏人都走开，坏人都走开！
v a 100 100 q 100 50 q 50 100 v a q 100 50 q 100 
50 t 270 b s q 100 50 q 100 50 q 50 100 q 100 50
b s t 270 270
合：尴尬都走开，尴尬都走开！
z b 100 100 q 100 50 q 50 100 z b q 100 50 q 100 50
t 270 z b q 100 50 q 100 50 q 50 100 q 100
50 z b t 270 270
合：史莱姆走开，史莱姆走开！
v a 100 100 q 100 50 q 50 100 v a q 100 50 q 100 50
t 270 b s q 100 50 q 100 50 q 50 100 q 100 50
b s t 270 270
合：唉~~~
z q 270 270 270
可莉：当你的天空突然下起了大雨
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 b s
q 270 100 100 50 w 270 100 100 z b q 270 w 270
e 270 r 270 e 270 100 50
可莉：那是我在为你炸乌云
w 270 q 270 v a q 270 270 t 270 270 v s q 270 270
t 270 270 z b q 270 270 h 270 g 270 g 270 100
温迪：当你的发丝微乱有阵风吹过
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270
b s q 270 100 100 50 w 270 100 100 z b q 270
w 270 e 270 r 270 e 270 100 50
温迪：那是我在远处想念你
w 270 q 270 v a q 270 270 t 270 270 v s q 270 270 
t 270 270 z b q 270 270 w 270 270 q 270 100 270
270 q 270 270 v t 270 270 270 270 b 270 270 270
270 z 270 270 270 270 r 100 100 e 270 270
w 100 100 q 270
间奏
v 270 270 t 270 270 b 270 270 270 270 z 270 270
270 q 100 100 j 100 100 q 270 270 v 270 270 t 270
270 b 270 270 270 270 z 270 270 270 270
七七：啊，轮到我了
r 100 100 e 270 270 w 100 100 q 270 v 270 270 t
270 270 b 270 270 270 270 z b q e 270 270 270 270
七七：你在忙吗，还是在摸鱼，我看看
z b 270 270 z b 270 270 q 100 w 100 e 270 e 100
r 100 v a t 270 270 v a 270 270 b s r 270 100
b s r 270 270 z b e 270 270 270
七七：哇，好大一条！
z b 270 270 270 z b a d 270 270 270 s f 270 270
z b d g 270 270 270 270 z b 270 270 z b 270 270
七七：内个~摸完能不能借她炸一下，嘿嘿
q 100 w 100 e 270 e 100 r 100 v a t 270 270 100
v a 270 270 100 b s e 100 r 100 e 100 w 100 q
100 h 100 z b g 270 270 270 z b 270 270
七七：啊，唱不完了
z b s f 270 270 270 z b a d 270 270 270
魈：不见万家灯火，尽斩世间妖魔
z v 270 270 50 a 100 50 n 100 100 50 a 100 50 a
50 100 a 50 100 50 s 100 50 50 100 c b d 270 270
d 100 50 s 100 100 50 d 100 50 d 50 100 d 100 50
50 j 100 50 50 100 q v n 270 270
魈：如此一切只为苍生不要想太多
a 100 50 n 100 100 50 a 100 50 25 a 25 50 100 a 
50 100 50 s 100 50 50 100 d v n 270 f 270 d 270
f 270 g b m 270 a 270 a 270 270
魈：平凡的起起落落，漂浮的因果对错
z v 270 270 50 a 100 50 n 100 100 50 a 100 50 a 
100 50 a 50 100 50 s 100 50 50 100 c b d 270 270
d 100 50 s 100 100 50 d 100 50 d 100 50 d 100 50
50 j 100 50 50 100 q v n 270 270
魈：都可以向风诉说
q 100 50 h 100 25 b m q 100 50 50 h 100 25 q 100
100 25 h 100 50 z b q 270 270
可莉：当前面太多阻碍看不到对岸
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 b
s q 270 100 100 50 w 270 100 100 z b q 270 w 
270 e 270 r 270 e 270 100 50
可莉：请替我保密，我为你炸平
w 270 q 270 v a q 270 270 t 270 270 v s q 270
270 t 270 270 z b q 270 270 h 270 g 270 g 270 100
七七：虽然我讨厌热乎乎的东西
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 b
s q 270 100 100 50 w 270 100 100 z b q 270 w
270 e 270 r 270 e 270 100 50
七七：我却想要拥抱你
w 270 q 270 v a q 270 270 t 270 270 v s
q 270 270 t 270 270
七七：可以吗？
z b q 270 270 w 270 270 q 270 100 270 270
主题曲：哒哒~哒哒哒~哒哒哒哒~哒~哒哒哒哒~哒~哒哒哒哒哒~~~
g 270 50 z 50 b 50 q 270 270 270 270 w 270 270 e
270 270 n 50 z 270 270 t 270 50 e 50 270 w 50 270
e 50 b 50 z 270 270 270 270 w 50 270 q 270 50 b
50 s 50 w 270 270 h 270 270 270 270 v 50 a 50 q
270 270 270 270 q 270 270 w 270 50 b 50 s 50 j
270 270 h 270 270 270 g 270 270 270 270
魈：如果你迷恋岁月舍不得向前
e 270 w 270 q 270 270 q v 270 50 g 270 50 q
270 50 g 270 50 b q 270 100 100 50 50 w 270 50 
100 100 z q 270 50 w 270 e 270 r 270 e 270 100 50
魈：我就默默记录这诗篇
w 270 50 q 270 50 v a q 270 270 50 t 270 270 50 b
q 270 270 50 t 270 270 50 z q 270 270 50 h 270
50 g 270 50 g 50 270 100
温迪：如果你厌倦引力想要去飞行
e 270 w 270 q 270 50 q v a 270 50 g 270 50 q 270
50 g 270 50 b s q 270 100 100 50 50 w 270 50 100
100 z b q 270 50 w 270 e 270 r 270 e 270 100 50
温迪：我就让，全世界的风吹向你
w 270 50 w 270 50 q 270 100 v a q 270 50 100 q 
270 50 b s t 270 50 r 270 50 e 270 50 q 270 50 z 
b q 270 270 270 w 270 270 270 z 270 b 270 q
"""
    with open('让风告诉你.yq','w') as f:
        f.write(txt)
#图标数据
icon = """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"""

class tx:
    def __init__(self):
        self.filepathtext = None
        self.root = tk.Tk()
        self.root.resizable(False,True)
        self.custom_font = font.Font(family="Helvetica", size=12)
        try:#应用图标
            from tkinter import PhotoImage
            icon_image = PhotoImage(data=icon)
            self.root.iconphoto(False, icon_image)
        except:
            pass
        self.slider = None
        #更新进度方法
        def updata_slider(event):
            self.slider.set(event)
            self.label['text'] = "[Yuan_Qin]》》", f'当前速度值{event/1000}倍速'
        self.root.title('Yuan_Qin')
        self.root.geometry("400x300")
        self.shudu = 1000
        self.stoptime = 2
        self.root.wm_attributes('-topmost',1)
        def updata_key(key):
            self.key.set(key)
        def upjindu(key):
            self.Scale2.set(key)
        self.music = musickey(fun = updata_key,fun2 = updata_slider,fun3 = upjindu)
        self.app_listen = False
        self.key = tk.StringVar()
        self.key.set('正在加载...')
        self.canvasw = 100
        self.tkstarts = False
        self.var = [tk.IntVar(),tk.IntVar()]
        self.scale_value = tk.DoubleVar()
        self.ifwords = False
    #滑动播放速度上传模块
    def on_scale_move(self,event):
        # print(f"Slider value: {event}")
        self.shudu = float(event)
        self.music.state["yan"]["speed"] = self.shudu
        # print(f'当前速度值{self.music.speed/1000}倍速')
        self.label['text'] = "[Yuan_Qin]》》", f'当前速度值{self.music.state["yan"]["speed"]/1000}倍速'
    #滑动等待速度上传模块
    def on_scale_move_tow(self,event):
        self.stoptime = float(event)
    def on_scale_move_three(self):
        self.app_listen = bool(self.var[0].get())
    #本地演奏模式启动模块
    def local_music(self):
        print(self.var[1].get())
        self.music.state["yan"]["local"] = bool(self.var[1].get())
    def on_scale_change(self, event):
        # 当滑块值变化时，调用 jinduJS 并传递当前值
        self.music.jinduJS(self.scale_value.get())
    #启动模块
    def start_all_sh(self):
        self.music.listen_start()
        if self.app_listen == True:
            self.music.listfo_start()
        else:
            all_threads = threading.enumerate()
            # 打印所有线程的名称和标识符
            for thread in all_threads:
                if thread.name == 'Thread-9 (listen2)':
                    self.music.stop_event2 = False
        self.menu2.destroy()
        self.menu2 = tk.Menu()
        self.menu2.add_cascade(label="关于", menu=self.menu_version())
        self.menu2.add_cascade(label="退出至界面", menu=self.menu_rustart())
        self.root.config(menu=self.menu2)
        # music.listfo_start()
        self.music.state["txif"] = True
        self.music.state["datestop"] = self.stoptime
        self.label2.destroy()
        self.slider2.destroy()
        self.btn2.destroy()
        self.check.destroy()
        self.checkAI.destroy()
        self.seek_label.destroy()
        self.seek_btn.destroy()
        self.root.geometry("600x300")
        self.label['text'] = "[Yuan_Qin]》》", f'当前速度值{self.music.state["yan"]["speed"]/1000}倍速'
        self.TScale2 = tk.Label(self.root,text="当前进度").pack()
        self.Scale2 = tk.Scale(self.root,from_=0,to=100,orient=tk.HORIZONTAL,resolution=1,length=600,variable=self.scale_value)
        self.Scale2.bind("<ButtonRelease-1>", self.on_scale_change)
        self.Scale2.set(0)
        self.Scale2.pack()
        self.labelkey = tk.Label(self.root,textvariable=self.key)
        self.labelkey.pack(anchor='sw')
        txts = self.music.txtimport(self.filepathtext)
        if txts == -1:
            xiaoxi('[Yuan_Qin]》》','曲谱无法编译,未知错误')
        else:
            #加载演奏
            stop = self.music.musicstart(txts)
            if stop == True:
                self.rustart(event=False)
    #文件上传模块
    def filepath(self,event = None):
        if self.filepathtext == None:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="选择一个文件",  # 对话框的标题
                filetypes=[("Text files", "*.yq"), ("All files", "*.*")]  # 可选择的文件类型
            )
            if file_path:
                self.filepathtext = file_path
            else:
                self.filepathtext = None
            if self.filepathtext != None:
                print(self.filepathtext)
                show_message_box('File',f'你已成功选择{self.filepathtext}文件')
                if os.path.exists('history.json'):
                    with open('history.json','r',encoding='utf-8') as f:
                        try:
                            self.nextjson = json.load(f)
                        except json.JSONDecodeError:
                            self.nextjson = {}
                        f.close()
                with open('history.json','w+',encoding='utf-8') as fs:
                    filename = os.path.basename(self.filepathtext)
                    self.nextjson[filename] = self.filepathtext
                    fs.write(json.dumps(self.nextjson, ensure_ascii=False, indent=4))
                center = {'key':filename,'value':self.filepathtext}
                self.initTextCenter(center=center,filego=False)
        if self.filepathtext != None:
            self.Preload()
    #更新应用
    def getupdate(self):
        import requests
        import webbrowser
        url = 'http://10.25.3.66:5000/updata'
        url2 = 'http://127.0.0.1:5000/updata'
        try:
            cent = requests.get(url2,timeout=2)
            if cent.status_code == 200:
                cent.encoding = 'utf-8'
                version_info = json.loads(cent.text)
                if version_info['version'] > version:
                    updataif = messagebox.askyesno('Update',f'发现新版本{version_info["version"]}，是否更新？\n更新内容：{version_info["content"]}\n发布时间:{version_info["time"]}')
                    if updataif:
                        webbrowser.open(version_info["url"])
                    else:
                        pass
            else:
                xiaoxi('[Yuan_Qin]》》','获取失败!,请检查网络连接')
        except requests.exceptions.RequestException:
            show_message_box('Error','获取失败,请检查网络连接')
            # xiaoxi('[Yuan_Qin]》》','获取失败!,请检查网络连接')
    #预加载模块
    def Preload(self):
        self.seek_label.destroy()
        self.seek_btn.destroy()
        self.menu.destroy()
        self.freePlay.destroy()
        self.menu2 = tk.Menu()
        self.menu2.add_cascade(label="关于", menu=self.menu_version())
        self.menu2.add_cascade(label="退出至界面", menu=self.menu_rustart(event=False))
        self.root.config(menu=self.menu2)
        self.label['text'] = '选择初始数值'
        self.label.pack(anchor='n')
        self.btn1.destroy()
        self.slider = tk.Scale(self.root, from_=200, to=2500, orient=tk.HORIZONTAL, resolution=200, command=self.on_scale_move,length=600,tickinterval=400)
        self.slider.set(1000)  # 设置默认值为50
        self.slider.pack()
        self.label2 = tk.Label(self.root,text='等待时间,初始等待时间为2s')
        self.label2.pack()
        self.slider2 = tk.Scale(self.root, from_=0, to=30, orient=tk.HORIZONTAL, resolution=1, command=self.on_scale_move_tow,length=600,tickinterval=2)
        self.slider2.set(2)  # 设置默认值为50
        self.slider2.pack()
        self.check = tk.Checkbutton(self.root,text="开启应用监听",variable=self.var[0],command=self.on_scale_move_three)
        self.check.pack()
        self.checkAI = tk.Checkbutton(self.root,text="离线演奏",variable=self.var[1],command=self.local_music)
        self.checkAI.pack()
        self.btn2 = tk.Button(self.root, text="开始", command=lambda :threading.Thread(target=self.start_all_sh).start())
        self.btn2.pack()
        self.root.geometry("800x400")
        self.root.resizable(False,False)
    #创作保存
    def save_txt(self,filename):
        text_content = self.text.get('1.0', tk.END)
        with open(filename,'w',encoding='utf-8')as f:
            f.write(text_content)
        xiaoxi('[Yuan_Qin]》》','已保存当前作曲')
        self.rustart(event=False)
    #预览创作与修改
    def sekk_filepath(self,event = None):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="选择一个文件",  # 对话框的标题
            filetypes=[("Text files", "*.yq"), ("All files", "*.*")]  # 可选择的文件类型
        )
        if file_path:
            self.root.geometry("800x600")
            for widget in self.root.winfo_children():
                widget.destroy()
            with open(file_path,'r+',encoding='utf-8') as f:
                txt = f.read()
            self.text = tk.Text(self.root,wrap=tk.WORD)
            self.save = tk.Button(self.root,text='保存',command=lambda:self.save_txt(filename=file_path))
            self.save.grid(row=0,column=0,sticky='ew')
            self.quit = tk.Button(self.root,text='退出',command=lambda:self.rustart(event=False))
            self.quit.grid(row=0,column=1,sticky='ew')
            self.text.grid(row=1, column=0, columnspan=2, sticky='nsew')
            self.text.insert(tk.END,txt)
    #传入历史歌单路径
    def initTextCenter(self,center,filego = True):
        if os.path.exists(center["value"]):
            if filego:
                self.filepathtext = center["value"]
            # 然后插入原字典中剩余的键值对
            new_dict = {}
            new_dict.update({k: v for k, v in self.nextjson.items() if k != center["key"]})
            new_dict[center["key"]] = center["value"]
            with open('history.json','w+',encoding='utf-8') as ffs:
                ffs.write(json.dumps(new_dict, ensure_ascii=False, indent=4))
                ffs.close()
            if filego:
                self.filepath()
        else:
            xiaoxi('[Yuan_Qin]》》','文件已经不存在了')
            del self.nextjson[center["key"]]
            with open('history.json','w+',encoding='utf-8') as fs:
                fs.write(json.dumps(self.nextjson, ensure_ascii=False, indent=4))
            self.rustart(event=False)
    #主见面菜单栏
    def create_menu(self):
        if os.path.exists('history.json'):
            with open('history.json','r+',encoding='utf-8') as f:
                try:
                    self.nextjson = json.load(f)
                except json.JSONDecodeError:
                    self.nextjson = {}
                f.close()
        else:
            self.nextjson = {}
        menu = tk.Menu()
        menu.add_command(label="近期歌曲")
        menu.add_separator()
        i = 0
        for key,value in reversed(list(self.nextjson.items())):
            dicts = {'key':key,'value':value}
            func = lambda center = dicts:self.initTextCenter(center)
            menu.add_command(label=key[:-3], command=func)
            if i == 10:
                break
            i += 1
        return menu
    #退出至主界面菜单栏列表
    def menu_rustart(self,event = None):
        menu2 = tk.Menu()
        menu2.add_command(label='退出至主界面', command=lambda:self.rustart(event=event))
        menu2.add_command(label='退出至应用', command=lambda:quit())
        return menu2
    #关于菜单栏列表
    def menu_version(self):
        menu3 = tk.Menu()
        menu3.add_command(label=f'当前版本{version}')
        menu3.add_command(label=f'版本迭代{versionid}')
        menu3.add_command(label='检查更新', command=self.getupdate)
        return menu3
    #自由演奏模式练习模式数据加载模块
    def practicevalue_update(self,event):
        if self.practiceindex >= len(self.practice_txt):
            self.practice_txt = ''
            self.keylabelValue.set('练习模式结束')
            self.seek = 0
            self.practiceindex = 0
            return self.practice_txt
        local = [localkey for localkey in self.practice_txt[event] if re.match(r'[a-zA-Z]',localkey)]
        funlist = [item.replace('+', '') for item in local if item != '']
        self.practicetxt = ' '.join(funlist)
        self.practicevalue.set(self.practicetxt)
        self.practice_len += len(self.practicetxt.replace(' ',''))
    #自由演奏模式练习模式启动模块
    def free_music_practice(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="选择一个文件",  # 对话框的标题
            filetypes=[("Text files", "*.yq"), ("All files", "*.*")]  # 可选择的文件类型
        )
        if file_path:
            self.root.geometry("600x300")
            self.music.state["txif"] = True
            self.practice_txt = self.music.txtimport(file_path)
            self.keyAll = ''
            self.keylabelValue.set('请开始你的表演')
            self.practicevalue = tk.StringVar()
            self.practicevalue.set('待加载...')
            self.practiceindex = 0
            self.practice_len = 0
            self.practicevalue_update(self.practiceindex)
            self.practice = tk.Label(self.root,textvariable=self.practicevalue,anchor='w',font=self.custom_font)
            self.practice.grid(row=1,column=0,sticky='nsew')
            self.frame = tk.Frame(self.root,height=2,relief=tk.SUNKEN,bd=1)
            self.frame.grid(row=2,column=0,sticky='nsew')
            self.ifwords = True
    #主引导模块
    def homes(self):
        self.root.resizable(False,False)
        self.menu = tk.Menu()                       #创建菜单
        self.root["menu"] = self.menu               #把菜单放置在窗口中（菜单条）
        self.menu.add_cascade(label="历史歌单", menu=self.create_menu())
        self.menu.add_cascade(label="关于", menu=self.menu_version())
        self.label = tk.Label(self.root,text='请输入目标乐谱存放地,以做运行曲谱')
        self.label.pack(anchor='sw')
        self.btn1 = tk.Button(self.root, text="获取文件", command=self.filepath)
        self.btn1.pack(anchor='sw')
        self.seek_label = tk.Label(self.root,text='选择一个文件查看曲谱内容或更改')
        self.seek_label.pack(anchor='sw')
        self.seek_btn = tk.Button(self.root, text="获取文件", command=self.sekk_filepath)
        self.seek_btn.pack(anchor='sw')
        self.freePlay = tk.Button(self.root, text="自由演奏模式", command=self.free_music)
        self.freePlay.pack(anchor='sw')
        # self.seek_btn2 = tk.Button(self.root, text="创建新文档", command=self.filepath)
        # self.seek_btn2.pack()
    #自由演奏模式启动模块
    def free_music(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.menu2 = tk.Menu()
        self.menu2.add_cascade(label="关于", menu=self.menu_version())
        self.menu2.add_cascade(label="退出至界面", menu=self.menu_rustart(event=False))
        self.menu2.add_command(label="练习模式/获取乐谱",command=lambda:self.free_music_practice())
        self.root.config(menu=self.menu2)
        self.root.geometry("400x400")
        self.root.resizable(False,True)
        self.keylabelValue = tk.StringVar()
        self.keylabelValue.set('待输入...')
        self.keyAll = ''
        self.seek = 0
        self.keyMiusic = []
        def keyMiusicUpData(event):
            self.keyMiusic.append(event)
            
        def keyMiusicUpData_stop(Fplay):
            Fplay.new.save_key()
            if len(self.keyMiusic) > 0:
                self.keyMiusic[-1].append("400")
            else:
                self.keyMiusic[0].append(['400'])
            toSring = ""
            for row in self.keyMiusic:
                musicSring = ' '.join(row)+'\n'
                toSring += musicSring
            print('[Yuan_Qin]》》已保存键位记录')
        def keydata(event):
            if event != "":
                self.keyAll += event
                self.keylabelValue.set(''.join(reversed(list(self.keyAll[-20:]))))
                if self.ifwords:
                    self.seek += 1
                    k = ""
                    n = 0
                    p = False
                    for t in range(0,len(self.practicetxt)):
                        i = self.practicetxt[t]
                        if i == ' ':k += i
                        else:
                            if n == self.seek:
                                l = t
                                while True:
                                    if l < len(self.practicetxt):
                                        if l == t:
                                            k += '|'+ i
                                            l += 1
                                        else:
                                            if self.practicetxt[l] == ' ':
                                                break
                                            else:
                                                k += self.practicetxt[l]
                                                l += 1
                                                p = True
                                    else:
                                        break
                                k += '| '
                            else:
                                if p != True:
                                    k += i
                                else:
                                    p = False
                            n += 1
                    self.practicevalue.set(k)
                    try:
                        if len(self.keyAll.replace(' ','')) >= self.practice_len:
                            self.practiceindex += 1
                            self.practicevalue_update(self.practiceindex)
                            self.seek = 0
                    except:
                        pass
        self.keylabel = tk.Label(self.root,textvariable=self.keylabelValue,anchor='w',font=self.custom_font)
        self.keylabel.grid(row=3,column=0,sticky='nsew')
        self.Fplay = Listener_listen_key_test(keydata,keyMiusicUpData)
        self.Fplay.listen_on_start()
        self.buttonSave = tk.Button(self.root,text="保存演奏记录",command=lambda:keyMiusicUpData_stop(Fplay=self.Fplay))
        self.buttonSave.grid(row=4,column=0,sticky='nsew')
    #自由演奏模式停止模块
    def free_music_stop(self):
        self.Fplay.listen_on_stop()
    #重置模块
    def rustart(self,event = None):
        if event == None:
            self.music.state["yan"]["processDown"] = 'quit'
            self.tkstarts = True
        #判断是否为程序调用,如果是判断是否为GUI引起的关闭,如果不是GUI引起的关闭则重新加载GUI,如果是GUI引起的关闭则程序不进行重置
        if event == False and self.tkstarts == True:
            self.tkstarts = False
        else:
            for widget in self.root.winfo_children():
                # print(type(widget).__name__)
                widget.destroy()
            self.root.geometry("400x300")
            self.root.resizable(False,True)
            self.homes()
        # self.music.state['yan']['local'] = False
        self.app_listen = False
        self.filepathtext = None
        try:
            self.free_music_stop()
        except:
            pass
        print(self.music.state)
        self.ifwords = False
    #GUI启动
    def start(self):
        self.homes()
        self.root.mainloop()
import os
#创作模式
class MusicCreate():
    #初始化
    def __init__(self):
        self.Cmusic = musickey()
        self.returnKey = self.Cmusic.Last_time_key
        self.musictxt = []
        # self.stop_event3 = threading.Event()
    #定义删除上一行
    def out(self):
        key = len(self.musictxt)-1
        drop_prompt = self.musictxt[key]
        self.musictxt.pop(key)
        print(f'[Yuan_Qin]》》已删除{drop_prompt}')
    #定义选择删除功能
    def down(self):
        drop_prompt = None
        def dropd(num):
            while True:
                drop = input(f'请输入删除的列数[1-{num-1}],退出请下一步:')
                if drop == '':
                    break
                try:
                    drop = int(drop)
                    if drop >= 1 and drop <= num-1:
                        break
                    else:
                        print(f'[Yuan_Qin]》》请输入[1~{num-1}]数字有效范围的值:')
                except ValueError:
                    print(f'[Yuan_Qin]》》请输入[1~{num-1}]数字范围的值:')
            return drop
        while True:
            os.system('cls')
            if drop_prompt != None:
                print(f'[Yuan_Qin]》》成功删除{drop_prompt}')
            print('[Yuan_Qin]》》进入删除模式:')
            print('[Yuan_Qin]》》已写入\n')
            nums = 1
            for drops in self.musictxt:
                print(f'li-{nums}>>'+drops)
                nums += 1
            drop = dropd(nums)
            if drop == '':
                break
            drop_prompt = self.musictxt[drop-1]
            self.musictxt.pop(drop-1)
            
    # def keylist_start(self):
    #     def key():
    #         while True:
    #             if music.Last_time_key == 'Key.f5':
    #                 self.down()
    #                 # self.stop_event3.wait()
    #             # time.sleep(0.3)
    #     self.thread3 = threading.Thread(target=key,daemon=True)
    #     self.thread3.start()
    #创作模式流程维持功能
    def create(self):
        # self.keylist_start()
        os.system('cls')
        print(f'''****************创作须知******************
    [Yuan_Qin]》》请选择需要发声键进行输入,每个发声键与速度使用空格进行隔开
    [Yuan_Qin]》》初始化默认速度为乐谱速度/1000
    [Yuan_Qin]》》为使美观可以写完一句一行,不要求强制换行,写完单句后回车自动保存,无内容时回车自动退出
    [Yuan_Qin]》》(当前为{version}版本创建功能暂不支持功能键,敬请期待!)
    [Yuan_Qin]》》创建功能按键=>>选择删除一整行F7或输入/d、删除上一段编写F8或输入/a、完全测试F9、选行测试F10
    [Yuan_Qin]》》创作规范例示"B 300 D 300 E 300 R 300 E 300 "''')
        while True:
            SaveFilepPhat = str(input('[Yuan_Qin]》》请输入乐谱保存地址:you file name:'))
            mode = str(input('追加A,覆盖W,默认追加模式:')).lower()
            if mode != 'w' or mode != 'a':
                if mode == '':
                    mode == 'a'
            if SaveFilepPhat == '':
                print('[Yuan_Qin]》》请输入一个文件存储地址:')
            else:
                break
        # index = 0
        while True:
            os.system('cls')
            # print(self.returnKey)
            txt = ""
            txtobserve = ""
            nums = 1
            for miui in self.musictxt:
                txt = txt + miui
                txtobserve = txtobserve + f'li-{nums}>>' + miui
                nums += 1
            with open(SaveFilepPhat+'.yq',mode) as fs:
                if len(txt) != 0:
                    fs.write(txt)
                fs.close()
            print(f'[Yuan_Qin]》》编辑已完成\n--------------------------------\n{txtobserve}--------------------------------\n')
            # if self.returnKey == 'Key.f5':
            #     self.down()
            NewMusic = str(input(f'[Yuan_Qin]》》len-{nums}>>')) + '\n' # index
            self.musictxt.append(NewMusic)
            if NewMusic == '\n':
                self.musictxt.pop(len(self.musictxt)-1)
                break
            elif NewMusic == '/d\n':
                self.musictxt.pop(len(self.musictxt)-1)
                self.down()
            elif NewMusic == '/a\n':
                self.musictxt.pop(len(self.musictxt)-1)
                self.out()
            # print(NewMusic,'\n',self.musictxt)C
            # index+=1
class flow_path():
    def __init__(self,music):
        self.music = music
    #启动所有线程
    def all_sh(self):
        self.music.listen_start()
        self.music.listfo_start()
    #加载乐谱
    def home(self):
        while True:
            musicfilename = str(input('[Yuan_Qin]》》请输入目标乐谱存放地,创建新琴谱请下一步,退出请输入q:'))
            if musicfilename.lower() =='q':
                os.system('cls')
                print('''
                            .&______~*@*~______&.           *
                        "w/%%%%%%%%%%%%%%%%%%%\w"        ***
                            `Y""Y""Y"""""Y""Y""Y'         *****
        __/M__          p-p_|__|__|_____|__|__|_q-q      **Y**
    ____|O_^_O|_________[EEEEM==M==MM===MM==M==MEEEE]-__....|....
    ''')
                print('[Yuan_Qin]》》感谢使用,期待你的下次再见!!!')
                xiaoxi('[Yuan_Qin]》》','应用已结束运行')
                self.music.timeon(0,5,'[Yuan_Qin]》》退出倒计时')
                quit()
            elif musicfilename == '':
                print('GO')
                # music.listen_start()
                MusicCreate().create()
            else:
                #加载局内功能按键
                iflix = input('[Yuan_Qin]》》是否使用离线播放')
                if iflix.lower() == 'y':
                    music.state["yan"]["local"] = True
                    print('[Yuan_Qin]》》已启用离线播放模式')
                else:
                    self.all_sh()
                while True:
                    try:
                        dates = input('[Yuan_Qin]》》当前默认速度为【乐谱速度/1000】,若要调整请输入[250~3000],不调整请下一步:')
                        if dates == '':
                            break
                        elif int(dates) >250 and int(dates) <3000:
                            self.music.state["yan"]["speed"] = int(dates)
                            break
                        show_error('[Yuan_Qin]','请输入[250~3000]范围内的整数')
                    except ValueError as t3:
                        show_error('[Yuan_Qin]','输入整数返回错误:'+str(t3))
                txts = self.music.txtimport(musicfilename)
                if txts == -1:
                    pass
                else:
                    #加载演奏
                    self.music.musicstart(txts)
# n = musickey()
# t = n.txtimport('起风了.yq')
# print(t)
if __name__ == '__main__':
    #默认乐谱
    if(not os.path.exists('起风了.yq')):
        music1()
    if(not os.path.exists('让风告诉你.yq')):
        music2()
    
    # #确认是否启用图形化界面
    def ask_yesno():
        mode = messagebox.askyesno(title="确认", message="是否启用图形化界面")
        return mode
    mode = ask_yesno()
    music = musickey()
    if mode == True:
        #启动图形化界面
        tx().start()
    else:
        #启动监听线程
        music.ifwindowsON()
        #启动Shell引导界面
        flow_path(music).home()
    #停止监听线程
    music.stop()