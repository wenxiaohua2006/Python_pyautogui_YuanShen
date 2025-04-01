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

# map1 = {"A":'C4', "S":'D4', "D":'E4', "F":'F4', "G":'G4', "H":'A4', "J":'B4', "K":'C5'}
# for key,value in map1.items():
#     sound = pygame.mixer.Sound(f"C:/Users/Administrator/Desktop/原神-演奏/全音阶文件/{key}.wav")
#     sound.play(loops=0)
#     time.sleep(0.5)
# # 停止所有正在播放的声音
# pygame.mixer.stop()

# # 退出 Pygame
# pygame.quit()

def fun(key=None):
    try:
        # print('{0}字符键'.format(key.char))
        newket = key.char
        sound = pygame.mixer.Sound(f"Audio/{newket.upper()}.wav")
        sound.play(loops=0)
        # time.sleep(0.5)
    except:
        pass
# 等待一段时间，让声音播放
class Listener_listen_key:
    def __init__(self) -> None:
        self.stop_event = threading.Event()
        self.thread = None
    def listen_start(self,func)->None:
        if self.thread is None or not self.thread.is_alive():
            def listen():
                with keyList(on_press=func) as listener:#自动向函数传入key类型参数,需要使用char属性转为字符类型
                    self.stop_event.wait()
                    pass
            self.thread = threading.Thread(target=listen, daemon=True)
            self.thread.start()
    def listen_stop(self)->None:
        self.stop_event.set()
class Listener_listen_key_test:
    def __init__(self) -> None:
        pass
    def listen_on_start(self):
        self.new = Listener_listen_key()
        self.new.listen_start(fun)
    def listen_on_stop(self):
        self.new.listen_stop()

Listener_listen_key_test().listen_on_start()
while True:
    time.sleep(10)