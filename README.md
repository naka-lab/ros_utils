# ros_utils

ROSを利用するために作ったツール類

## インストール

```
cd ~/catkin_ws/src
git clone https://github.com/naka-lab/ros_utils.git
```

## param_setting_gui

ros paramを確認・設定可能なGUI

- 実行
```
rosrun ros_utils param_setting_gui.py
```

- 確認・設定したいパラメータが属しているnamespaceをプルダウンメニューから選択して，refreshボタンを押す
- 現在のパラメータが表示されるので，各パラメータを書き換えsetボタンを押すと，パラメータが変更される
