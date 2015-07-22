from distutils.core import setup
import py2exe
import sys
sys.argv.append('py2exe')
options={
	'py2exe':{
	'bundle_files':1
	}
}
setup(options=options,
	zipfile=None,
	windows=['nju_login.py'])