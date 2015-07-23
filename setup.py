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
    'compressed': 1,
        'bundle_files': 1,  # 将所有东西打包到一个.exe文件
        'includes':['sip']
    }
}
setup(options=options,
      zipfile=None,  # 将.zip文件也打包进.exe文件
      windows=[{
      'script':file_dir,
      'icon_resources': [(1, "favicon.ico")]
      }],
      version = "2015.07.23",
      name = "NJU_login")  # windows参数可以隐藏运行时的cmd框
