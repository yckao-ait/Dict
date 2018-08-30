# Python 3
# -*- coding: UTF-8 -*-
#
# 08/29/18 added auto translattion, always on top.
# 08/27/18 added tkinter, cht-chs translation font chaged, changed md5 locatoin to enable continuous translation.
# 08/27/18 created based on yodao API engine, dummy UI.
#=======================================================
import pyperclip
import hashlib
import random
import requests
import time
import json
from tkinter import *
from PIL import Image, ImageTk
from langconv import Converter
import threading

root = Tk() # create master windows
T = Text(root, height=25, width=200,font=("新細明體",12,"normal"))
T.pack()
T.insert(END,"將翻譯文字拷貝至剪貼簿再執行智能翻譯\n")
T.insert(END,"Copy text to clipboard and start translation\n")
# Moved btn text to global
autoSwitchBtn_text = StringVar()
bilinSwitchBtn_text = StringVar()

s = requests.Session()
m = hashlib.md5()

class Dict:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer': 'http://fanyi.youdao.com/',
            'contentType': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
        self.base_config()

    def base_config(self):
        """
        setup basic config & cookie
        """
        s.get('http://fanyi.youdao.com/')

    def translate(self,srcString):
        i = srcString
        salf = str(int(time.time() * 1000) + random.randint(0, 9))
        n = 'fanyideskweb' + i + salf + "rY0D^0'nM0}g5Mm1z%1G4"
        m.update(n.encode('utf-8'))
        sign = m.hexdigest()
        data = {
            'i': i,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salf,
            'sign': sign,
            'doctype': 'json',
            'version': "2.1",
            'keyfrom': "fanyi.web",
            'action': "FY_BY_DEFAULT",
            'typoResult': 'false'
        }
        resp = s.post(self.url, headers=self.headers, data=data)
        return resp.json()

    def translateFinal(self,srcString):
        global m
        m = hashlib.md5()
        i = srcString
        salf = str(int(time.time() * 1000) + random.randint(0, 9))
        n = 'fanyideskweb' + i + salf + "rY0D^0'nM0}g5Mm1z%1G4"
        m.update(n.encode('utf-8'))
        sign = m.hexdigest()
        data = {
            'i': i,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salf,
            'sign': sign,
            'doctype': 'json',
            'version': "2.1",
            'keyfrom': "fanyi.web",
            'action': "FY_BY_DEFAULT",
            'typoResult': 'false'
        }

        resprow = s.post(self.url, headers=self.headers, data=data)
        resp = resprow.json()
        #print(resp)
        #=== dataResult is list of dict
        dataResult = resp['translateResult']
        print(dataResult)
        count = len(dataResult)
        i = 0
        strSource=""
        strTranslated = ""
        while i < count:
            #print(dataResult[i])
            #print("\n")
            #== dictResult is list of dict
            dictResult = dataResult[i]
            j = 0
            while j < len(dictResult):
                #print(dictResult[j]['tgt'])
                strTranslated += dictResult[j]['tgt']
                strSource += dictResult[j]['src']
                j += 1
            i += 1
            strTranslated += "\n"
            strSource += "\n"
        return strTranslated

##++ tkinter ==================================================
class Window(Frame): 
    # init windows
    def __init__(self, master=None):      
        # Frame init with maser windows. 
        Frame.__init__(self, master)   
        # reference to tk windows master                 
        self.master = master
      #執行init_window()
        self.init_window()
        self._isAuto = False
        self._isBilingual = False
        self._lastTranslated = ""

    #init_window（） and init windows control
    def init_window(self):
        # Change window title
        self.master.title("My Smart Translator w/ 有道翻譯 - Gauss Mindworks Inc")
        # pack widget into container
        self.pack(fill=BOTH, expand=1)
        # create button
        translateButton = Button(self, text="Translate(智能翻譯)",command=self.client_translate)
        
        global autoSwitchBtn_text
        global bilinSwitchBtn_text

        autoSwitchButton = Button(self, textvariable=autoSwitchBtn_text,command=self.client_auto_switch)
        autoSwitchBtn_text.set("Auto Translation On")

        bilinSwitchButton = Button(self,textvariable=bilinSwitchBtn_text,command=self.client_auto_bilingual)
        bilinSwitchBtn_text.set("Binlingual On")

        quitButton = Button(self, text="Quit",command=self.client_exit)
        # place button in window
        translateButton.place(x=00,y=0)
        autoSwitchButton.place(x=150, y=0)
        bilinSwitchButton.place(x=300, y=0)
        quitButton.place(x=450, y=0)

    def client_translate(self):
        global dic
        global root

        
        #T.delete(0,END)
        print("Start Translate\n")
        #pyperclip.copy("""今天天氣如何""")
        msg = pyperclip.paste()
        if msg == "" :
            msg = """今天天氣如何"""

        
        if self._lastTranslated==msg:
            if self._isAuto == True:
                # keep doing auto translation
                self._timer = threading.Timer(8.0,self.client_translate)
                self._timer.start()
            return
        
        T.delete(1.0,END)
        translatedMsg = dic.translateFinal(msg)
        #line = Converter('zh-hans').convert(line.decode('utf-8'))
        #line = line.encode('utf-8')
        
        chtMsg=Converter('zh-hant').convert(translatedMsg)
        #print(translatedMsg)
        print(chtMsg)

        self._lastTranslated = msg
        #T.insert(END,translatedMsg)
        if self._isBilingual==True:
            T.insert(END,msg+"\n")

        T.insert(END,chtMsg)

        if self._isAuto == True:
            # keep doing auto translation
            self._timer = threading.Timer(8.0,self.client_translate)
            self._timer.start()  

    def client_auto_switch(self):
        global autoSwitchBtn_text
        global bilinSwitchBtn_text
        if self._isAuto == False:
            self._timer = threading.Timer(8.0,self.client_translate)
            self._timer.start()
            self._isAuto = True
            autoSwitchBtn_text.set("Auto Translation OFF")
            print("start auto translation\n")
        else:
            self._isAuto = False
            self._timer.cancel()
            autoSwitchBtn_text.set("Auto Translation On")
                        
        #global root
        #root.lift()
    
    def client_auto_bilingual(self):
        global autoSwitchBtn_text
        global bilinSwitchBtn_text
        if self._isBilingual == False:
            self._isBilingual = True
            bilinSwitchBtn_text.set("Binlingual OFF")
            print("bilingual ON")
        else:    
            self._isBilingual = False
            bilinSwitchBtn_text.set("Binlingual On")
            print("binlingual OFF")

    def client_exit(self):
        exit()

dic = Dict()
msg = pyperclip.paste()
root.geometry("600x480")    #Set windows size
app = Window(root)          #create window
root.configure(background='gold')
#root.lift()
root.attributes('-topmost', 'true')
root.mainloop()             #mainloop