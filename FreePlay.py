import pygame
import sys
import time
import threading
from pynput.keyboard import Key, Listener as keyList
import os
script_path = os.path.abspath(sys.argv[0])
# 获取脚本文件所在的目录
script_dir = os.path.dirname(script_path)
os.chdir(script_dir)
# 初始化 Pygame
pygame.init()

# 初始化 mixer 模块，设置音频通道数和缓冲区大小（可选）
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

'''调度方差'''
class FunctionCallTracker:
    """## 调度方差测量器
    `interval`:最大调用方差间隔
    - 拿取成员方法`my_function`进行测量
    """
    def __init__(self, interval=0.3):
        self.last_call_time = None
        self.interval = interval
    """计时器"""
    def is_consecutive_call(self):
        current_time = time.time()
        if self.last_call_time is None:
            # 如果是第一次调用，记录当前时间并返回False
            self.last_call_time = current_time
            return False,0
        elif current_time - self.last_call_time <= self.interval:
            variance = current_time - self.last_call_time
            self.last_call_time = current_time
            # 如果当前时间与上次调用时间的差值在指定间隔内，返回True
            return True,variance
        else:
            # 如果超过指定间隔，更新上次调用时间并返回False
            variance = current_time - self.last_call_time
            self.last_call_time = current_time
            return False,variance
    """方差输出"""
    def my_function(self):
        l = self.is_consecutive_call()
        if l[0]:
            # print("Function was called consecutively within 0.3 seconds.")
            return True,l[1]
        else:
            # print("Function was not called consecutively or within the specified interval.")
            return False,l[1]


# 等待一段时间，让声音播放
class Listener_listen_key:
    def __init__(self,keydataup = None,KeyMusicfun = None) -> None:
        self.stop_event = threading.Event()
        self.thread = None
        self.keydataup = keydataup
        self.KeyMusic = KeyMusicfun
        self.langkey = []
        # self.txt = ""
        self.times = FunctionCallTracker(interval=0.07)
        self.threadname = 0
    def fun(self,key=None):
        # self.threadname += 1
        # def stop_listening(key):
        try:
            # print('{0}字符键'.format(key.char))
            newket = key.char
            newket = newket.upper()
            if newket in ['Q','W','E','R','T','Y','U','A','S','D','F','G','H','J','Z','X','C','V','B','N','M']:
                self.start_time = time.time()
                sound = pygame.mixer.Sound(f"Audio/{newket}.wav")
                sound.play(loops=0)
                timelist = self.times.my_function()
                if timelist[0]:
                    self.keydataup(newket)
                    self.langkey.append(newket)
                else:
                    # print(self.txt)
                    # self.KeyMusic(newket)
                    if timelist[1] < 0.6:
                        # print("启用3")
                        if timelist[1] != 0:
                            self.langkey.append(str(int(round(timelist[1],3)*1000)))
                        self.langkey.append(newket)
                        if len(self.langkey) > 30:
                            self.langkey.append(str(int(round(timelist[1],3)*1000)))
                            print(round(timelist[1],3))
                            self.KeyMusic(self.langkey)
                            self.langkey = []
                            self.langkey.append(newket)
                    else:
                        # print("启用4")
                        self.langkey.append(str(int(round(timelist[1],3)*1000)))
                        print(round(timelist[1],3))
                        self.KeyMusic(self.langkey)
                        self.langkey = []
                        self.langkey.append(newket)
                    self.keydataup(' '+newket)
                    # self.txt = ""
                    # self.txt += newket
        except:
            pass
        # name = f"Thread{self.threadname}"
        # threading.Thread(target=stop_listening(key), args=(name,)).start()
    def save_key(self):
        if len(self.langkey) > 0:
            self.KeyMusic(self.langkey)
            self.langkey = []
    def listen_start(self)->None:
        if self.thread is None or not self.thread.is_alive():
            def listen():
                with keyList(on_press=self.fun) as listener:#自动向函数传入key类型参数,需要使用char属性转为字符类型
                    self.stop_event.wait()
                    pass
            self.thread = threading.Thread(target=listen, daemon=True)
            self.thread.start()
    def listen_stop(self)->None:
        self.stop_event.set()
class Listener_listen_key_test:
    def __init__(self,fun,fun2) -> None:
        self.stop = True
        self.fun = fun
        self.funkey = fun2
    # def fun2(self,key=None):
    #     self.fun(key)
    # def fun3(self,key=None):
    #     self.funkey(key)
    def listen_on_start(self):
        self.new = Listener_listen_key(keydataup=self.fun,KeyMusicfun=self.funkey)
        self.new.listen_start()
    def listen_on_stop(self):
        self.new.listen_stop()
if __name__ == '__main__':
    Listener_listen_key_test().listen_on_start()