#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import rospy
import rosparam
import tkinter as tk
import yaml
import os

os.chdir( os.path.abspath(os.path.dirname(__file__)))

# GUIパーツ
root = tk.Tk()
root.title("ROSLauncher")

# windowを自動で閉じるかどうか
is_auto_close = tk.BooleanVar()
is_auto_close.set(True)

# 実行ボタンを配置するframe
frame_launcher = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
parts = []

commands = {}

class Command():
    def __init__(self, name, com, opt ):
        self.com = com
        self.opt = opt
        self.name = name
    
    def __call__(self):
        print( "call", self.com, self.opt.get() )

        command =  'gnome-terminal --tab --active --title ' + self.name + ' -- bash -c "' + self.com + ' ' + self.opt.get()
        
        if not is_auto_close.get():
            command += '; bash"'
        else:
            command += '"'

        print(command)
        os.system( command.encode("utf8") )

def selection_changed( pname ):
    # 表示されているGUIを消去
    for p in parts:
        p.pack_forget()

    for command in commands[pname]:
        name = command["name"]
        com = command["command"]
        opt = ""

        if "option" in command and command["option"]!=None:
            opt = command["option"]

        frame = tk.Frame(frame_launcher)
        frame.pack()
        parts.append( frame )

        tk.Label(frame, text=name, width=30  ).pack(side="left")
        #opt_entry = tk.Entry(frame, textvariable=tk.StringVar(frame, opt), width=30 )
        opt_entry = tk.Entry(frame, textvariable=command["opt_string"], width=30 )
        opt_entry.pack(side="left")
        tk.Button( frame, text='laucnch', command=Command(name, com, opt_entry) ).pack(side="left")


def main():
    # コマンドを読み込み
    global commands
    with open('launcher_settings.yaml') as file:
        commands = yaml.safe_load(file)
    packages = commands.keys()

    for pack in packages:
        for com in commands[pack]:
            name = com["name"]
            opt = ""
            if "option" in com and com["option"]!=None:
                opt = com["option"]
            com["opt_string"] = tk.StringVar(root, opt)

    frame = tk.Frame(root)
    frame.pack()

    tk.Label(frame, text="package:" ).pack(side="left")

    # パッケージ選択のプルダウンメニュー
    opt = tk.OptionMenu(frame, tk.StringVar(frame, "general"), *packages, command=selection_changed )
    opt.config(width=50 )
    opt.pack(side="left")

    # windowを自動で閉じるかどうかのチェックボックス
    tk.Checkbutton( frame, variable=is_auto_close ,text="終了したウィンドウを自動で閉じる" ).pack(side="left")

    # 初期選択
    selection_changed( "general" )

    frame_launcher.pack()
    root.mainloop()
        
if __name__ == "__main__":
    main()
