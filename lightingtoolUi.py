try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui 


class LightingToolDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('Lighting Tool')
		self.resize(300,100)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		self.setStyleSheet(
			'''
				QDialog{
					front-family: Papyrus;
					background-color: #FFC7A7
				}

			'''

		)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.createpointButton = QtWidgets.QPushButton('CREATEPOINT')
		self.createpointButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #FFB8DC;
					border-radius: 12px;
					font-size: 12px;
					font-family: Papyrus;
					font-weight: bold;
					padding: 4px;
					color: #000000
				}
				QPushButton:hover {
					background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 beige, stop:1 #FDAAAA);
				}
				QPushButton:pressed {
					background-color: black;
				}

			'''
		)

		self.creatskydomelightButton = QtWidgets.QPushButton('Creat Skydomelight')
		self.creatskydomelightButton.setStyleSheet(
			'''
				QPushButton {
					background-color: #FFB8DC;
					border-radius: 12px;
					font-size: 16px;
					font-family: Papyrus;
					font-weight: bold;
					padding: 4px;
					color: #000000
				}
				QPushButton:hover {
					background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 beige, stop:1 #FDAAAA);
				}
				QPushButton:pressed {
					background-color: black;
				}

			'''
		)
		self.buttonLayout.addWidget(self.createpointButton)
		self.buttonLayout.addWidget(self.creatskydomelightButton)

		self.mainLayout.addStretch()


def run():
	global ui 
	try: 
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = LightingToolDialog(parent=ptr)
	ui.show()
