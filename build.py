"""
使用py2exe将.py文件转换为.exe文件。
需要首先安装py2exe,可以直接pip install py2exe
"""
from distutils.core import setup
import py2exe
import sys
file_dir = 'nju_login.py'
sys.argv.append('py2exe')  # 巧妙避免了用到cmd
options = {
    'py2exe': {
        'bundle_files': 1  # 将所有东西打包到一个.exe文件
    }
}
setup(options=options,
      zipfile=None,  # 将.zip文件也打包进.exe文件
      windows=[file_dir])  # windows参数可以隐藏运行时的cmd框
