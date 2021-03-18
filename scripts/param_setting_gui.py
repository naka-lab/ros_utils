#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import rospy
import rosparam
from collections import defaultdict
import tkinter as tk

# パラメータ名保存用dict
param_dict = defaultdict(list)

# GUIパーツ
root = tk.Tk()
text_ns = tk.StringVar()
frame_param = tk.Frame(root, relief=tk.GROOVE, borderwidth=2)
parts = []

# setボタン押下時にGUIから値を読み込み送信するクラス
class SetVar():
    def __init__(self, pname, entry ):
        self.pname = pname
        self.entry = entry
    
    def __call__(self):
        print( "set param:" )
        print("  ", self.pname)
        print("  ", self.entry.get())
        rospy.set_param( self.pname, eval(self.entry.get()) )

# refreshボタン押下時の動作。選択されたnamespaceでGUIを生成
def button_refresh():
    ns = text_ns.get()
    pnames = param_dict[ns]

    print("Load :", ns) 

    # 表示されているGUIを消去
    for p in parts:
        p.pack_forget()

    # 選択されたnamespaceで新たにGUIを生成
    for i in range(len(pnames)):
        pname = pnames[i]
        var = rosparam.get_param( pname )
        print("  ", pname, var)

        frame = tk.Frame(frame_param)
        frame.pack()
        parts.append( frame )

        tk.Label(frame, text=pnames[i], width=50  ).pack(side="left")
        entry = tk.Entry(frame, textvariable=tk.StringVar(frame, str(var)), width=50)
        entry.pack(side="left")

        tk.Button( frame, text='set', command=SetVar(pname, entry) ).pack(side="left")

def main():
    rospy.init_node("param_setting_gui")

    print("parameters: ")
    params_all = rosparam.list_params("/")
    for p in params_all:
        split_p = p.split("/")
        pararent = "/".join(split_p[:-1])
        if pararent=="":
            pararent="/"
        
        if len(split_p):
            if split_p[1] in ("camera", "move_group", "crane_x7", 
            "robot_description_planning", "robot_description_semantic",
            "robot_description_kinematics", "roslaunch"):
                continue
        
        param_dict[pararent].append( p )
        print("  ", pararent, p )

    # param name selection gui
    frame = tk.Frame(root)
    frame.pack()

    tk.Label(frame, text="namespce:" ).pack(side="left")

    text_ns.set( list(param_dict.keys())[0] )
    opt = tk.OptionMenu(frame, text_ns, *param_dict.keys() )
    opt.config(width=50 )
    opt.pack(side="left")

    tk.Button( frame, text='refresh', command=button_refresh).pack(side="left")

    frame_param.pack()

    root.mainloop()
        
if __name__ == "__main__":
    main()