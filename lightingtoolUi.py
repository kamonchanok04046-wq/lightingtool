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

		self.setWindowTitle("Lighting Tool")
		self.resize(600, 300)

		self.setStyleSheet('''
			QDialog {
				font-family: Papyrus;
				background-color: #FFC7A7;
				color: black;
			}
			QPushButton {
				background-color: #FFB8DC;
				border-radius: 8px;
				font-size: 12px;
				font-weight: bold;
				padding: 4px;
				color: black;
			}
			QPushButton:hover {
				background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 beige, stop:1 #FDAAAA);
			}
			QPushButton:pressed {
				background-color: black;
				color: white;
			}
			QLabel {
				font-weight: bold;
				font-size: 12px;
				color: black;
			}
			QDoubleSpinBox, QListWidget {
				color: black;
				background-color: #FFE3D0;
				border: 1px solid gray;
			}
		''')


		# ---------------------- MAIN LAYOUT ----------------------
		mainLayout = QtWidgets.QVBoxLayout(self)

		# ====== CREATE BUTTONS ROW ======
		self.buttonLayout = QtWidgets.QHBoxLayout()
		mainLayout.addLayout(self.buttonLayout)

		self.createAreaBtn = QtWidgets.QPushButton("Create Arealight")
		self.createSkyBtn = QtWidgets.QPushButton("Create Skydomelight")
		self.createPhotoBtn = QtWidgets.QPushButton("Create Photometriclight")
		self.createPointBtn = QtWidgets.QPushButton("Create Pointlight")
		self.createSpotBtn = QtWidgets.QPushButton("Create Spotlight")
		self.createDirBtn = QtWidgets.QPushButton("Create Directionlight")

		self.buttonLayout.addWidget(self.createAreaBtn)
		self.buttonLayout.addWidget(self.createSkyBtn)
		self.buttonLayout.addWidget(self.createPhotoBtn)
		self.buttonLayout.addWidget(self.createPointBtn)
		self.buttonLayout.addWidget(self.createSpotBtn)
		self.buttonLayout.addWidget(self.createDirBtn)

		mainLayout.addStretch()

		# ====== BODY: LIGHTS (LEFT) + PROPERTIES (RIGHT) ======
		bodyLayout = QtWidgets.QHBoxLayout()
		mainLayout.addLayout(bodyLayout)

		self.lightsPanel = self.createLightsPanel()
		bodyLayout.addWidget(self.lightsPanel, 1)

		self.propertiesPanel = self.createPropertiesPanel()
		bodyLayout.addWidget(self.propertiesPanel, 1)

		# ====== BOTTOM BUTTONS ======
		bottomLayout = QtWidgets.QHBoxLayout()
		mainLayout.addLayout(bottomLayout)

		self.refreshBtn = QtWidgets.QPushButton("REFRESH")
		self.selectBtn = QtWidgets.QPushButton("SELECT")
		self.deleteBtn = QtWidgets.QPushButton("DELETE")
		bottomLayout.addWidget(self.refreshBtn)
		bottomLayout.addWidget(self.selectBtn)
		bottomLayout.addWidget(self.deleteBtn)

		mainLayout.addStretch()

	def createLightsPanel(self):
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QVBoxLayout(widget)

		label = QtWidgets.QLabel("LIGHTS")
		layout.addWidget(label)

		self.lightsList = QtWidgets.QListWidget()
		self.lightsList.addItem("spotLight1")  
		layout.addWidget(self.lightsList)

		return widget

	def createPropertiesPanel(self):
		widget = QtWidgets.QWidget()
		layout = QtWidgets.QVBoxLayout(widget)

		label = QtWidgets.QLabel("PROPERTIES")
		layout.addWidget(label)

		intensityLayout = QtWidgets.QHBoxLayout()
		layout.addLayout(intensityLayout)
		intensityLayout.addWidget(QtWidgets.QLabel("INTENSITY"))
		self.intensitySpin = QtWidgets.QDoubleSpinBox()
		self.intensitySpin.setRange(0, 100)
		self.intensitySpin.setValue(5.0)
		intensityLayout.addWidget(self.intensitySpin)

		layout.addWidget(QtWidgets.QLabel("COLOR"))
		self.colorBtn = QtWidgets.QPushButton()
		self.colorBtn.setFixedSize(60, 20)
		self.colorBtn.setStyleSheet("background-color: #F5D5C5; border: 1px solid gray;")
		layout.addWidget(self.colorBtn)

		layout.addWidget(QtWidgets.QLabel("TRANSLATE"))
		translateLayout = QtWidgets.QHBoxLayout()
		layout.addLayout(translateLayout)
		self.tx = QtWidgets.QDoubleSpinBox()
		self.ty = QtWidgets.QDoubleSpinBox()
		self.tz = QtWidgets.QDoubleSpinBox()
		for s, v in zip([self.tx, self.ty, self.tz], [3, 5, 0]):
			s.setRange(-999, 999)
			s.setValue(v)
			translateLayout.addWidget(s)

		layout.addStretch()
		return widget

def run():
	global ui
	try:
		ui.close()
		ui.deleteLater()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = LightingToolDialog(parent=ptr)
	ui.show()


