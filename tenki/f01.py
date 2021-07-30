# ==================================================
# library
# ==================================================
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog

import sqlite3
from numpy import complex128
import pandas as pd

import datetime
import os
import csv
import sys

import matplotlib.pyplot as plt
import japanize_matplotlib

import requests
import bs4

"""
趣旨：自分の住んでいる場所の今後の天気情報/予報を「直感的」に把握したい。
経緯：「気温、湿度、風速、雨量」を把握し、出かける際の服装・持ち物を決めたい。

情報源：tenki.jp
上記より情報を取得し、データベースに格納
データベースから引き出した情報をウィジェット内ツリービューに表示
matplotチャートで出力・表示

そのほか：csv読み込み、書き出し

"""

# =============================================================================================
# class / bs4
# =============================================================================================
class BS4:
    def __init__(self,URL):
        self.r = requests.get(URL)
        self.s = bs4.BeautifulSoup(self.r.text, 'html.parser')

    def scraping(self,a,b,c): 
        """
        bs4で抽出したテキストからさらに絞り込み
        引数：htmlのクラス、要素など
        戻値：リスト
        a = 'tr'
        b = 'head'
        c = 'p'
        """
        list1= []
        for j in self.s.find_all(a , class_ = b):
            for i in j.find_all(c):
                list1.append(i.text)

        return list1
  

# =============================================================================================
# bs4
# =============================================================================================
def ProcessScraping(URL,a,b,c):
    """
    ///Webスクレイピングのプロセス
    """
    bs4 = BS4(URL)
    r = bs4.scraping(a,b,c)
    return r


