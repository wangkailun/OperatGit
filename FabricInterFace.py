from qtpy.QtGui import *
from qtpy.QtWidgets import *
import sys
import re
import time
import os

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
		self.gitaddress = QLabel("git地址:")
		
		self.dir1 = sys.argv[0]
		self.dir1 = os.path.dirname(self.dir1)
		self.dir1 = self.dir1 + r"\password.txt"


		f = open(self.dir1 , "r")
		git = f.readline()
		username = f.readline()
		password = f.readline()
		f.close()
		
		
		self.usernameEdit = QLineEdit()
		self.passwdEdit = QLineEdit()
		self.gitaddressEdit = QLineEdit()

		self.gitaddressEdit.setText(git)
		self.usernameEdit.setText(username)
		self.passwdEdit.setText(password)
		
		self.clearbutton = QPushButton("清除")
		self.linkbutton = QPushButton("确定")
		
		self.readpassword = QCheckBox("记住密码")
		
		grid = QGridLayout()
		grid.addWidget(self.gitaddress , 0 , 1)
		grid.addWidget(self.gitaddressEdit , 0 , 2)
		grid.addWidget(self.username , 1 , 1)
		grid.addWidget(self.usernameEdit , 1 , 2)
		grid.addWidget(self.passwd , 2 , 1)
		grid.addWidget(self.passwdEdit , 2 , 2)
		grid.addWidget(self.readpassword , 3 , 1)
		grid.addWidget(self.clearbutton , 4 , 2)
		grid.addWidget(self.linkbutton , 4 , 3)
		
		self.wget1.setLayout(grid)
		
		self.clearbutton.clicked.connect(self.ClearEndit)
		self.linkbutton.clicked.connect(self.ConnectGit)
		
		self.readpassword.toggle()


		
		
	def ClearEndit(self):
		self.gitaddressEdit.clear()
		self.usernameEdit.clear()
		self.passwdEdit.clear()
		
	def ConnectGit(self):
		git = self.gitaddressEdit.text()
		name = self.usernameEdit.text()
		password = self.passwdEdit.text()
		if name == "" or password == "" or git == "":
			if name == "":
				print("用户名不能为空")
				
			elif password == '':
				print("密码不能为空")

			else:
				print("git地址不能为空")

				
				
		else:
			self.readpassword.stateChanged.connect(self.RememberPassword)
		
			host = Linux("120.26.103.174" , name , password)
			host.connect()
			host.send()
			host.close()



	def RememberPassword(self , state):
		if state == Qt.Checked:
			self.ClearEndit()
		else:
			dir1 = sys.argv[0]
			dir1 = os.path.dirname(dir1)
			dir1 = dir1 + r"\password.txt"
			f = open(dir1 , "w")
			f.writelines([self.gitaddressEdit.text()+"\n",self.usernameEdit.text()+"\n" , self.passwdEdit.text()+"\n"])
			f.close()

		
		
class Linux(object):
	def __init__(self , ip , username , password , timeout = 50):
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
				
				print(u"连接%s成功"%self.ip)
				print(self.chan.recv(65535).decode("utf-8"))
				
				return
				
			except Exception as e:
				if self.try_times != 0:
					print(u"连接失败，重新连接")
					self.try_times -= 1
					
				else:
					print(u"重试三次失败，结束程序!")
					exit(1)
					
					
	def close(self):
		self.chan.close()
		self.t.close()
		
		
	def send(self):
		cmd1 = "cd /tmp\r"
		cmd2 = "ls \r"
		cmd3 = "git clone /home/git/family.git\r"
		cmd4 = "cd family\r"
		cmd5 = "git pull origin master\r"
		cmd6 =  "cd homepage/test\r"
		cmd7 = "sudo rm -rf example.tar\r"
		cmd8 = "tar -cvf example.tar *\r"
		cmd9 = "cd /usr/lunlun/tmp\r"
		cmd10 = "sudo rm -rf *\r"
		cmd11 = "sudo tar -xvf /tmp/family/homepage/test/example.tar\r"
		
		cmd12 = self.password + "\r"
		
		self.chan.send(cmd1)
		time.sleep(0.5)
		print(self.chan.recv(65535).decode("utf-8"))
		
		
		self.chan.send(cmd2)
		time.sleep(0.5)
		result = self.chan.recv(65535).decode("utf-8")
		
		a = re.findall(r"family" , result)
		
		if a == '':
			self.chan.send(cmd3)
			time.sleep(20)
			print(self.chan.recv(65535).decode("utf-8"))
			
			self.chan.send(cmd4)
			time.sleep(3)
			print(self.chan.recv(65535).decode("utf-8"))
			
		else:
			self.chan.send(cmd4)
			time.sleep(3)
			print(self.chan.recv(65535).decode("utf-8"))
			
		
		
		self.chan.send(cmd5)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))
		
		self.chan.send(cmd6)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))
		
		self.chan.send(cmd7)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))
		
		
		self.chan.send(cmd12)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))
		
		
		
		self.chan.send(cmd8)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))
		
		self.chan.send(cmd9)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))
		
		self.chan.send(cmd10)
		time.sleep(5)
		print(self.chan.recv(65535).decode("utf-8"))
		
		self.chan.send(cmd11)
		time.sleep(3)
		print(self.chan.recv(65535).decode("utf-8"))



		print("更新完成！")


		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyWidget()
	window.show()
	sys.exit(app.exec_())

