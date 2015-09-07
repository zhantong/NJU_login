"""将.py文件转换为.exe文件
  需要首先安装py2exe,可以直接pip install py2exe；
  实际生成为一个文件夹，里面有必要的dll；
  另外还需要复制PyQt5中的platforms文件夹，一般路径为
  Python34/Lib/site-packages/PyQt5/plugins/Platforms。
"""
from distutils.core import setup
import py2exe  # 并未直接调用，但必不可少
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
