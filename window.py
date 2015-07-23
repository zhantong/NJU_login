from PyQt5.QtWidgets import *
import sys
import nju_login_2
class ChangeInfo(QDialog):
    def __init__(self, parent=None):
        super(ChangeInfo, self).__init__(parent)
        usr = QLabel("用户：")
        pwd = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 3);
        gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 3);

        okBtn = QPushButton("确定")
        cancelBtn = QPushButton("取消")
        btnLayout = QHBoxLayout()

        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)

        self.setLayout(dlgLayout)
        okBtn.clicked.connect(self.ok)
        cancelBtn.clicked.connect(self.reject)
        self.setWindowTitle("登录")
        self.resize(300, 200)
        self.usrLineEdit.setText(nju.id)
        self.pwdLineEdit.setText(nju.pw)
    def ok(self):
        nju.set_id_pw(self.usrLineEdit.text(),self.pwdLineEdit.text())
        super(ChangeInfo, self).accept()
class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.browser = QPlainTextEdit()
        gridLayout = QGridLayout()
        gridLayout.addWidget(self.browser,0,0,1,2)
        self.conBtn = QPushButton("连接")
        changeinfoBtn = QPushButton("修改账号密码")
        gridLayout.addWidget(self.conBtn, 1, 0, 1, 1)
        gridLayout.addWidget(changeinfoBtn, 1, 1, 1, 1)
        cancelBtn=QPushButton("关闭程序")
        gridLayout.addWidget(cancelBtn, 2, 0,1,2)
        self.setLayout(gridLayout)
        cancelBtn.setFocus()
        cancelBtn.clicked.connect(self.accept)
        changeinfoBtn.clicked.connect(self.show_info)
        self.conBtn.clicked.connect(self.connect)
        self.browser.setReadOnly(True)
        self.conBtn.clicked.emit(True)
    def show_info(self):
        cinfo=ChangeInfo()
        cinfo.show()
        cinfo.exec_()
    def connect(self):
        if self.conBtn.text()=='连接':
            self.browser.setPlainText(nju.connect())
        else:
            self.browser.setPlainText(nju.disconnect())
        if nju.get_info()==-1:
            self.conBtn.setText('连接')
        else:
            self.conBtn.setText('断开')
if __name__=='__main__':
    nju=nju_login_2.NJU_Login()
    app = QApplication(sys.argv)
    dlg = LoginDlg()
    dlg.show()
    sys.exit(app.exec_())