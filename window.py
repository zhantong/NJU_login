"""PyQt实现南京大学校园网登录、登出图形界面
    需要下载并安装PyQt5（并不能通过pip安装）
"""
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import PyQt5.QtCore  # 只用在py2exe用来打包，这里并未用到
import sys
import nju_login_2


class ChangeInfo(QDialog):

    """修改账号密码界面
    """

    def __init__(self, parent=None):
        super(ChangeInfo, self).__init__(parent)
        usr = QLabel("账号：")
        pwd = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 2)
        gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 2)

        okBtn = QPushButton("确定")
        cancelBtn = QPushButton("取消")
        gridLayout.addWidget(okBtn, 2, 0, 1, 1)
        gridLayout.addWidget(cancelBtn, 2, 1, 1, 1)
        aboutBtn = QPushButton("关于作者")
        gridLayout.addWidget(aboutBtn, 2, 2, 1, 1)
        self.setLayout(gridLayout)
        okBtn.clicked.connect(self.ok)
        aboutBtn.clicked.connect(self.about)
        cancelBtn.clicked.connect(self.reject)
        self.setWindowTitle("修改账号密码")
        self.setWindowIcon(QtGui.QIcon('favicon.ico'))
        #self.resize(300, 200)
        self.usrLineEdit.setText(nju.id)  # 读取账号
        self.pwdLineEdit.setText(nju.pw)  # 读取密码

    def ok(self):
        """提交修改账号密码
        """
        nju.set_id_pw(self.usrLineEdit.text(), self.pwdLineEdit.text())
        super(ChangeInfo, self).accept()

    def about(self):
        """关于作者
        """
        QMessageBox.about(
            self, "关于作者", "如果你有任何意见或建议\n欢迎联系我：zhantong1994@163.com")


class LoginDlg(QWidget):

    """主界面
    """

    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.browser = QPlainTextEdit()
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.browser, 0, 0, 1, 2)
        self.conBtn = QPushButton("连接")
        changeinfoBtn = QPushButton("修改账号密码")
        gridLayout.addWidget(self.conBtn, 1, 0, 1, 1)
        gridLayout.addWidget(changeinfoBtn, 1, 1, 1, 1)
        cancelBtn = QPushButton("关闭程序")
        cancelBtn.setDefault(True)
        gridLayout.addWidget(cancelBtn, 2, 0, 1, 2)
        self.setLayout(gridLayout)
        self.setWindowTitle("南京大学|校园网自动登录")
        self.setWindowIcon(QtGui.QIcon('favicon.ico'))
        cancelBtn.setFocus()
        cancelBtn.clicked.connect(self.close)
        changeinfoBtn.clicked.connect(self.show_info)
        self.conBtn.clicked.connect(self.connect)
        self.browser.setReadOnly(True)
        self.conBtn.clicked.emit(True)  # 模拟点击

    def show_info(self):
        """打开修改账号密码界面
        """
        cinfo = ChangeInfo()
        cinfo.show()
        cinfo.exec_()

    def connect(self):
        """连接/断开
            连接或断开校园网，并设置按钮的text
        """
        if self.conBtn.text() == '连接':
            self.browser.setPlainText(nju.connect())
        else:
            self.browser.setPlainText(nju.disconnect())
        if nju.get_info() == -1:
            self.conBtn.setText('连接')
        else:
            self.conBtn.setText('断开')

if __name__ == '__main__':
    nju = nju_login_2.Campusnetwork()
    app = QApplication(sys.argv)
    dlg = LoginDlg()
    dlg.show()
    sys.exit(app.exec_())
