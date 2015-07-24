"""
使用py2exe将.py文件转换为.exe文件。
需要首先安装py2exe,可以直接pip install py2exe
"""
from distutils.core import setup
import py2exe
import sys
file_dir = 'window.py'
sys.argv.append('py2exe')  # 巧妙避免了用到cmd
options = {
    'py2exe': {
        'compressed': 1,  # 压缩
        'bundle_files': 1,  # 是否打包到一个.exe文件
        'includes': ['sip']  # PyQt打包成exe的错误修复
    }
}
setup(options=options,
      zipfile=None,  # 是否将.zip文件也打包进.exe文件
      windows=[{  # windows参数可以隐藏运行时的cmd框
          'script': file_dir,
          'icon_resources': [(1, "favicon.ico")]  # 加入图标
      }])
