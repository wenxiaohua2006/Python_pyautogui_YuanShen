try:
    from pyautogui import keyDown,keyUp,press
    from pynput.keyboard import Listener
    import threading
    import time
    import re
    import os
    import win32gui
    import win32process
    import psutil
    import tkinter as tk  
    from tkinter import messagebox
    print('依赖库正常导入')
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
#弹窗提示
def show_message_box(title,add):  
    root = tk.Tk()
    # 隐藏主窗口  
    root.withdraw()
    messagebox.showinfo(title, add)  
    root.destroy()

version = 'Yuan_Qin-version:0.1.11'
versionid = 1
print(f'''******************************欢迎使用键琴演奏******************************
                       当前版本:{version}
                                  迭代ID:{versionid}
                            ******使用须知******
                            使用自创乐谱请规范格式
                            详细请看自带乐谱起风了.txt
---版本计划:0.1.12进行按键同步优化,0.2.13创作功能大更新,0.3.14新用户界面大更新,0.3.15深度代码层优化
---0.4.16大更新接入HTML网页,1.5.17新创作模式游戏乐曲离线播放,2.9.1最终优化,3.1.1乐谱纠错和创造模式接入AI,9.9.10最终版本
局内按键使用:F1暂停/继续演奏       F2速度-0.2      F3速度+0.2     F4结束演奏''')
class musickey():
    def __init__(self):
        #局内调整器
        self.status = True    #进程
        self.speed = 2000    #速度
        self.processDown = 'run'    #进程结束
        self.stop_event = threading.Event()
        self.stop_event2 = threading.Event()
        self.jstatus = 0
        self.Last_time_key = None
    #乐谱导入处理
    def txtimport(self,file):
        try:
            with open(file,'r+') as f:
                txt = f.read()
            #处理乐谱
            txt_split = txt.split('\n')
            music = []
            for txtn in txt_split:
                MusicList = txtn.split(' ')
                for detection in MusicList:
                    if detection != '':
                        music.append(detection)
            date = input('[Yuan_Qin]》》乐谱已处理完成,请输入等待开始时间')
            if date == '':
                date = 2
            time.sleep(float(date))
            return music
        except UnicodeDecodeError as t2:
            print('[Yuan_Qin]》》无法打开文件,请确保文件内容只有字键和数字,返回错误:',t2)
            show_message_box('[Yuan_Qin]','无法打开文件,请确保文件内容只有字键和数字,返回错误:'+t2)
            return -1
        except FileNotFoundError as t1:
            print('[Yuan_Qin]》》文件地址错误无法打开返回错误:',str(t1))
            show_message_box('[Yuan_Qin]','文件地址错误无法打开返回错误:'+str(t1))
            return -1
    #获取当前窗口进程
    def windows(self):
        # 获取当前激活窗口的句柄
        hwnd = win32gui.GetForegroundWindow()
        # 获取与激活窗口关联的进程ID
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        # 使用进程ID查找进程对象
        try:
            process = psutil.Process(pid)
            # 获取进程的名称
            process_name = process.name()
        except psutil.NoSuchProcess as f:
            process_name = 'none.exe'
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
            show_message_box('Unable to find supporting applications','无法找到支持应用,请确保支持应用已开启或无视该信息继续使用')
        if support == 1:
            show_message_box('welcome','系统已检测到支持应用打开')
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
        functionset = ['Key.f1','Key.f2','Key.f3','Key.f4','Key.f5','Key.f6','Key.f7','Key.f8']
        keys = key
        keyname = str(keys)
        if keyname in functionset:
            # try:
            #     b = ('{0}字符键'.format(keys.char))
            #     pass
            # except AttributeError:  
            # print('{0} 功能键'.format(keys))
            #F1方法定义
            if keyname == functionset[0]:
                self.status = not self.status
            #F2方法定义
            elif keyname == functionset[1]:
                self.speed += 250
                print('\r                     |[Yuan_Qin]》》当前速度:,{}'.format(self.speed),end='')
            #F3方法定义
            elif keyname == functionset[2]:
                if self.speed >250:
                    self.speed -= 250
                    print('\r                     |[Yuan_Qin]》》当前速度:,{}'.format(self.speed),end='')
                elif self.speed < 250:
                    show_message_box('[Yuan_Qin]','当前速度已为最大')
            #F4方法定义
            elif keyname == functionset[3]:
                self.processDown = 'quit'
            elif keyname == functionset[4] or keyname == functionset[5] or keyname == functionset[6] or keyname == functionset[7]:
                self.Last_time_key = keyname
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
        self.thread = threading.Thread(target=listen, daemon=True)
        self.thread.start()
    #窗口监听器实例
    def listfo_start(self):
        def listen2():
            while True:
                Check = self.windows()
                # print(Check)
                if Check == 'YuanShen.exe' and self.jstatus == 1:
                    self.status = True
                    self.jstatus = 0
                elif Check != 'YuanShen.exe':
                    self.status = False
                    self.jstatus = 1
                time.sleep(0.5)
            # self.stop_event2.wait()
        self.thread2 = threading.Thread(target=listen2,daemon=True)
        self.thread2.start()
    #关闭所有线程
    def stop(self):
        self.stop_event.set()
        self.stop_event2.set()
    #开始演奏
    def musicstart(self,txt:list):
        musicup  = txt
        index = 0
        print('演奏已开始运行')
        while index < len(musicup):  
            play = musicup[index] 
            #演奏过程
            if re.match(r'[a-zA-Z]',play):
                press(play)
                time.sleep(0.000001)
                print('\r当前键符》》{}'.format(play),end='')
                # print('\r{}'.format('\n'),end='')
                # print('\n')
            elif play.isnumeric() == True:
                date = int(play)/self.speed
                time.sleep(date)
            #演奏退出
            if self.processDown == 'quit':
                break
            #演奏等待
            while self.status == False:
                time.sleep(0.5)
            index += 1
        print('[Yuan_Qin]》》演奏已结束')
        show_message_box('[Yuan_Qin]','演奏已结束')
        self.processDown = 'run'

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

