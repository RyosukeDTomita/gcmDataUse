#########################################################################
# Name: fontjp.py
#
# Return japanese font path.
# if you do not have source-han-code-jp, you can download [here](https://github.com/adobe-fonts/source-han-code-jp/archive/2.000R.zip)
#
# Usage:
#        ```
#        from fontjp import fontjp
#        jp = fontjp()
#        ax.set_xlabel("test",fontproperties=jp.font
#        ```
#
#        OR
#
#        ```
#        from fontjp import fontjp
#        jp = fontjp()
#        ax.set_xlabel("test",fontproperties=jp()
#        ```
# Author: Ryosuke Tomita
# Date: 2021/5/6
##########################################################################
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import os
import platform
pf = platform.system()

class fontjp:
    def __init__(self):
        if pf == "Darwin":
            self.font_dir = '/Users/tomita/Library/Fonts'
        elif pf == "Linux":
            self.font_dir = '/home/tomita/.local/share/fonts'
        self.font_path = os.path.join(self.font_dir + '/SourceHanCodeJP-Regular.otf')
        self.font = font_manager.FontProperties(fname=self.font_path,size=14)
    def __call__(self):
        return self.font
