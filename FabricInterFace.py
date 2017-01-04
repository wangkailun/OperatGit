from qtpy.QtGui import *
from qtpy.QtWidgets import *
import sys
import re
import time

import paramiko

class MyWidget(QMainWindow):
	def __init__(self):
		super(MyWidget , self).__init__()
		self.wget1 = QWidget()
		self.setCentralWidget(self.wget1)
		self.resize(300, 300)
		self.setWindowTitle("登录窗口")
		
		
		self.initUI()
		
	def initUI(self):
		self.username = QLabel("用户名:")
		self.passwd = QLabel("密码:")
		
		self.usernameEdit = QLineEdit()
		self.passwdEdit = QLineEdit()
		
		self.clearbutton = QPushButton("清除")
		self.linkbutton = QPushButton("确定")
		
		grid = QGridLayout()
		grid.addWidget(self.username , 0 , 1)
		grid.addWidget(self.usernameEdit , 0 , 2)
		grid.addWidget(self.passwd , 1 , 1)
		grid.addWidget(self.passwdEdit , 1 , 2)
		grid.addWidget(self.clearbutton , 2 , 2)
		grid.addWidget(self.linkbutton , 2 , 3)
		
		self.wget1.setLayout(grid)
		
		self.clearbutton.clicked.connect(self.ClearEndit)
		self.linkbutton.clicked.connect(self.ConnectGit)
		
		
	def ClearEndit(self):
		self.usernameEdit.clear()
		self.passwdEdit.clear()
		
	def ConnectGit(self):
		QToolTip.setFont(QFont("QSansSerif" , 10))
		name = self.usernameEdit.text()
		password = self.passwdEdit.text()
		if name == "" or password == "":
			if name == "":
				self.usernameEdit.setToolTip("用户名不能为空!^^")
				print(password)
				
			else:
				self.passwdEdit.setToolTip("密码不能为空！^^")
				print(name)
				
				
		else:
		
			host = Linux("123.206.191.48" , name , password)
			host.connect()
			host.send("ls -l")
			host.close()
		
		'''
			t = paramiko.Transport(("123.206.191.48",22))
			t.connect(username = name , password = password)
			
			chan = t.open_session()
			chan.settimeout(30)
			chan.get_pty()
			chan.invoke_shell()
			
			cmd = "ls -a \r"
			p = re.compile(r":~ #")
			
			result = ""
			chan.send(cmd)
			
			while True:
				time.sleep(0.5)
				ret = chan.recv(65535)
				ret = ret.decode("utf-8")
				result += ret
				if p.search(ret):
					print(result)
					break
					
					
		'''
		
class Linux(object):
	def __init__(self , ip , username , password , timeout = 30):
		self.ip = ip
		self.username = username
		self.password = password
		self.timeout = timeout
		self.t = ""
		self.chan = ""
		
		self.try_times = 3
		
		
	def connect(self):
		while True:
			try:
				self.t = paramiko.Transport(sock=(self.ip , 22))
				self.t.connect(username = self.username , password = self.password)
				self.chan = self.t.open_session()
				self.chan.settimeout(self.timeout)
				self.chan.get_pty()
				self.chan.invoke_shell()
				
				print("连接%s成功"%self.ip)
				
				return
				
			except Exception as e:
				if self.try_times != 0:
					print("连接失败，重新连接")
					self.try_times -= 1
					
				else:
					print("重试三次失败，结束程序!")
					exit(1)
					
					
	def close(self):
		self.chan.close()
		self.t.close()
		
		
	def send(self , cmd):
		cmd += "\r"
		
		p = re.complie(r":~ #")
		
		result = ""
		self.chan.send(cmd)
		while True:
			time.sleep(0.5)
			ret = self.chan.recv(65535)
			ret = ret.decode("utf-8")
			result += ret
			if p.search(ret):
				print(result)
				
				return result
				
					
			
	
			
			
			
				
				
		
			
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyWidget()
	window.show()
	sys.exit(app.exec_())

