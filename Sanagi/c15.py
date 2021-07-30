# ==================================================
# library
# ==================================================
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import pandas as pd
import datetime
import os
import csv
import sys
import matplotlib.pyplot as plt
import japanize_matplotlib

"""
できあがったDBデータを出力、・CSV出力、・matplot.table/jpg
"""
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
        self.master.geometry("1800x900+0+0")

        # ウィンドウのタイトル
        self.master.title("アゲハチョウの羽化観察")

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
        # テーブル有無確認、無ければ作成
        TableExsistenceCheckAndCreate()

        # -------------------------
        # データ読込み
        # -------------------------
        # DB / table名
        tableName="SanagiTable"

        # data
        data = ProcessGetData(tableName)

        # -------------------------
        # master / frame
        # -------------------------
        #tcl_isOk = self.register(IsOk)
        self.frame1 = tk.Frame(self, width=800, height=100)   
        self.frame2 = tk.Frame(self, width=800, height=300)
        self.frame3 = tk.Frame(self, width=800, height=100)
        self.frame4 = tk.Frame(self, width=800, height=100)
        self.frame5 = tk.Frame(self, width=800, height=100)
        self.frame1.grid(column=0,row=0,padx=5,pady=5)
        self.frame2.grid(column=0,row=1,padx=5,pady=5)
        self.frame3.grid(column=0,row=2,padx=5,pady=5)
        self.frame4.grid(column=0,row=3,padx=5,pady=5)
        self.frame5.grid(column=0,row=4,padx=5,pady=5)

        # --------------------------------------------------
        # 【変数】ウィジェット間距離など
        # --------------------------------------------------
        pad_x1 = 10
        pad_y1 = 3
        width1 = 20
        width2 = 30
        Lbl_name1 = "ID"
        Lbl_name2 = "名前"
        Lbl_name3 = "サナギになった日"
        Lbl_name4 = "羽化予想日"
        Lbl_name5 = "羽化した日"
        Lbl_name6 = "実日数"
        Lbl_name7 = "羽化まで日数"
        fontsize1 = 15
        fontsize2 = 12

        # Entry欄のheight
        ipady_1 = 15

        # 羽化に必要な日数
        need_sanagiDay=10

        # --------------------------------------------------
        # frame1 / button
        # --------------------------------------------------
        self.btn_2= tk.Button(self.frame1, text = '新規登録', command=self.WritePush2,font=("",fontsize1))
        self.btn_2.grid(column=0,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_4= tk.Button(self.frame1, text = 'ＤＢ読込み', command=lambda:self.WritePush4(tableName),font=("",fontsize1))
        self.btn_4.grid(column=2,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_6= tk.Button(self.frame1, text = 'テーブル削除/作成', command=lambda:self.WritePush6(tableName),font=("",fontsize1))
        self.btn_6.grid(column=3,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_5= tk.Button(self.frame1, text = '開発用/元データ呼び出し', command=self.WritePush5,font=("",fontsize1))
        self.btn_5.grid(column=4,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_9= tk.Button(self.frame1, text = 'CSV読み込み', command=self.WritePush10,font=("",fontsize1))
        self.btn_9.grid(column=5,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_10= tk.Button(self.frame1, text = 'CSV出力', command=self.WritePush11,font=("",fontsize1))
        self.btn_10.grid(column=6,row=0,padx=pad_x1,pady=pad_y1)

        self.btn_11= tk.Button(self.frame1, text = '表jpg出力', command=self.WritePush12,font=("",fontsize1))
        self.btn_11.grid(column=7,row=0,padx=pad_x1,pady=pad_y1)

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
        self.Label_7.grid(column=0,row=3,padx=pad_x1,pady=pad_y1)
        self.entry_7 = tk.Entry(self.frame2, width=width2, bg='white',fg='black',justify='center',font=("",fontsize2))
        self.entry_7.insert(tk.END,need_sanagiDay)
        self.entry_7.grid(column=0,row=4,padx=pad_x1,pady=pad_y1,ipady=ipady_1)

        # 入力不可 / Entry1=ID
        self.entry_1.configure(state='disabled')
        
        # --------------------------------------------------
        # frame3 / button
        # --------------------------------------------------

        # チェックボタン
        self.btn_8= tk.Button(self.frame3, text = '入力チェック', command=self.WritePush9,width=30,font=("",fontsize1))
        self.btn_8.grid(column=0,row=0,padx=pad_x1,pady=pad_y1)

        # 書き込みボタン
        self.btn_1= tk.Button(self.frame3, text = '書き込み', command=lambda:self.WritePush1(tableName),width=30,font=("",fontsize1))
        self.btn_1.grid(column=1,row=0,padx=pad_x1,pady=pad_y1)

        # 削除ボタン
        self.btn_3= tk.Button(self.frame3, text = '削除処理', command=lambda:self.WritePush3(tableName),width=30,font=("",fontsize1))
        self.btn_3.grid(column=2,row=0,padx=pad_x1,pady=pad_y1)

        # -------------------------
        # frame4 / treeview
        # -------------------------
        self.tree = ttk.Treeview(self.frame4, height = 20, style='Treeview')

        # treeの設定
        self.tree["columns"] = (1,2,3,4,5,6)
        self.tree["show"] = "headings"
        self.tree.column(1, width=200,anchor=tk.CENTER)
        self.tree.column(2, width=200,anchor=tk.CENTER)
        self.tree.column(3, width=200,anchor=tk.CENTER)
        self.tree.column(4, width=200,anchor=tk.CENTER)
        self.tree.column(5, width=200,anchor=tk.CENTER)
        self.tree.column(6, width=200,anchor=tk.CENTER)
        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="名前")
        self.tree.heading(3, text="サナギになった日")
        self.tree.heading(4, text="羽化予想日")
        self.tree.heading(5, text="羽化した日")
        self.tree.heading(6, text="実日数")
        
        # --------------------------------------------------
        # frame5 / Quit button
        # --------------------------------------------------
        self.btn_2= tk.Button(self.frame5, text="閉じる", fg="black",command=self.master.destroy,font=("",fontsize1))
        self.btn_2.grid(column=0,row=0,padx=pad_x1,pady=pad_y1)

        # --------------------------------------------------
        # Entry入力不可状態
        # --------------------------------------------------
        AllEntryDisable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)

        # --------------------------------------------------
        #ツリー内をマウスで選択した時
        # --------------------------------------------------
        self.tree.bind("<<TreeviewSelect>>", self.OnTreeSelect)

        # pack
        self.tree.pack()

        # DB/Tableの有無のチェック、無ければ作成する
        TableExsistenceCheckAndCreate()


    def OnTreeSelect(self,event):     
        """
        ///ツリービュー内の情報を選択したときの処理///
        """
        # Entryの入力可能処理
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)

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
        
        # Entry1への入力受付可能に設定
        #self.entry_1.configure(state='normal')

        # 中身をいったん消してから/データ挿入
        self.entry_1.delete(0, tk.END)  
        self.entry_1.insert(tk.END,d1)
        self.entry_2.delete(0, tk.END)  
        self.entry_2.insert(tk.END,d2)
        self.entry_3.delete(0, tk.END)  
        self.entry_3.insert(tk.END,d3)
        self.entry_4.delete(0, tk.END)  
        self.entry_4.insert(tk.END,d4)
        self.entry_5.delete(0, tk.END)  
        self.entry_5.insert(tk.END,d5)
        self.entry_6.delete(0, tk.END)  
        self.entry_6.insert(tk.END,d6)

        # Entry制限
        self.entry_1.configure(state='disabled')
        self.entry_4.configure(state='disabled')
        self.entry_6.configure(state='disabled')

    def WritePush1(self,tableName):
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
        # メイン処理の開始
        #-------------------------------
        # Entry欄の情報取得
        e1 = self.entry_1.get()
        e2 = self.entry_2.get()
        e3 = self.entry_3.get()
        e4 = self.entry_4.get()
        e5 = self.entry_5.get()
        e6 = self.entry_6.get()

        # DB接続し、
        dbc = DBconnection()

        # UPDATE/INSERTの振り分け
        if e1 != "":

            # データ/UPDATE
            dbc.Updatedata(tableName,e1,e2,e3,e4,e5,e6)

        else:
            # データ/INSERT
            dbc.InsertData(tableName,e2,e3,e4,e5,e6)

        # DB COMMIT/CLOSE
        dbc.Commit()
        dbc.Close()

        # DBを再読み込み
        data = ProcessGetData(tableName)

        # データ挿入
        TreeDataImport(self.tree,data)

        # ポップアップ通知
        if e1 != "":
            PopUp1(e1)
        else:    
            PopUp2()

    def WritePush2(self):
        """
        ///新規登録時の処理///
        """
        # Entryへの入力受付可能に設定
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)

        # 中身を消す
        self.entry_1.delete(0, tk.END)  
        self.entry_2.delete(0, tk.END)  
        self.entry_3.delete(0, tk.END)  
        self.entry_4.delete(0, tk.END) 
        self.entry_5.delete(0, tk.END)
        self.entry_6.delete(0, tk.END)
        self.entry_7.delete(0, tk.END)

        # 初期値を入れる

        self.entry_7.insert(tk.END,"10") 

        # 一部のEntryへの入力不可にする
        self.entry_1.configure(state='disabled')
        self.entry_4.configure(state='disabled')
        self.entry_6.configure(state='disabled')

        # 通知
        PopUp8()

    def WritePush3(self,tableName):
        """
        ///ツリー上のいずれかのデータを削除する処理
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
        dbc = DBconnection()
        #実行処理
        dbc.DeleteRecordData(tableName,e1)

        # COMMIT/CLOSE  
        dbc.Commit()
        dbc.Close()

       # DBを再読み込み
        df = ProcessGetData(tableName)

        # データ挿入
        TreeDataImport(self.tree,df)

        # 通知
        PopUp5()

    def WritePush4(self,tableName):
        """
        ///再読み込みボタン：DB読込みをしてツリービューに表示する///
        ツリービューのデータ削除、読み込み
        Entryのデータ削除
        """
        # DB接続し、
        dbc = DBconnection()

        # DBを再読み込み
        data = ProcessGetData(tableName)

        # データ挿入
        TreeDataImport(self.tree,data)

        # ポップアップ通知
        PopUp6()

    def WritePush5(self):
        """
        ///特定ファイルのデータリストを読み込み、DBへ登録しなおす。///
        ///データの初期化///
        """
        # sanagi_data.pyからリスト取り出し
        v = ReadDataFromOterFile()

        # DB接続、INSERT
        # DB接続
        tableName="SanagiTable"
        dbc = DBconnection()
        #sql1 = 'INSERT INTO SanagiTable(name,sanagi,prediction,birth,dif) VALUES(?,?,?,?,?)'
        sql1 = "INSERT INTO %s(name,sanagi,prediction,birth,dif) VALUES(?,?,?,?,?)" % tableName
        
        # ループ回数確認
        numberElements = len(v)
        minLoopNumber = int(numberElements)

        # SQL実行/INSERT
        for i in range(0,minLoopNumber,1):
            dbc.cur.execute(sql1,(v[i][0],v[i][1],v[i][2],v[i][3],v[i][4]))

        dbc.Commit()

        # 最新データ取り出し
        d = dbc.cur.execute("SELECT * FROM SanagiTable")
        data = d.fetchall()

        # DB閉じる
        dbc.Close()

        # Treeview
        TreeDataImport(self.tree,data)

        # Entryの入力制限
        AllEntryDisable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)

        # ポップアップ通知
        PopUp6()

    def WritePush6(self,tableName):
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
        TableDropAndCreate()

        # DB/SELECT、ツリー表示
        # DB接続し、
        dbc = DBconnection()

        # DBを再読み込み
        df = ProcessGetData(tableName)

        # データ挿入
        TreeDataImport(self.tree,df)

        # Entryの入力制限
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)
       
       # Entry欄の情報削除
        AllEntryInfoErase(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)

        # Entryの入力制限
        AllEntryDisable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)

        # 通知
        PopUp7()

    def WritePush8(self):
        """
        ///入力チェックを行う処理
        ///新規登録押下後のアクション
        """
        # Entry欄の情報取得
        e1 = self.entry_1.get()
        e2 = self.entry_2.get()
        e3 = self.entry_3.get()
        e4 = self.entry_4.get()
        e5 = self.entry_5.get()
        e6 = self.entry_6.get()
        e7 = self.entry_7.get()
        
        # 未入力の場合の処理
        if e3 =="":
            #(命令：entry6を削除するべき)
            return

        # 文字列「0」の時
        elif e3=="0":
            #(命令：entry6を削除するべき)
            return

        # 「-」が含まれる場合、replaceする
        elif e3.find('-'):
            e3 = e3.replace('-', '')

        # 文字列数のチェック
        if len(e3) != 8:
            return
        
        # -----------------------
        # 羽化予想日の計算
        # -----------------------
        # サナギになった日/datetime型
        dt_e3 = StrToDateTime(e3)

        # 羽化必要日数を取得してdatetimedelta型へ
        dt_e7 = int(e7)
        dt_needsanagi = IntToTimedelta(dt_e7)

        # 日にちの計算
        dt_prediction = dt_e3 + dt_needsanagi
        dt_prediction = dt_prediction.date()

        # -----------------------
        # 羽化に要した日数の計算
        # e5 / 羽化した日の情報のチェック
        # -----------------------

        # 文字列なしの時
        if e5 =="":
            #(命令：entry6を削除するべき)
            return

        # 文字列「0」の時
        elif e5=="0":
            #(命令：entry6を削除するべき)
            return

        # 「-」が含まれる場合、replaceする
        elif e5.find('-'):
            e5 = e5.replace('-', '')

        # 文字列数のチェック
        if len(e5) != 8:
            return
        
        # datetime型
        dt_e5 = StrToDateTime(e5)
        dt_dif = (dt_e5 - dt_e3).days

        # -----------------------
        # データ反映
        # 未入力でボタン押下の場合、動作しないように。
        # -----------------------
        dt_e3 = dt_e3.strftime('%Y-%m-%d')
        dt_e5 = dt_e5.strftime('%Y-%m-%d')

        self.entry_3.configure(state='normal')
        self.entry_3.delete(0, tk.END) 
        self.entry_3.insert(tk.END,dt_e3)

        # 羽化予想日
        self.entry_4.configure(state='normal')
        self.entry_4.delete(0, tk.END) 
        self.entry_4.insert(tk.END,dt_prediction)
        self.entry_4.configure(state='disabled')
     
        self.entry_5.configure(state='normal')
        self.entry_5.delete(0, tk.END) 
        self.entry_5.insert(tk.END,dt_e5)

        # 羽化実日数
        self.entry_6.configure(state='normal')
        self.entry_6.delete(0, tk.END) 
        self.entry_6.insert(tk.END,dt_dif)
        self.entry_6.configure(state='disabled')

    def WritePush9(self):
        """
        ///入力チェックを行う処理
        ///新規登録押下後のアクション
        7/14:再構築
        """
        # Entry欄の情報取得
        e1 = self.entry_1.get()
        e2 = self.entry_2.get()
        e3 = self.entry_3.get()
        e4 = self.entry_4.get()
        e5 = self.entry_5.get()
        e6 = self.entry_6.get()
        e7 = self.entry_7.get()

        # 入力情報有無のチェック
        # Select時、e1,e4,e6：disable
        # 入力必要：e3,e5,e7
        if e3=="" or e5=="" or e7=="":
            PopUp12()
            return

        # ------------------------------
        # e3チェック
        # ------------------------------ 
        # 2021-05-21と入力を期待する
        # 20210521の場合はそのまま通す
        if "-" in e3:
            e3 = e3.replace('-', '')

        # 数字以外の文字列の場合はstop
        if e3.isdigit()==False:
            PopUp13()
            return

        # 数字入力は20210501と、8文字
        if len(e3)!=8:
            PopUp14()
            return

        # ------------------------------
        # e5のチェック
        # ------------------------------
        # Birth:2021-05-30を期待する
        # 0という場合もある
        if "-" in e5:
            e5 = e5.replace('-', '')

        # 数字以外の文字列の場合はstop
        if e5.isdigit()==False:
            PopUp13()
            return
        
        # 0という入力の場合、そのままにしておく
        if e5=="0":
            e5="0"

        # 0以外で、数字入力は20210501と、8文字
        elif len(e5)!=8:
            PopUp14()
            return

        # ------------------------------
        # e7のチェック
        # ------------------------------
        # 羽化に必要な日数＝10（デフォルト）

        # 数字以外の文字列の場合はstop
        if e7.isdigit()==False:
            PopUp13()
            return
        
        # ------------------------------
        # 入力チェック終了
        # 計算の開始
        # ------------------------------
        # ------------------------------
        # e4 羽化予定日
        # ------------------------------
        # e3+e7で、予定日を算出する

        # e3 / datetime型
        e3 = StrToDateTime(e3)

        # e7 / timedelta
        e7 = IntToTimedelta(int(e7))

        # e3+e7
        e4 = e3 + e7

        # ------------------------------
        # e6 実日数
        # ------------------------------
        # e5-e3で、日数を算出する
        
        # e3 / datetime型
        e5 = StrToDateTime(e5)

        # e5-e3
        e6 = e5-e3
        e6 = int(e6.days)

        # ------------------------------
        # Entryへのデータ反映
        # ------------------------------
        
        # 反映前のデータ準備
        e3 = e3.date()
        e4 = e4.date()
        e5 = e5.date()
        e7 = e7.days

        # Entryの入力制限
        AllEntryEnable(self.entry_1,self.entry_2,self.entry_3,self.entry_4,self.entry_5,self.entry_6)
    
        # Entry1～7へデータ反映
        self.entry_1.delete(0, tk.END) 
        self.entry_1.insert(tk.END,e1)

        self.entry_2.delete(0, tk.END) 
        self.entry_2.insert(tk.END,e2)

        self.entry_3.delete(0, tk.END) 
        self.entry_3.insert(tk.END,e3)

        self.entry_4.delete(0, tk.END) 
        self.entry_4.insert(tk.END,e4)

        self.entry_5.delete(0, tk.END) 
        self.entry_5.insert(tk.END,e5)

        self.entry_6.delete(0, tk.END) 
        self.entry_6.insert(tk.END,e6)

        self.entry_7.delete(0, tk.END) 
        self.entry_7.insert(tk.END,e7)

        # Entry / disable
        self.entry_1.configure(state='disabled')
        self.entry_4.configure(state='disabled')
        self.entry_6.configure(state='disabled')

        # 通知
        PopUp15()

    def WritePush10(self):
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
        print(data)

        # ツリーへデータ挿入
        TreeDataImport(self.tree,data)

        # 通知
        PopUp0()

    def WritePush11(self):
        """
        ///CSVの出力
        ///DBデータを抽出し、CSVファイルとして出力する
        """
        # CSVファイルの保存先のチェック
        s1,s2,s3 = CheckCsvFolderExists()

        # DB接続、データをSELECT*で引っ張る
        # DB接続し、
        dbc = DBconnection()

        # tablename
        tableName = "SanagiTable"

        # DBを再読み込み
        data = ProcessGetData(tableName)

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

    def WritePush12(self):
        """
        ///Matplotlib.tableの表jpgを出力、保存
        """
        # jpg保存先フォルダ有無のチェック
        s1,s2,s3 = CheckCsvFolderExists()

        # DB接続、データをSELECT*で引っ張る
        # DB接続し、
        dbc = DBconnection()

        # tablename
        tableName = "SanagiTable"

        # DBを再読み込み
        data = ProcessGetData(tableName)

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
    def __init__(self):
        """
        ///データベース接続///
        """
        dbname='butterfly.db'

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
        #tableName='SanagiTable'
        r = self.cur.execute("SELECT * FROM %s" % tableName)
        r = r.fetchall()
        return r

    def Updatedata(self,tableName,e1,e2,e3,e4,e5,e6):
        """
        ///データベースに既存情報を書き換え・更新///
        """
        self.cur.execute("UPDATE %s SET name=?,sanagi=?,prediction=?,birth=?,dif=? WHERE id=?" % tableName,(e2,e3,e4,e5,e6,e1))

    def InsertData(self,tableName,e2,e3,e4,e5,e6):
        """
        ///データベースに、新規情報をインサートする///
        変数：テーブル名は%s、VALUESは?で。
        """
        self.cur.execute("INSERT INTO %s(name,sanagi,prediction,birth,dif) VALUES(?,?,?,?,?)" % tableName,(e2,e3,e4,e5,e6))

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
        ///SanagiTableの作成///
        """
        sql = 'CREATE TABLE SanagiTable(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, sanagi DATE, prediction DATE, birth DATE, dif INTEGER)'
        self.cur.execute(sql)
    
    def CheckTableExistence(self,tableName):
        """
        ///DB内のテーブル名有無をチェック
        """
        r = self.cur.execute('SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="%s"' % tableName)
        return r

# ====================================================================================================
# Sanagiの再リスト化
# ほかファイルから再配列するためのもの
# データがないときは、ここから持ってくる（開発用）
# ====================================================================================================
class Sanagi:
    def __init__(self, s, n, b):
        """
        ///サナギ観察データ保持をするための情報の再配列///
        """
        dt_needsanagi = datetime.timedelta(days = 10)
        self.sanagi = s
        self.name = n
        self.prediction = s + dt_needsanagi
        self.birth = b
        
        if self.birth != 0:
            self.dif = (self.birth - self.sanagi).days
        else:
            self.dif = 0
        
    def RenewList(self,newList):
        newList.append([self.name,self.sanagi,self.prediction, self.birth, self.dif])
        return newList

    def Print(self):
        print(self.name, self.sanagi,self.prediction, self.birth, self.dif)


# ====================================================================================================
# function群
# 
# ====================================================================================================
# ==================================================
# function / データベース関係
# ==================================================
def ProcessGetData(tableName):
    """
    ///一連タスク：DB接続、SELECTで抽出、DataFrameでreturn///
    """
    #tableName = "SanagiTable"
    bf = DBconnection()
    bf.connection
    bf.cur
    data = bf.Getdata(tableName)
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
        tree.insert("", "end", values=(data[i][0], data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]))
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
    import sanagi5_data
    l = sanagi5_data.l

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
def TableExsistenceCheckAndCreate():
    """
    ///テーブル有無チェック後、テーブルを作る
    """
    dbc = DBconnection()
    tableName = "SanagiTable"
    cur = dbc.CheckTableExistence(tableName)

    # Check the Existence of table and Create the table
    if cur.fetchone() == (0,):
        print("SanagiTable is not existed then created")
        dbc.CreateTable(tableName)
    
    else:
        print('SanagiTable exists')

    dbc.Commit()
    dbc.Close()

