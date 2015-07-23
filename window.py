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
    def accept(self):
        if self.usrLineEdit.text().strip() == "eric" and self.pwdLineEdit.text() == "eric":
            super(ChangeInfo, self).accept()
        else:
            print(self.pwdLineEdit.text())
            QMessageBox.warning(self,
                    "警告",
                    "用户名或密码错误！",
                    QMessageBox.Yes)
            self.usrLineEdit.setFocus()
class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.browser = QPlainTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        gridLayout = QGridLayout()
        self.conBtn = QPushButton("连接")
        changeinfoBtn = QPushButton("修改账号密码")
        gridLayout.addWidget(self.conBtn, 0, 0, 1, 1)
        gridLayout.addWidget(changeinfoBtn, 0, 1, 1, 1)
        layout.addLayout(gridLayout)
        self.setLayout(layout)
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

nju=nju_login_2.NJU_Login()
app = QApplication(sys.argv)
dlg = LoginDlg()
dlg.show()
dlg.exec_()
app.exit()