C J 300 M W 300 E 300 S 300 G 300 T 300 E 300 
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
    with open('起风了.txt','w') as f:
        f.write(txt)
def music2():
    txt = """e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 
b s q 270 100 100 50 w 270 100 100 z b q
270 w 270 e 270 r 270 e 270 100 50
w 270 q 270 v a q 270 270 t 270 270 v s q 
270 270 t 270 270 z b q 270 270 h 270 g 270
g 270 100
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 
b s q 270 100 100 50 w 270 100 100 z b q 270 
w 270 e 270 r 270 e 270 100 50
w 270 q 270 v a q 270 270 t 270 270 v s q 
270 270 t 270 270 z b q 270 270 w 270 270
q 270 100 270 270
v a q 270 100 270 v a 270 b s t 270 100
100 r 270 e 270 z b 270 270 z b 270 q 270 
w 270 e 270 q 270 v a q t 270 100 270 v a 270 b 
s 270 270 q y 270 q t 270 z b q y 270 q t 270 z b
270 q 270 w 270 e 270 t 270 v a q t 270 100 
270 v a 270 b s 270 270 q r 270 q e 270 z b 270 270
z b 270 q 270 w 270 e 270 q 270 v a q e 270 270
v a 270 b s 270 r 270 e 270 q 270 z b 270
270 270 270 270
a d 270 100 100 q 270 100 100 a d 270 q 270 100
a d 270 a s 270
q 270 100 h 270 q a s 270 w 270 q 270 270
a f 270 100 100 q 270 100 100 a f 270 q 270 
100 a f 270 a d 270 q 270 100 h 270 q a d 270 
w 270 q 270 270
z 270 t 100 e 100 50 50 25 z e 100 25 e 100 50 50 50 
b w 100 50 50 e 100 50 w 100 50 b 100 50 50 q 100 50 
q 270
z 270 t 100 e 100 50 50 25 z e 100 25 e 100 50 50 50
b w 100 50 50 e 100 50 w 100 50 b 100 50 50 q 
100 50 q 270
v a 270 g 270 v a h 270 q 270 b s r 270
e 270 z b w 270 q 270 270 100
q 100 50 q 50 100 v a q 100 50 q 100 50 t 270 b 
s q 100 50 q 100 50 q 50 100 q 100 50 b s t 270 270
z b 100 100 q 100 50 q 50 100 z b q 100 50 q 100 50
t 270 z b q 100 50 q 100 50 q 50 100 q 100 50
z b t 270 270
v a 100 100 q 100 50 q 50 100 v a q 100 50 q 100
50 t 270 b s q 100 50 q 100 50 q 50 100 q 100
50 b s t 270 270
z b 270 g 270 z b h 270 q 270 z b r 270 e 270 z
b w 270 q 270
v a 100 100 q 100 50 q 50 100 v a q 100 50 q 100 
50 t 270 b s q 100 50 q 100 50 q 50 100 q 100 50
b s t 270 270
z b 100 100 q 100 50 q 50 100 z b q 100 50 q 100 50
t 270 z b q 100 50 q 100 50 q 50 100 q 100
50 z b t 270 270
v a 100 100 q 100 50 q 50 100 v a q 100 50 q 100 50
t 270 b s q 100 50 q 100 50 q 50 100 q 100 50
b s t 270 270
z q 270 270 270
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 b s
q 270 100 100 50 w 270 100 100 z b q 270 w 270
e 270 r 270 e 270 100 50
w 270 q 270 v a q 270 270 t 270 270 v s q 270 270
t 270 270 z b q 270 270 h 270 g 270 g 270 100
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270
b s q 270 100 100 50 w 270 100 100 z b q 270
w 270 e 270 r 270 e 270 100 50
w 270 q 270 v a q 270 270 t 270 270 v s q 270 270 
t 270 270 z b q 270 270 w 270 270 q 270 100 270
270 q 270 270 v t 270 270 270 270 b 270 270 270
270 z 270 270 270 270 r 100 100 e 270 270
w 100 100 q 270
v 270 270 t 270 270 b 270 270 270 270 z 270 270
270 q 100 100 j 100 100 q 270 270 v 270 270 t 270
270 b 270 270 270 270 z 270 270 270 270
r 100 100 e 270 270 w 100 100 q 270 v 270 270 t
270 270 b 270 270 270 270 z b q e 270 270 270 270
z b 270 270 z b 270 270 q 100 w 100 e 270 e 100
r 100 v a t 270 270 v a 270 270 b s r 270 100
b s r 270 270 z b e 270 270 270
z b 270 270 270 z b a d 270 270 270 s f 270 270
z b d g 270 270 270 270 z b 270 270 z b 270 270
q 100 w 100 e 270 e 100 r 100 v a t 270 270 100
v a 270 270 100 b s e 100 r 100 e 100 w 100 q
100 h 100 z b g 270 270 270 z b 270 270
z b s f 270 270 270 z b a d 270 270 270
z v 270 270 50 a 100 50 n 100 100 50 a 100 50 a
50 100 a 50 100 50 s 100 50 50 100 c b d 270 270
d 100 50 s 100 100 50 d 100 50 d 50 100 d 100 50
50 j 100 50 50 100 q v n 270 270
a 100 50 n 100 100 50 a 100 50 25 a 25 50 100 a 
50 100 50 s 100 50 50 100 d v n 270 f 270 d 270
f 270 g b m 270 a 270 a 270 270
z v 270 270 50 a 100 50 n 100 100 50 a 100 50 a 
100 50 a 50 100 50 s 100 50 50 100 c b d 270 270
d 100 50 s 100 100 50 d 100 50 d 100 50 d 100 50
50 j 100 50 50 100 q v n 270 270
q 100 50 h 100 25 b m q 100 50 50 h 100 25 q 100
100 25 h 100 50 z b q 270 270
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 b
s q 270 100 100 50 w 270 100 100 z b q 270 w 
270 e 270 r 270 e 270 100 50
w 270 q 270 v a q 270 270 t 270 270 v s q 270
270 t 270 270 z b q 270 270 h 270 g 270 g 270 100
e 270 w 270 q 270 q v a 270 g 270 q 270 g 270 b
s q 270 100 100 50 w 270 100 100 z b q 270 w
270 e 270 r 270 e 270 100 50
w 270 q 270 v a q 270 270 t 270 270 v s
q 270 270 t 270 270
z b q 270 270 w 270 270 q 270 100 270 270
g 270 50 z 50 b 50 q 270 270 270 270 w 270 270 e
270 270 n 50 z 270 270 t 270 50 e 50 270 w 50 270
e 50 b 50 z 270 270 270 270 w 50 270 q 270 50 b
50 s 50 w 270 270 h 270 270 270 270 v 50 a 50 q
270 270 270 270 q 270 270 w 270 50 b 50 s 50 j
270 270 h 270 270 270 g 270 270 270 270
e 270 w 270 q 270 270 q v 270 50 g 270 50 q
270 50 g 270 50 b q 270 100 100 50 50 w 270 50 
100 100 z q 270 50 w 270 e 270 r 270 e 270 100 50
w 270 50 q 270 50 v a q 270 270 50 t 270 270 50 b
q 270 270 50 t 270 270 50 z q 270 270 50 h 270
50 g 270 50 g 50 270 100
e 270 w 270 q 270 50 q v a 270 50 g 270 50 q 270
50 g 270 50 b s q 270 100 100 50 50 w 270 50 100
100 z b q 270 50 w 270 e 270 r 270 e 270 100 50
w 270 50 w 270 50 q 270 100 v a q 270 50 100 q 
270 50 b s t 270 50 r 270 50 e 270 50 q 270 50 z 
b q 270 270 270 w 270 270 270 z 270 b 270 q
"""
    with open('让风告诉你.txt','w') as f:
        f.write(txt)
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
    [Yuan_Qin]》》初始化默认速度为乐谱速度/2000
    [Yuan_Qin]》》为使美观可以写完一句一行,不要求强制换行,写完单句后回车自动保存,无内容时回车自动退出
    [Yuan_Qin]》》(当前为{version}版本创建功能暂不支持功能键,敬请期待!)
    [Yuan_Qin]》》创建功能按键=>>选择删除一整行F5或输入/d、删除上一段编写F6或输入/a、完全测试F7、选行测试F8
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
            with open(SaveFilepPhat+'.txt',mode) as fs:
                if len(txt) != 0:
                    fs.write(txt)
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
#启动所有线程
def all_sh():
    music.listen_start()
    music.listfo_start()
#加载乐谱
def home():
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
            music.timeon(0,5,'[Yuan_Qin]》》退出倒计时')
            quit()
        elif musicfilename == '':
            print('GO')
            # music.listen_start()
            MusicCreate().create()
        else:
            #加载局内功能按键
            all_sh()
            while True:
                try:
                    dates = input('[Yuan_Qin]》》当前默认速度为【乐谱速度/2000】,若要调整请输入[250~10000],不调整请下一步:')
                    if dates == '':
                        break
                    elif int(dates) >250 and int(dates) <10000:
                        music.speed = int(dates)
                        break
                    show_message_box('[Yuan_Qin]','请输入[250~10000]范围内的整数')
                except ValueError as t3:
                    show_message_box('[Yuan_Qin]','输入整数返回错误:'+str(t3))
            txts = music.txtimport(musicfilename)
            if txts == -1:
                pass
            else:
                #加载演奏
                music.musicstart(txts)
music = musickey()
music1()
music2()
print('[Yuan_Qin]》》自带歌曲:起风了.txt、让风告诉你.txt,已存在当前程序目录下')
music.ifwindowsON()
home()
#停止监听线程
music.stop()
#E:\\qz1.txt
#