def TableDropAndCreate():
    """
    ///テーブル削除、作成
    """
    dbc = DBconnection()
    tableName = "SanagiTable"

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

"""
def IsOk(diff):
    #///半角数字の入力のみ受け付ける

    if not diff.encode('utf-8').isdigit():
        # 妥当でない（半角数字でない）場合はFalseを返却
        print("false")
        return False

    # 妥当（半角数字である）の場合はTrueを返却
    print("true")
    return True
"""

# ==================================================
# function / Entry欄
# ==================================================
def AllEntryDisable(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6):
    """
    ///Entry欄の入力を全て不可にする
    """
    entry_1.configure(state='disabled')
    entry_2.configure(state='disabled')
    entry_3.configure(state='disabled')
    entry_4.configure(state='disabled')
    entry_5.configure(state='disabled')
    entry_6.configure(state='disabled')

def AllEntryEnable(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6):
    """
    ///Entry欄の入力を全て可能にする
    """
    entry_1.configure(state='normal')
    entry_2.configure(state='normal')
    entry_3.configure(state='normal')
    entry_4.configure(state='normal')
    entry_5.configure(state='normal')
    entry_6.configure(state='normal')


def AllEntryInfoErase(entry_1,entry_2,entry_3,entry_4,entry_5,entry_6):
    """
    ///Entry欄の情報を全て削除する
    """
    entry_1.delete(0, tk.END) 
    entry_2.delete(0, tk.END) 
    entry_3.delete(0, tk.END) 
    entry_4.delete(0, tk.END) 
    entry_5.delete(0, tk.END) 
    entry_6.delete(0, tk.END) 


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
    ///戻り値：データフレーム
    """
    #columnsArray = ["name", "sanagi", "prediction", "birth", "dif"]
    df = pd.DataFrame(data,columns=["id","name", "sanagi", "prediction", "birth", "dif"])
    return df

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
    dt = dt.strftime('%Y_%m%d_%H%M%S')
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