# ====================================================================================================
# ウィジェット
# ====================================================================================================
class Application(tk.Frame):
    def __init__(self, master=None):
        """
        ///ウィジェット親クラス///
        """
        super().__init__(master)
        self.master = master

        # 全体ウィンドウサイズ、配置位置
        self.master.geometry("1300x900+0+0")

        # ウィンドウのタイトル
        self.master.title("tenki.jpの天気予報")

        # 上記を反映する
        self.pack()

        # ウィンドウ内のウィジェットを配置
        self.create_widgets()

    def create_widgets(self):
        """
        ///ウィジェットの配置///
        ///この中でウィジェット部品を配置する///
        """
        # ウィジェットのスタイル設定
        self.style = ttk.Style()

        fontsize_t1 = 13
        fontsize_t2 = 10

        # Treeview headingのフォント
        self.style.configure("Treeview.Heading",font=("",fontsize_t1))

        # Treeview内のフォント
        self.style.configure("Treeview",font=("",fontsize_t2))

        # -------------------------
        # DB / テーブル有無チェック
        # -------------------------
        # DB / DB名
        dbname = "tenki.db"
        # DB / table名
        tableName="WeatherTable"

        # テーブル有無確認、無ければ作成
        TableExsistenceCheckAndCreate(dbname,tableName)

        # -------------------------
        # master / frame
        # -------------------------
        #tcl_isOk = self.register(IsOk)
        self.frame0 = tk.Frame(self, width=800, height=100)  
        self.frame1 = tk.Frame(self, width=800, height=100)   
        self.frame2 = tk.Frame(self, width=800, height=300)
        self.frame3 = tk.Frame(self, width=800, height=100)
        self.frame4 = tk.Frame(self, width=800, height=100)
        self.frame5 = tk.Frame(self, width=800, height=100)
        self.frame6 = tk.Frame(self, width=800, height=100)
        self.frame0.grid(column=0,row=0,padx=5,pady=5)
        self.frame1.grid(column=0,row=1,padx=5,pady=5)
        self.frame2.grid(column=0,row=2,padx=5,pady=5)
        self.frame3.grid(column=0,row=3,padx=5,pady=5)
        self.frame4.grid(column=0,row=4,padx=5,pady=5)
        self.frame5.grid(column=0,row=5,padx=5,pady=5)
        self.frame6.grid(column=0,row=6,padx=5,pady=5)

        # --------------------------------------------------
        # 【変数】ウィジェット間距離など
        # --------------------------------------------------
        pad_x1 = 10
        pad_y1 = 3
        width1 = 10
        width2 = 10
        Lbl_name1 = "ID"
        Lbl_name2 = "hour"
        Lbl_name3 = "weather"
        Lbl_name4 = "temperature"
        Lbl_name5 = "humidity"
        Lbl_name6 = "windblow"
        Lbl_name7 = "wind-speed"
        Lbl_name8 = "precipitation"
        fontsize1 = 15
        fontsize2 = 12
        width_treeview1 = 100

        # Entry欄のheight
        ipady_1 = 15

        # 情報取得したいURL
        URL_yokohama ='https://tenki.jp/forecast/3/17/4610/14100/1hour.html'
        URL_saku ='https://tenki.jp/forecast/3/23/4820/20217/1hour.html' 
        URL_nagoya ='https://tenki.jp/forecast/5/26/5110/23100/1hour.html' 
        URL_fukuoka='https://tenki.jp/forecast/9/43/8210/40130/1hour.html' 
        URL_kagoshima ='https://tenki.jp/forecast/9/49/8810/46201/1hour.html' 
        URL_sapporo ='https://tenki.jp/forecast/1/2/1400/1100/1hour.html' 
        URL_fukushima = 'https://tenki.jp/forecast/2/10/3610/7201/1hour.html'
        URL_aomori = 'https://tenki.jp/forecast/2/5/3110/2201/1hour.html'
        URL_osaka = 'https://tenki.jp/forecast/6/30/6200/27100/1hour.html'
        URL_onomichi ='https://tenki.jp/forecast/7/37/6710/34205/1hour.html'
        URL_kouchi = 'https://tenki.jp/forecast/8/42/7410/39201/1hour.html'

        # --------------------------------------------------
        # frame0 / button
        # --------------------------------------------------
        t1 = '横浜市'

        t2 = '佐久市'
        t3 = '名古屋市'
        t4 = '福岡市'
        t5 = '鹿児島市'
        t6 = '札幌市'
        t7 = '福島市'
        t8 = '青森市'
        t9 = '大阪市'
        t10 = '尾道市'
        t11 = '高知市'










        self.btn_20= tk.Button(self.frame0, text = t1, command=lambda:self.Push2(URL_yokohama,dbname,tableName,t1),font=("",fontsize1))
        self.btn_20.grid(column=0,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_21= tk.Button(self.frame0, text = t2, command=lambda:self.Push2(URL_saku,dbname,tableName,t2),font=("",fontsize1))
        self.btn_21.grid(column=1,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_22= tk.Button(self.frame0, text = t3, command=lambda:self.Push2(URL_nagoya,dbname,tableName,t3),font=("",fontsize1))
        self.btn_22.grid(column=2,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_23= tk.Button(self.frame0, text = t4, command=lambda:self.Push2(URL_fukuoka,dbname,tableName,t4),font=("",fontsize1))
        self.btn_23.grid(column=3,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_24= tk.Button(self.frame0, text = t5, command=lambda:self.Push2(URL_kagoshima,dbname,tableName,t5),font=("",fontsize1))
        self.btn_24.grid(column=4,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_25= tk.Button(self.frame0, text = t6, command=lambda:self.Push2(URL_sapporo,dbname,tableName,t6),font=("",fontsize1))
        self.btn_25.grid(column=5,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_26= tk.Button(self.frame0, text = t7, command=lambda:self.Push2(URL_fukushima,dbname,tableName,t7),font=("",fontsize1))
        self.btn_26.grid(column=6,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_27= tk.Button(self.frame0, text = t8, command=lambda:self.Push2(URL_aomori,dbname,tableName,t8),font=("",fontsize1))
        self.btn_27.grid(column=7,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_28= tk.Button(self.frame0, text = t9, command=lambda:self.Push2(URL_osaka,dbname,tableName,t9),font=("",fontsize1))
        self.btn_28.grid(column=8,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_29= tk.Button(self.frame0, text = t10, command=lambda:self.Push2(URL_onomichi,dbname,tableName,t10),font=("",fontsize1))
        self.btn_29.grid(column=9,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_30= tk.Button(self.frame0, text = t11, command=lambda:self.Push2(URL_kouchi,dbname,tableName,t11),font=("",fontsize1))
        self.btn_30.grid(column=10,row=0,padx=pad_x1,pady=pad_y1)

        # --------------------------------------------------
        # frame1 / button
        # --------------------------------------------------
        self.btn_4= tk.Button(self.frame1, text = 'ＤＢ読込み', command=lambda:self.Push4(dbname,tableName),font=("",fontsize1))
        self.btn_4.grid(column=2,row=1,padx=pad_x1,pady=pad_y1)

        self.btn_6= tk.Button(self.frame1, text = 'テーブル削除/作成', command=lambda:self.Push6(dbname,tableName),font=("",fontsize1))
        self.btn_6.grid(column=3,row=1,padx=pad_x1,pady=pad_y1)

        self.btn_9= tk.Button(self.frame1, text = 'CSV読み込み', command=self.Push10,font=("",fontsize1))
        self.btn_9.grid(column=5,row=1,padx=pad_x1,pady=pad_y1)

        self.btn_10= tk.Button(self.frame1, text = 'CSV出力', command=lambda:self.Push11(dbname,tableName),font=("",fontsize1))
        self.btn_10.grid(column=6,row=1,padx=pad_x1,pady=pad_y1)

        self.btn_11= tk.Button(self.frame1, text = '表jpg出力', command=lambda:self.Push12(dbname,tableName),font=("",fontsize1))
        self.btn_11.grid(column=7,row=1,padx=pad_x1,pady=pad_y1)

        self.btn_12= tk.Button(self.frame1, text = 'チャート出力', command=lambda:self.Push13(dbname,tableName),font=("",fontsize1))
        self.btn_12.grid(column=7,row=1,padx=pad_x1,pady=pad_y1)

        # --------------------------------------------------
        # frame2 / Label,Entry
        # -------------------------------------------------- 
        # 選択したデータの表示場所＆入力箇所
        self.Label_1 = tk.Label(self.frame2, text = Lbl_name1, width = width1, bg='gray',fg='white',font=("",fontsize1))
        self.Label_1.grid(column=0,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_1 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_1.grid(column=0,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)      

        self.Label_2 = tk.Label(self.frame2, text = Lbl_name2, width = width1, bg='gray',fg='white',font=("",fontsize1))
        self.Label_2.grid(column=1,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_2 = tk.Entry(self.frame2,width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_2.grid(column=1,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        self.Label_3 = tk.Label(self.frame2, text = Lbl_name3, width = width1, bg='gray',fg='white',font=("",fontsize1))
        self.Label_3.grid(column=2,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_3 = tk.Entry(self.frame2,width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_3.grid(column=2,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        self.Label_4 = tk.Label(self.frame2, text = Lbl_name4, width = width1, bg='gray', fg='white',font=("",fontsize1))
        self.Label_4.grid(column=3,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_4 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_4.grid(column=3,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        self.Label_5 = tk.Label(self.frame2, text = Lbl_name5, width = width1, bg='gray', fg='white',font=("",fontsize1))
        self.Label_5.grid(column=4,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_5 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_5.grid(column=4,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        self.Label_6 = tk.Label(self.frame2, text = Lbl_name6, width = width1, bg='gray', fg='white',font=("",fontsize1))
        self.Label_6.grid(column=5,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_6 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_6.grid(column=5,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        self.Label_7 = tk.Label(self.frame2, text = Lbl_name7, width = width1, bg='gray', fg='white',font=("",fontsize1))
        self.Label_7.grid(column=6,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_7 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_7.grid(column=6,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)
    
        self.Label_8 = tk.Label(self.frame2, text = Lbl_name8, width = width1, bg='gray', fg='white',font=("",fontsize1))
        self.Label_8.grid(column=7,row=1,padx=pad_x1,pady=pad_y1)
        self.entry_8 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_8.grid(column=7,row=2,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        
        # --------------------------------------------------
        # frame3 / button
        # --------------------------------------------------
        # 書き込みボタン
        self.btn_1= tk.Button(self.frame3, text = '書き込み', command=lambda:self.Push1(dbname,tableName),width=30,font=("",fontsize1))
        self.btn_1.grid(column=1,row=0,padx=pad_x1,pady=pad_y1)

        # 削除ボタン
        self.btn_3= tk.Button(self.frame3, text = '削除処理', command=lambda:self.Push3(dbname,tableName),width=30,font=("",fontsize1))
        self.btn_3.grid(column=2,row=0,padx=pad_x1,pady=pad_y1)

        # --------------------------------------------------
        # frame4 / entry
        # --------------------------------------------------
        self.entry_9 = tk.Entry(self.frame4, width=80, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_9.grid(column=0,row=0,padx=pad_x1,pady=pad_y1,ipady=ipady_1)
        # -------------------------
        # frame5 / treeview
        # -------------------------
        self.tree = ttk.Treeview(self.frame5, height = 20, style='Treeview')

        # treeの設定
        self.tree["columns"] = (1,2,3,4,5,6,7,8)
        self.tree["show"] = "headings"
        self.tree.column(1, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(2, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(3, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(4, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(5, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(6, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(7, width=width_treeview1,anchor=tk.CENTER)
        self.tree.column(8, width=width_treeview1,anchor=tk.CENTER)
        self.tree.heading(1, text=Lbl_name1)
        self.tree.heading(2, text=Lbl_name2)
        self.tree.heading(3, text=Lbl_name3)
        self.tree.heading(4, text=Lbl_name4)
        self.tree.heading(5, text=Lbl_name5)
        self.tree.heading(6, text=Lbl_name6)
        self.tree.heading(7, text=Lbl_name7)
        self.tree.heading(8, text=Lbl_name8)
        
        # --------------------------------------------------
        # frame6 / Quit button
        # --------------------------------------------------
        self.btn_2= tk.Button(self.frame6, text="閉じる", fg="black",command=self.master.destroy,font=("",fontsize1))
        self.btn_2.grid(column=0,row=0,padx=pad_x1,pady=pad_y1)

        # --------------------------------------------------
        # Entry入力不可状態の処理
        # --------------------------------------------------
        AllEntryDisable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)

        # --------------------------------------------------
        #ツリー内をマウスで選択した時
        # --------------------------------------------------
        self.tree.bind("<<TreeviewSelect>>", self.OnTreeSelect)

        # pack
        self.tree.pack()

        # DB/Tableの有無のチェック、無ければ作成する
        TableExsistenceCheckAndCreate(dbname,tableName)


    def OnTreeSelect(self,event):     
        """
        ///ツリービュー内の情報を選択したときの処理///
        """
        # Entryの入力可能処理
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)

        for id in self.tree.selection():
            #Dicionary形式で抽出
            self.tree.set(id)

        mydic = self.tree.set(id)
        d1 = mydic['1']
        d2 = mydic['2']
        d3 = mydic['3']
        d4 = mydic['4']
        d5 = mydic['5']
        d6 = mydic['6']
        d7 = mydic['7']
        d8 = mydic['8']


        # 中身をいったん消してから/データ挿入
        AllEntryInfoErase(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)

        # データを入れる
        self.entry_1.insert(tk.END,d1)
        self.entry_2.insert(tk.END,d2)
        self.entry_3.insert(tk.END,d3)
        self.entry_4.insert(tk.END,d4)
        self.entry_5.insert(tk.END,d5)
        self.entry_6.insert(tk.END,d6) 
        self.entry_7.insert(tk.END,d7)
        self.entry_8.insert(tk.END,d8)

        # Entry制限


    def Push1(self,dbname,tableName):
        """
        ///書き込みボタン押下時の処理///
        ///Entry内の情報を読み取り、DBへ登録する///
        """
        # ------------------------------
        # 実行前の確認処理
        # ------------------------------
        res = PopUp4()

        # yesで抜けて進む
        if res =="yes":
            pass

        # noで終了処理
        else:
            return      

        # ------------------------------
        # 処理の開始
        #-------------------------------
        # Entry欄の情報取得
        e1 = self.entry_1.get()
        e2 = self.entry_2.get()
        e3 = self.entry_3.get()
        e4 = self.entry_4.get()
        e5 = self.entry_5.get()
        e6 = self.entry_6.get()
        e7 = self.entry_7.get()
        e8 = self.entry_8.get()

        # DB接続し、
        dbc = DBconnection(dbname)

        # UPDATE/INSERTの振り分け（ID有無で振り分け）
        if e1 != "":

            # データ/UPDATE
            dbc.Updatedata(tableName,e1,e2,e3,e4,e5,e6,e7,e8)

        else:
            # データ/INSERT
            dbc.InsertData(tableName,e2,e3,e4,e5,e6,e7,e8)

        # DB COMMIT/CLOSE
        dbc.Commit()
        dbc.Close()

        # DBを再読み込み
        data = ProcessGetData(dbname,tableName)

        # データ挿入
        TreeDataImport(self.tree,data)

        # ポップアップ通知
        if e1 != "":
            PopUp1(e1)
        else:    
            PopUp2()

    def Push2(self,URL,dbname,tableName,prefecture):
        """
        ///Webスクレイピング処理///
        """
        # 情報取得したいURL
        #URL ='https://tenki.jp/forecast/3/17/4610/14100/1hour.html' 

        # Webのタグ情報を収集する
        r1,r2,r3,r4,r5,r6,r7,r8 = ProcessAllTagInfo(URL)

        # pandas
        df = ToPandasDataFrame2(r2,r3,r4,r5,r6,r7,r8)
        pd.set_option('display.max_rows', None)

        # DB/table drop
        TableDropAndCreate(dbname,tableName)

        # DB/ inseert
        dbc = DBconnection(dbname)
        df.to_sql("WeatherTable",dbc.connection,if_exists='append',index=None)
        dbc.Commit
        dbc.Close

        # DB/select、Treeview
        data = ProcessGetData(dbname,tableName)
        TreeDataImport(self.tree,data)

        # Entryの入力制限
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)
       
        # entryをすべて消す
        AllEntryInfoErase(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)

        # entryに「●●市」と入れる
        self.entry_9.insert(tk.END,prefecture + "のお天気情報")

        # entryを入力不可
        # Entryの入力制限
        AllEntryDisable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)


        # 通知
        PopUp0()
        



    def Push3(self,dbname,tableName):
        """
        ///1つのレコードを削除///
        Entry情報を読み取る
        IDがない場合、「できない」処理
        IDありの場合、「いいですか？」
        ID指定で、削除処理、完了通知
        """

        # 1=id, 2=sanagi, 3=name, 4=birth
        e1 = self.entry_1.get()
        e2 = self.entry_2.get()
        e3 = self.entry_3.get()
        e4 = self.entry_4.get()
        e5 = self.entry_5.get()
        e6 = self.entry_6.get()

        # IDが無い場合
        if e1 == "":
            PopUp3()
            return
        
        # IDがある場合
        else:
            # 処理前の確認
            res = PopUp4()

            # yesで抜けて進む
            if res =="yes":
                pass

            # noで終了処理
            else:
                return
        
        # DB接続
        dbc = DBconnection(dbname)
        #実行処理
        dbc.DeleteRecordData(tableName,e1)

        # COMMIT/CLOSE  
        dbc.Commit()
        dbc.Close()

       # DBを再読み込み
        df = ProcessGetData(dbname,tableName)

        # データ挿入
        TreeDataImport(self.tree,df)

        # 通知
        PopUp5()

    def Push4(self,dbname,tableName):
        """
        ///再読み込みボタン///
        ///DB読込みをしてツリービューに表示する///
        ツリービューのデータ削除、読み込み
        Entryのデータ削除
        """
        # DBを再読み込み
        data = ProcessGetData(dbname,tableName)

        # データ挿入
        TreeDataImport(self.tree,data)

        # ポップアップ通知
        PopUp6()



    def Push6(self,dbname,tableName):
        """
        ///テーブル削除、新規でテーブル作成する
        """
        # ------------------------------
        # 実行前の確認処理
        # ------------------------------
        res = PopUp4()

        # yesで抜けて進む
        if res =="yes":
            pass

        # noで終了処理
        else:
            return

        # テーブル削除、作成
        TableDropAndCreate(dbname,tableName)

        # DB/SELECT、ツリー表示
        # DBを再読み込み
        data = ProcessGetData(dbname,tableName)

        # データ挿入
        TreeDataImport(self.tree,data)

        # Entryの入力制限
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)
       
       # Entry欄の情報削除
        AllEntryInfoErase(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)

        # Entryの入力制限
        AllEntryDisable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6,self.entry_7,self.entry_8,self.entry_9)

        # 通知
        PopUp7()



    def Push10(self):
        """
        ///CSVの読み込み
        """
        # CSVファイルの保存先のチェック
        s1,s2,s3 = CheckCsvFolderExists()

        # ファイルダイヤログ表示、ファイル選択ができるように。
        filePath = OpenFileDialog(s1)

        # ダイヤログでキャンセルボタン押下の場合の処理
        if filePath == "":
            return

        # CSV読み込み / List型
        data = CsvOpenAndReader(filePath)

        # ツリーへデータ挿入
        TreeDataImport(self.tree,data)

        # 通知
        PopUp0()

    def Push11(self,dbname,tableName):
        """
        ///CSVの出力
        ///DBデータを抽出し、CSVファイルとして出力する
        """
        # CSVファイルの保存先のチェック
        s1,s2,s3 = CheckCsvFolderExists()

        # DB接続、データをSELECT*で引っ張る
        # DBを再読み込み
        data = ProcessGetData(dbname,tableName)

        # Pandas / Dataframeにする
        df = ToPandasDataFrame(data)

        # Timestamp
        Tstamp = GetTimeStamp()

        # CSVのファイルにする
        FldName = s2
        csvName = "_out.csv"
        dirName = FldName + "\\"    
        fileSavePath = dirName + Tstamp + csvName

        # CSVへ出力
        df.to_csv(fileSavePath,index=False,encoding='utf_8_sig')
        
        # 完了通知
        PopUp0()

    def Push12(self,dbname,tableName):
        """
        ///Matplotlib.tableの表jpgを出力、保存
        """
        # jpg保存先フォルダ有無のチェック
        s1,s2,s3 = CheckCsvFolderExists()

        # DB接続、データをSELECT*で引っ張る
        # DBを再読み込み
        data = ProcessGetData(dbname,tableName)

        # Pandas / Dataframeにする
        df = ToPandasDataFrame(data)

        # チェック/dfがない場合はSTOP
        if len(df)==0:
            PopUp11()
            return

        # Timestamp
        Tstamp = GetTimeStamp()

        # matplotに渡す
        fig = CreatePltTable(df)
        
        # Save as jpg
        SaveTablefig(fig,s3)

        # Matplotlib.table終了処理
        plt.clf()
        plt.close()

        # 通知
        PopUp0()

    def Push13(self,dbname,tableName):
        """
        ///MATPLOTチャートを出力し、表示する
        """
        # DBからデータをもらう
        data = ProcessGetData(dbname,tableName)

        # DFにする
        df = ToPandasDataFrame(data)

        # DF ⇒ MATPLOT
        chart = CreatPltChart(df)
        plt.show()

def CreatPltChart(df):
    """
    ///Matplotの表を作成する
    """
    # グラフ上限値を決めておく（5℃～25℃）
    tempMin = 10
    tempMax = 35
    humidMin = 0
    humidMax = 100
    windMin = 0
    windMax = 15
    precipiMin = 0
    precipiMax = 30

    x1 = df.hour
    y1 = df.temperature
    x2 = df.hour
    y2 = df.humidity
    x3 = df.hour
    y3 = df.windspeed
    x4 = df.hour
    y4 = df.precipitation

    # 日付情報取得
    td2 = GetTimeStamp()

    # fig1-------------------------------
    fig1 = plt.figure(figsize=(8,8))


    # (data)----------------------------
    chart1 = fig1.add_subplot(2,2,1)
    chart1.plot(x1, y1)
    plt.ylim(tempMin, tempMax)
    # グラフ内のラベル表記
    chart1.set_title(td2 + " / Temperature")
    chart1.set_xlabel("Time")
    chart1.set_ylabel("Temperature(℃)")

    # fig2-------------------------------
    #fig2 = plt.figure(td2 + "_01")
    # (data)----------------------------
    chart2 = fig1.add_subplot(2,2,2)
    chart2.plot(x2, y2)
    plt.ylim(humidMin, humidMax)
    # グラフ内のラベル表記
    chart2.set_title(td2 + " / Humidity")
    chart2.set_xlabel("Time")
    chart2.set_ylabel("Humidity(%)")

    # fig3-------------------------------
    #fig3 = plt.figure(td2 + "_01")
    # (data)----------------------------
    chart3 = fig1.add_subplot(2,2,3)
    chart3.plot(x3, y3)
    plt.ylim(windMin, windMax)
    # グラフ内のラベル表記
    chart3.set_title(td2 + " / WindSpeed")
    chart3.set_xlabel("Time")
    chart3.set_ylabel("WindSpeed(m/h)")

    # fig3-------------------------------
    #fig4 = plt.figure(td2 + "_01")
    # (data)----------------------------
    chart4 = fig1.add_subplot(2,2,4)
    chart4.plot(x4, y4)
    plt.ylim(windMin, windMax)
    # グラフ内のラベル表記
    chart4.set_title(td2 + " / Precipitation")
    chart4.set_xlabel("Time")
    chart4.set_ylabel("Precipitation(mm/h)")

    #-----------------------------
    # グラフの設定
    #-----------------------------
    fig1.tight_layout()

    #-----------------------------
    # 戻り値
    #-----------------------------
    fig_all = (fig1)
    return fig_all

# ====================================================================================================
# データベース
# ====================================================================================================
# ///基本情報：
# データベース名：butterfly.db
# テーブル名：SanagiTable
# カラム名：id,name,sanagi,prediction,birth,dif

class DBconnection:
    """
    データベース関係：
    """
    def __init__(self,dbname):
        """
        ///データベース接続///
        """
        self.connection = sqlite3.connect(dbname)
        self.cur = self.connection.cursor()

    def Commit(self):
        """
        ///データコミット///
        """
        r = self.connection.commit()
        return r

    def Close(self):
        """
        ///データベースクローズ///
        """
        r = self.cur.close()
        return r

    def Getdata(self,tableName):
        """
        ///データベースから情報取得///
        """
        r = self.cur.execute("SELECT * FROM %s" % tableName)
        r = r.fetchall()
        return r

    def Updatedata(self,tableName,e1,e2,e3,e4,e5,e6,e7,e8):
        """
        ///データベースに既存情報を書き換え・更新///
        """
        self.cur.execute("UPDATE %s SET hour=?,weather=?,temperature=?,humidity=?,windblow=? ,windspeed=?,precipitation=? WHERE id=?" % tableName,(e2,e3,e4,e5,e6,e7,e8,e1))

    def InsertData(self,tableName,e2,e3,e4,e5,e6,e7,e8):
        """
        ///データベースに、新規情報をインサートする///
        変数：テーブル名は%s、VALUESは?で。
        """
        self.cur.execute("INSERT INTO %s(hour,weather,temperature,himidity,windblow,windspeed,precipitation) VALUES(?,?,?,?,?,?,?)" % tableName,(e2,e3,e4,e5,e6,e7,e8))

    def DeleteRecordData(self,tableName,e1):
        """
        ///データベースから、特定の1つのレコードを削除する///
        注意：引数は(e1,)とタプルで渡すこと。(e1)だと文字列で誤解する

        """
        self.cur.execute("DELETE FROM %s WHERE id=%s" %(tableName,e1))

    def DropTable(self,tableName):
        """
        ///テーブル削除///
        """
        self.cur.execute("DROP TABLE %s" % tableName)

    def CreateTable(self,tableName):
        """
        ///Tableの作成///
        """
        sql = 'CREATE TABLE %s(id INTEGER PRIMARY KEY AUTOINCREMENT, hour INTEGER, weather STRING, temperature REAL, humidity REAL, windblow STRING, windspeed INTEGER, precipitation INTEGER )' % tableName
        self.cur.execute(sql)
    
    def CheckTableExistence(self,tableName):
        """
        ///DB内のテーブル名有無をチェック
        """
        r = self.cur.execute('SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="%s"' % tableName)
        return r



# ====================================================================================================
# function群
# 
# ====================================================================================================
# ==================================================
# function / データベース関係
# ==================================================
def ProcessGetData(dbname,tableName):
    """
    ///一連タスク：DB接続、SELECTで抽出、DataFrameでreturn///
    """
    dbc = DBconnection(dbname)
    dbc.connection
    dbc.cur
    data = dbc.Getdata(tableName)
    return data

# ==================================================
# function / Treeview関係
# ==================================================
def TreeDataImport(tree,data):
    """
    ///Treeviewへデータ挿入///
    ///SQLから抽出したリストを、Treeviewへinsert
    """
    # まずはツリー表示のデータをクリア
    tree.delete(*tree.get_children())

    # データ挿入
    a = len(data)

    for i in range(a):
        tree.insert("", "end", values=(data[i][0], data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],data[i][7]))
# ==================================================
# function / popup
# ==================================================
def PopUp0():
    """
    ///処理完了をユーザーへ通知する（汎用型）///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info','処理完了')


def PopUp1(id):
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info','書き込み完了しましたよん', detail="【ID】：" + id)

def PopUp2():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '新規の書き込み完了～♪')

def PopUp3():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '削除したい箇所を選択してね')

def PopUp4():
    """
    ///実行していいですか？///
    """
    res = messagebox.askquestion("注意", "実行していいですか？")
    return res

def PopUp5():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '削除完了')

def PopUp6():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '再読み込み完了')

def PopUp7():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', 'DBテーブル削除、新規作成完了')

def PopUp8():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '入力スペースに入力後、書き込みボタンを押してね')

def PopUp9():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', 'サナギになった日を入れてから、書き込みボタンを押してね')

def PopUp10():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '数字８文字でお願い～\n2020/5/20の場合は、\n20210520って感じで～')

def PopUp11():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', 'DB/テーブルがからっぽ\n処理できないっす')


def PopUp12():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '未入力だよ～')

def PopUp13():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '数字で入力しておくれ')

def PopUp14():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '数字を8文字で～～')

def PopUp15():
    """
    ///処理完了をユーザーへ通知する///
    """
    # メッセージボックス（情報） 
    messagebox.showinfo('Info', '入力チェック完了')

# ==================================================
# function / ファイル関係
# ==================================================
def ReadDataFromOterFile():
    """
    ///データファイルのリストを再リスト化する
    ///データファイルの要素数＝3
    ///使用したいデータ要素数＝5（追加：prediction,dif）
    """
    # データファイル
    import sanagi6_data
    l = sanagi6_data.l

    max = len(l)
    newList=[[]]

    # --------------------
    # edit data
    # --------------------
    for i in range(0,max,1):
        # Sanagi class
        s = Sanagi(l[i][0],l[i][1],l[i][2])
        newList = s.RenewList(newList)
    
    # 1行目からっぽなので削除
    newList.pop(0)

    return newList

# ==================================================
# function / データベース関係
# ==================================================
def TableExsistenceCheckAndCreate(dbname,tableName):
    """
    ///テーブル有無チェック後、テーブルを作る
    """
    dbc = DBconnection(dbname)
    cur = dbc.CheckTableExistence(tableName)

    # Check the Existence of table and Create the table
    if cur.fetchone() == (0,):
        print("Table is not existed then created")
        dbc.CreateTable(tableName)
    
    else:
        print('Table exists')

    dbc.Commit()
    dbc.Close()

def TableDropAndCreate(dbname,tableName):
    """
    ///テーブル削除、作成
    """
    dbc = DBconnection(dbname)

    # テーブル削除
    dbc.DropTable(tableName)
    dbc.Commit()
    
    # 新規テーブル作成
    dbc.CreateTable(tableName)
    dbc.Commit()

    # CLOSE  
    dbc.Close()

# ==================================================
# function / datetime関係
# ==================================================
def StrToDateTime(str):
    """
    ///文字列をDatetime型にする
    ///戻り値：datetime
    """
    r = datetime.datetime.strptime(str, '%Y%m%d')
    return r

def IntToTimedelta(n):
    """
    ///整数INTをtimedeltaにする（加減算用）
    ///戻り値：timedelta
    """
    r = datetime.timedelta(days = n)
    return r


# ==================================================
# function / Entry欄
# ==================================================
def AllEntryDisable(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6,entry_7,entry_8,entry_9):
    """
    ///Entry欄の入力を全て不可にする
    """
    entry_1.configure(state='disabled')
    entry_2.configure(state='disabled')
    entry_3.configure(state='disabled')
    entry_4.configure(state='disabled')
    entry_5.configure(state='disabled')
    entry_6.configure(state='disabled')
    entry_7.configure(state='disabled')
    entry_8.configure(state='disabled')
    entry_9.configure(state='disabled')

def AllEntryEnable(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6,entry_7,entry_8,entry_9):
    """
    ///Entry欄の入力を全て可能にする
    """
    entry_1.configure(state='normal')
    entry_2.configure(state='normal')
    entry_3.configure(state='normal')
    entry_4.configure(state='normal')
    entry_5.configure(state='normal')
    entry_6.configure(state='normal')
    entry_7.configure(state='normal')
    entry_8.configure(state='normal')
    entry_9.configure(state='normal')


def AllEntryInfoErase(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6,entry_7,entry_8,entry_9):
    """
    ///Entry欄の情報を全て削除する
    """
    entry_1.delete(0, tk.END) 
    entry_2.delete(0, tk.END) 
    entry_3.delete(0, tk.END) 
    entry_4.delete(0, tk.END) 
    entry_5.delete(0, tk.END) 
    entry_6.delete(0, tk.END)
    entry_7.delete(0, tk.END) 
    entry_8.delete(0, tk.END)
    entry_9.delete(0, tk.END) 


# ==================================================
# function / フォルダ
# ==================================================
def CheckCsvFolderExists():
    """
    ///CSVファイルの保存先フォルダ有無チェック、作成///
    ///戻り値：フォルダ名（string）
    """
    # 探すべきフォルダ名
    s1 = "csv_read_fld"
    s2 = "csv_out_fld"
    s3 = "table_out_fld"

    s_array = (s1,s2,s3)

    for s in s_array:
        if not os.path.exists(s):
            # ディレクトリが存在しない場合、ディレクトリを作成する
            print("Not exists, and created")
            os.makedirs(s)

    return s1,s2,s3

# ==================================================
# function / dataframe
# ==================================================
def ToPandasDataFrame(data):
    """
    ///Pandas dataframeにする
    引数：data(DB)
    戻値：データフレーム
    """
    col1 = "id"
    col2 = "hour"
    col3 = "weather"
    col4 = "temperature"
    col5 = "humidity"
    col6 = "windblow"
    col7 = "windspeed"
    col8 = "precipitation"

    df = pd.DataFrame(data,
                    columns=[
                    col1,
                    col2,
                    col3,
                    col4,
                    col5,
                    col6,
                    col7,
                    col8
                    ])
    return df

def ToPandasDataFrame2(r2,r3,r4,r5,r6,r7,r8):
    """
    ///Pandas dataframeにする
    引数：リスト
    戻値：データフレーム
    """
    col2 = "hour"
    col3 = "weather"
    col4 = "temperature"
    col5 = "humidity"
    col6 = "windblow"
    col7 = "windspeed"
    col8 = "precipitation"

    df = pd.DataFrame({
                        col2:r2,
                        col3:r3,
                        col4:r4,
                        col5:r5,
                        col6:r6,
                        col7:r7,
                        col8:r8
                        })
    return df




# =============================================================================================
# function
# =============================================================================================
def CreateHourList(l):
    """
    ///hourの値を調整
    「0～24、0～24、0～24」の塊になっているので「0～72」にする
    """
    r=[]
    loopnum=len(l)

    for i in range(0,loopnum,1):
        if i<=23:
            r.append(int(l[i]))
        elif i>=24 and i<=47:
            r.append(int(l[i])+24)
        elif i>=48:
            r.append(int(l[i])+48)
    return r

def ChangeTypeStrToFloat(l):
    """
    ///文字列型をFLOAT型に変換する
    引数：リスト
    戻値：リスト
    """
    r = [float(s) for s in l]
    return r

def ChangeTypeStrToInt(l):
    """
    ///文字列型をFLOAT型に変換する
    引数：リスト
    戻値：リスト
    """
    r = [int(s) for s in l]
    return r




def ProcessAllTagInfo(URL):
    """
    ///htmlから必要なタグ情報だけを抽出
    引数：URL
    戻値：タグ情報（リスト型）
    """
    # --------------
    # 1.日時（3日分＝3こ）
    # --------------
    a = 'tr'
    b = 'head'
    c = 'p'
    r1 = ProcessScraping(URL,a,b,c)

    # --------------
    # 2.時刻
    # --------------
    a = 'tr'
    b = 'hour'
    c = 'span'
    r2 = ProcessScraping(URL,a,b,c)

    # [0～24]×3 ⇒ [0～72]にする
    r2 = CreateHourList(r2)

    # Str⇒intに変換
    r2 = ChangeTypeStrToInt(r2)

    # --------------
    # 3.天気 / 日本語
    # --------------
    a = 'tr'
    b = 'weather'
    c = 'p'
    r3 = ProcessScraping(URL,a,b,c)

    # --------------
    # 4.気温
    # --------------
    a = 'tr'
    b = 'temperature'
    c = 'span'
    r4 = ProcessScraping(URL,a,b,c)

    # Str⇒floatに変換
    r4 = ChangeTypeStrToFloat(r4)

    # --------------
    # 5.湿度
    # --------------
    a = 'tr'
    b = 'humidity'
    c = 'td'
    r5 = ProcessScraping(URL,a,b,c)

    # Str⇒floatに変換
    r5 = ChangeTypeStrToFloat(r5)

    # --------------
    # 6.風向き / 日本語
    # --------------
    a = 'tr'
    b = 'wind-blow'
    c = 'p'
    r6 = ProcessScraping(URL,a,b,c)

    # --------------
    # 7.風速
    # --------------
    a = 'tr'
    b = 'wind-speed'
    c = 'span'
    r7 = ProcessScraping(URL,a,b,c)

    # Str⇒intに変換
    r7 = ChangeTypeStrToInt(r7)

    # --------------
    # 8.雨量
    # --------------
    a = 'tr'
    b = 'precipitation'
    c = 'span'
    r8 = ProcessScraping(URL,a,b,c)

    # Str⇒intに変換
    r8 = ChangeTypeStrToInt(r8)

    return r1,r2,r3,r4,r5,r6,r7,r8























# ==================================================
# function / ファイルダイヤログ
# ==================================================
def OpenFileDialog(s1):
    """
    ///ファイルダイヤログを開き、ファイル選択可能な状態に
    ///戻り値：ファイルパス
    """
    #dirName = "csv_read_fld/"
    dirName = s1 + "/"
    typeList = [('CSVファイル','*.csv')] 
    filename = filedialog.askopenfilename(
                title = "画像ファイルを開く",
                filetypes = typeList,
                initialdir = dirName
                )
    
    return filename

def CsvOpenAndReader(filePath):
    """
    ///CSV読込み、リストにして戻す
    ///戻り値：リスト
    """
    with open(filePath,'r',encoding="utf-8") as f:
        reader = csv.reader(f)

        # 1行ごとに読み込み、リストにする
        l = [row for row in reader]

        # 0行目（ラベル情報）のため削除
        l.pop(0)

    return l

def GetTimeStamp():
    """
    ///ファイル保存用のタイムスタンプ文字列
    ///戻り値：文字列
    """
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y_%m%d_%H%M_%S')
    return dt


def CreatePltTable(df):
    """
    ///Matplotlib.tableで表を作成する
    
    """
    titleName= "サナギ羽化観察"
    plt.rcParams["font.family"] = "IPAexGothic"

    # index number(1-)
    length = len(df)

    
    row_names=[]
    for i in range(1,length + 1,1):
        row_names.append(i)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.set(title= titleName)
    ax.axis('off')
    ax.axis('tight')
    
    tb = ax.table(cellText=df.values,
            colLabels=df.columns,rowLabels=row_names,loc='upper center', 
            bbox=[0, 0, 1, 1],
            )

    return fig


# save table image as jpg file(Weather info as table)
def SaveTablefig(fig,fldname):
    """
    ///Matplotlib.tableをJPG保存する
    """
    currentdir = os.getcwd()
    figName = "Sanagi"
    timestamp = GetTimeStamp()
    figfldName = "/" + fldname + "/"
    fig.savefig(currentdir  + figfldName + timestamp + figName + "_.jpg")



# ====================================================================================================
# ウィジェット起動/メイン
# ====================================================================================================
root = tk.Tk()
app = Application(master=root)
app.mainloop()