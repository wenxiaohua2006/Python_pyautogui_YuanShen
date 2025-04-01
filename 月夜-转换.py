import re
import tkinter as tk
from tkinter import messagebox
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
class convert:
    def __init__(self):
        self.i = '100'
        self.i2 = '200'
        self.i3 = '300'
        self.i4 = '400'
    def txtimporton(self,file,savename,box:bool=True):
        # try:
            try:
                with open(file,'r+',encoding='utf-8') as f:
                    txt = f.read()
            except Exception as y:
                show_error('错误',f'{y},发生文件{file}')
                return -1
            txt_split = list(filter(lambda x: x != '', txt.split('\n')))
            ZON = ""
            for txtn in txt_split:
                if txt != '':
                    n = re.search(r'[\u4e00-\u9fff]',txtn)
                    if n:
                        txt_split.remove(txtn)
                        continue
                    new_word = []
                    a = False
                    c = False
                    b = False
                    p = ""
                    l = ""
                    ding = False#
                    for strtxt in txtn:
                        if strtxt == '(' or a == True:
                            a = True
                            if re.match(r'[a-zA-Z]',strtxt):
                                p = p + strtxt + ' '
                            elif strtxt == ')':
                                # print(p)
                                p = p[:-1]
                                new_word.append(p)
                                a = False
                                p = ""
                        elif strtxt == '[' or c == True:
                            c = True
                            ding = True#
                            if re.match(r'[a-zA-Z]',strtxt):
                                p = p + strtxt + ' '
                            elif strtxt == ']':
                                l = l[:-5]
                                new_word.append(l)
                                c = False
                                l = ""
                                ding = False
                        elif strtxt == '-' and b == False:
                            new_word.append(' 100 ')
                            b = True
                        elif b == True:
                            b = False
                        elif strtxt == ' ':
                            if ding:#
                                new_word.append(' 400 ')#
                            else:
                                new_word.append(' 200 ')
                            #新修改
                        # elif strtxt in [')[','](']:
                        #     new_word.append(' 200 ')
                            #结束
                        elif strtxt == '/':
                            pass
                        else:
                            new_word.append(strtxt)
                    # try:
                    d = [new_word[0]]
                        # print(d)
                    # except:
                    #     pass
                    key = len(new_word)
                    for a in range(1,key):
                        a1 = new_word[a-1]
                        a2 = new_word[a]
                        if re.match(r'[a-zA-Z]',a1) and re.match(r'[a-zA-Z]',a2):
                            d.append(' 300 ' + a2)
                        else:
                            d.append(a2)#不保护
                    try:
                        if re.search(r'[a-zA-Z]',d[len(d)-1]):
                            d.append(' 300 ')
                        for txts in d:
                            ZON = ZON + txts
                    except UnboundLocalError:
                        pass
                    ZON = ZON + '\n'
            if box == True:
                print(ZON)
            with open(savename+'.yq','w+') as h:
                h.write(ZON)
            if box == True:
                show_message_box('提示','成功转换')
        # except Exception as pp:
        #     show_error('错误',f'转换失败{pp},错误文件{file}')
if __name__ == '__main__':
    print('--------------------------转换需知')
    print('温馨提示:转换提示,特供作者《《月夜OuO》》编曲乐谱转换,其余作者无法转换')
    txtfilename = input('请输入同目录下的文件名或完整的路径,包括后缀名:')
    savetxtname = input('请输入转换文件名保存名称,包括后缀名:')
    n = convert().txtimporton(txtfilename,savetxtname)
    if n == -1:
        show_error('错误','转换失败')