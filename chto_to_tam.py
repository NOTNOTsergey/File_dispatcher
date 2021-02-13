import os
import chto_to_tam_design as design
from copy import deepcopy
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui

def write_log(exc):
	f = open(os.getcwd() + '/logs.txt', 'w')
	f.write(str(exc))
	f.close()

def file_search(cwd):
		try:
			results = [str(i)[ str(i).index("'")  + 1 : -2 ] for i in os.scandir(cwd)]
		except:
			print("it's an error")
			return []

		files = [ [], [] ]

		for i in results:
			if os.path.isfile(cwd) == False and cwd.endswith("/") == False:
				if os.path.isdir(cwd + "/" + i):
					files[0].append(i)
				else:
					files[1].append(i)
			else:
				if os.path.isdir(cwd + "/" + i):
					files[0].append(i)
				else:
					files[1].append(i)
		return files


array = ['hide_dirs', 'hide_files']

class ExampleApp(QtWidgets.QDialog, design.Ui_Dialog):

	def __init__(self):
		super().__init__()

		# self.set_script("")


		self.setupUi(self)

		self.listWidget.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.scripts_listWidget.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.LineEdit.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.scripts_LineEdit.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))
		self.finder_LineEdit.setFont(QtGui.QFont("Fira Code Light", 11, QtGui.QFont.Bold))

		self.LineEdit.returnPressed.connect(self.set_items)

		self.scripts_LineEdit.returnPressed.connect(self.set_scripts_items)

		self.finder_LineEdit.returnPressed.connect(self.set_scripts_items)

		self.listWidget.itemDoubleClicked.connect(self.new_search)

		self.listWidget.itemClicked.connect(self.selectionChanged)

		self.scripts_listWidget.itemDoubleClicked.connect(self.start_program_on_python)

	def new_search(self, item):
		dir_now = self.LineEdit.text() + item.text()
		if os.path.isdir(dir_now) and not dir_now.endswith('/'):
			dir_now += '/'
			self.LineEdit.setText(self.LineEdit.text() + '/')
		if os.path.isdir(dir_now):
			self.listWidget.clear()
			os.system('cd ' + dir_now)
			result = file_search(dir_now)
			self.LineEdit.setText(dir_now)
			self.listWidget.clear()
			self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
			if len(result[0]) != 0:
				if len(result[0]) >= 16:
					self.listWidget.addItems(result[0][ : 15] + ['d---->'])
					array[0] = 'hide_dirs'
				else:
					self.listWidget.addItems(result[0])
					array[0] = 'full_dirs'
			else:
				self.listWidget.addItem('в этой папке нет вложенных папок')
			self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
			if len(result[1]) != 0:
				if len(result[1]) >= 16:
					self.listWidget.addItems(result[1][ : 15] + ['f---->'])
					array[0] = 'hide_files'
				else:
					self.listWidget.addItems(result[1])
					array[1] = 'full_dirs'
			else:
				self.listWidget.addItem('нет файлов в этой папке')
		#____________________________________________________only for Linux
		elif os.path.isfile(dir_now) and (dir_now.endswith('.jpg') or dir_now.endswith('.ico') or dir_now.endswith('.png')):
			os.system('gwenview ' +  dir_now)
		#____________________________________________________
		elif os.path.isfile(dir_now) and (dir_now.endswith('.json') or dir_now.endswith('.py')):
			os.system('code ' + dir_now)
		

	def start_program_on_python(self, item):
		if os.path.isfile(self.scripts_LineEdit.text() + item.text()) and item.text().endswith('.py'):
			os.system("python -u " + '"' + self.scripts_LineEdit.text() + item.text() + '"')
			return None	

	def selectionChanged(self, item):
		text = deepcopy(item.text())
		if item.text() == 'd---->':
			self.set_items(arg='full_dirs', arg2=array[1])
		elif item.text() == 'f---->':
			self.set_items(arg=array[0], arg2='full_files')
		elif item.text() == '    delete':
			if os.path.isdir(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text()):
				os.rmdir(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text())
			elif os.path.isfile(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text()):
				os.remove(self.LineEdit.text() + self.listWidget.item(self.listWidget.currentRow() - 1).text())
			self.set_items()
		# elif item.text() == '    rename':


		else:
			if os.path.isdir(self.LineEdit.text() + item.text()):

				result = file_search(self.LineEdit.text())
				self.listWidget.clear()
				




				self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
				if len(result[0]) != 0:
					self.listWidget.addItems(result[0][ : result[0].index(text) + 1] + ['    delete', '    rename'] + result[0][result[0].index(text) + 1: ])
				else:
					self.listWidget.addItem('в этой папке нет вложенных папок')
				self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
				if len(result[1]) != 0:
					if len(result[1]) >= 16:
						self.listWidget.addItems(result[1][ : 15] + ['f---->'])
					else:
						self.listWidget.addItems(result[1])
				else:
					self.listWidget.addItem('нет файлов в этой папке')





			elif os.path.isfile(self.LineEdit.text() + text):
				result = file_search(self.LineEdit.text())
				self.listWidget.clear()


				self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
				if len(result[0]) != 0:
					if len(result[0]) >= 16:
						self.listWidget.addItems(result[0][ : 15] + ['d---->'])
					else:
						self.listWidget.addItems(result[0])
				else:
					self.listWidget.addItem('в этой папке нет вложенных папок')
				self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
				if len(result[1]) != 0:
					self.listWidget.addItems(result[1][ : result[1].index(text) + 1] + ['    delete', '    rename'] + result[1][result[1].index(text) + 1: ])
				else:
					self.listWidget.addItem('нет файлов в этой папке')







	def set_items(self, arg='hide_dirs', arg2='hide_files'):
		if self.LineEdit.text() != "":
			if self.LineEdit.text().startswith("|>"):
				try:
					exec(self.LineEdit.text()[3 : ])
				except Exception as e:
					print(e)
				self.LineEdit.setText("|> ")
			elif self.LineEdit.text().startswith("||>"):
				try:
					os.system(self.LineEdit.text()[4 : ])
				except Exception as e:
					print(e)
				self.LineEdit.setText("||> ")
			else:
				result = file_search(self.LineEdit.text())
				self.listWidget.clear()
				try:
					self.listWidget.clear()
					self.listWidget.addItem(f'|>	{len(result[0])}				папок---------------------------------------------------------------------------------')
					if len(result[0]) != 0:
						if len(result[0]) >= 16 and arg == 'hide_dirs':
							self.listWidget.addItems(result[0][ : 15] + ['d---->'])
							array[0] = 'hide_dirs'
						else:
							self.listWidget.addItems(result[0])
							array[0] = 'full_dirs'
					else:
						self.listWidget.addItem('в этой папке нет вложенных папок')
					self.listWidget.addItem(f'|>	{len(result[1])}				файлов--------------------------------------------------------------------------------')
					if len(result[1]) != 0:
						if len(result[1]) >= 16 and arg2 == 'hide_files':
							self.listWidget.addItems(result[1][ : 15] + ['f---->'])
							array[0] = 'hide_files'
						else:
							self.listWidget.addItems(result[1])
							array[1] = 'full_dirs'
					else:
						self.listWidget.addItem('нет файлов в этой папке')
					return
				except Exception as e:
					print(e)

	def set_scripts_items(self):
		try:
			if os.path.isfile(self.scripts_LineEdit.text()) and self.scripts_LineEdit.text().endswith('.py'):
				os.system("python -u " + '"' + self.scripts_LineEdit.text() + '"')
				return None	
			result = file_search(self.scripts_LineEdit.text())

			fiile = []

			for files in result[1]:
				if files.endswith(self.finder_LineEdit.text()):
					fiile.append(files)
			
			if len(fiile) == 0:
				self.scripts_listWidget.clear()
				self.scripts_listWidget.addItem(f'файлов с расширением {self.finder_LineEdit.text()} в данной папке нет')
				self.scripts_listWidget.addItem('какая жалость, поищите в другой папке')
			else:
				self.scripts_listWidget.clear()
				self.scripts_listWidget.addItems(fiile)
		except Exception as e:
			print(e)			




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = ExampleApp()
	window.show()
	app.exec_()