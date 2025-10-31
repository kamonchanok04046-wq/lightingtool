# lightingtoolUi.py - FINAL: ใช้ QTimer, เพิ่ม Translate/Rotate, เปลี่ยนปุ่มเป็น RESET

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from maya import cmds
import os, sys

# ----------- Auto add local path -----------
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

# ----------- Import utility functions -----------
import lightingtoolUtil as util 


class LightingToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lighting Tool")
        self.resize(620, 380)

        # ---------------------- STYLESHEET ----------------------
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
            QListWidget::item {
                color: #CDAA00;
                font-weight: bold;
                padding: 3px;
            }
            QListWidget::item:selected {
                background-color: #FFD700;
                color: black;
            }
        ''')

        # ---------------------- MAIN LAYOUT ----------------------
        main_layout = QtWidgets.QVBoxLayout(self)

        # ---------- CREATE BUTTONS ----------
        button_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.createAreaBtn = QtWidgets.QPushButton("Create Arealight")
        self.createPointBtn = QtWidgets.QPushButton("Create Pointlight")
        self.createSpotBtn = QtWidgets.QPushButton("Create Spotlight")
        self.createDirBtn = QtWidgets.QPushButton("Create Directionlight")

        # เพิ่มเฉพาะปุ่ม Light พื้นฐาน
        for btn in [self.createAreaBtn, self.createPointBtn, self.createSpotBtn, self.createDirBtn]:
            button_layout.addWidget(btn)

        # ---------- BODY ----------
        body_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(body_layout)

        # LEFT PANEL
        left_layout = QtWidgets.QVBoxLayout()
        self.light_list = QtWidgets.QListWidget()
        left_layout.addWidget(QtWidgets.QLabel("LIGHTS"))
        left_layout.addWidget(self.light_list)

        # bottom buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.resetBtn = QtWidgets.QPushButton("RESET") # <--- เปลี่ยนจาก Refresh เป็น Reset
        self.selectBtn = QtWidgets.QPushButton("SELECT")
        self.deleteBtn = QtWidgets.QPushButton("DELETE")
        btn_layout.addWidget(self.resetBtn)
        btn_layout.addWidget(self.selectBtn)
        btn_layout.addWidget(self.deleteBtn)
        left_layout.addLayout(btn_layout)

        # RIGHT PANEL (Properties)
        self.right_panel = QtWidgets.QWidget()
        right_main_layout = QtWidgets.QVBoxLayout(self.right_panel)

        self.light_name_label = QtWidgets.QLabel("Select a Light")
        self.light_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.light_name_label.setStyleSheet("font-size: 14px; background-color: #FFE3D0; padding: 5px;")
        right_main_layout.addWidget(self.light_name_label)

        properties_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QFormLayout(properties_widget)

        self.intensity_box = QtWidgets.QDoubleSpinBox()
        self.intensity_box.setRange(0.0, 10000.0)
        self.intensity_box.setValue(5.0)

        self.color_btn = QtWidgets.QPushButton()
        self.color_btn.setFixedSize(60, 20)
        self.color_btn.setStyleSheet("background-color: #F5D5C5; border: 1px solid gray;")
        self.color_btn.clicked.connect(self.pick_color)

        # Translate Inputs
        translate_layout = QtWidgets.QHBoxLayout()
        self.tx = QtWidgets.QDoubleSpinBox()
        self.ty = QtWidgets.QDoubleSpinBox()
        self.tz = QtWidgets.QDoubleSpinBox()
        for spin in [self.tx, self.ty, self.tz]:
            spin.setRange(-9999, 9999)
            spin.setDecimals(3)
            translate_layout.addWidget(spin)
            
        # Rotation Inputs
        rotate_layout = QtWidgets.QHBoxLayout()
        self.rx = QtWidgets.QDoubleSpinBox()
        self.ry = QtWidgets.QDoubleSpinBox()
        self.rz = QtWidgets.QDoubleSpinBox()
        for spin in [self.rx, self.ry, self.rz]:
            spin.setRange(-360.0, 360.0) 
            spin.setDecimals(3)
            rotate_layout.addWidget(spin)

        right_layout.addRow("INTENSITY", self.intensity_box)
        right_layout.addRow("COLOR", self.color_btn)
        right_layout.addRow("TRANSLATE", translate_layout)
        right_layout.addRow("ROTATE", rotate_layout) # <-- เพิ่มแถว Rotation

        self.applyBtn = QtWidgets.QPushButton("APPLY")
        right_layout.addRow("", self.applyBtn)

        right_main_layout.addWidget(properties_widget)
        right_main_layout.addStretch()
        self.right_panel.setVisible(False)

        body_layout.addLayout(left_layout, 1)
        body_layout.addWidget(self.right_panel, 1)

        # ---------- Connections ----------
        self.resetBtn.clicked.connect(self.reset_light) # <--- เชื่อมต่อปุ่ม Reset
        self.light_list.itemSelectionChanged.connect(self.show_light_properties)
        self.selectBtn.clicked.connect(self.select_light)
        self.deleteBtn.clicked.connect(self.delete_light)
        self.applyBtn.clicked.connect(self.apply_changes)

        # CREATE LIGHT BUTTONS
        self.createAreaBtn.clicked.connect(lambda: self.create_and_refresh("area"))
        self.createPointBtn.clicked.connect(lambda: self.create_and_refresh("point"))
        self.createSpotBtn.clicked.connect(lambda: self.create_and_refresh("spot"))
        self.createDirBtn.clicked.connect(lambda: self.create_and_refresh("directional"))

        # Initial refresh
        self.refresh_lights()

        # 🔁 เริ่มระบบ auto-refresh ทุก 0.5 วินาที
        self._setup_timer_refresh()


    # ---------- Auto Refresh System ----------
    def _setup_timer_refresh(self):
        """ตั้ง timer ให้ refresh อัตโนมัติ"""
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._poll_scene_changes)
        self._timer.start(500)  # ทุก 0.5 วินาที

    def _poll_scene_changes(self):
        """ตรวจสอบว่า scene มีการเพิ่ม/ลบ light หรือไม่ (นี่คือฟังก์ชัน Refresh ของเดิม)"""
        current = [self.light_list.item(i).text() for i in range(self.light_list.count())]
        scene = util.get_all_lights()
        if sorted(current) != sorted(scene):
            self.refresh_lights()

    # ---------- Main Functionalities ----------
    def create_and_refresh(self, light_type):
        light = util.create_light(light_type)
        if light:
            self.refresh_lights()
            cmds.select(light)

    def refresh_lights(self):
        self.light_list.clear()
        for l in util.get_all_lights():
            item = QtWidgets.QListWidgetItem(l)
            item.setForeground(QtGui.QBrush(QtGui.QColor("#CDAA00")))
            self.light_list.addItem(item)

    def show_light_properties(self):
        items = self.light_list.selectedItems()
        if not items:
            self.right_panel.setVisible(False)
            self.light_name_label.setText("Select a Light")
            return

        self.right_panel.setVisible(True)
        light = items[0].text()
        self.light_name_label.setText(light)

        if cmds.objExists(light):
            light_shape = util.get_shape(light)

            # Intensity
            if light_shape and cmds.attributeQuery("intensity", node=light_shape, exists=True):
                self.intensity_box.setValue(cmds.getAttr(light_shape + ".intensity"))
            else:
                self.intensity_box.setValue(0.0)

            # Color
            if light_shape and cmds.attributeQuery("color", node=light_shape, exists=True):
                color = cmds.getAttr(light_shape + ".color")[0]
                self.color_btn.setStyleSheet(
                    f"background-color: rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)});"
                )
            else:
                self.color_btn.setStyleSheet("background-color: #F5D5C5; border: 1px solid gray;")

            # Translate
            if cmds.objExists(light + ".translate"):
                pos = cmds.getAttr(light + ".translate")[0]
                self.tx.setValue(pos[0])
                self.ty.setValue(pos[1])
                self.tz.setValue(pos[2])
            else:
                self.tx.setValue(0.0)
                self.ty.setValue(0.0)
                self.tz.setValue(0.0)
                
            # Rotate
            if cmds.objExists(light + ".rotate"):
                rot = cmds.getAttr(light + ".rotate")[0]
                self.rx.setValue(rot[0])
                self.ry.setValue(rot[1])
                self.rz.setValue(rot[2])
            else:
                self.rx.setValue(0.0)
                self.ry.setValue(0.0)
                self.rz.setValue(0.0)

    def select_light(self):
        items = self.light_list.selectedItems()
        if items:
            cmds.select(items[0].text())

    def delete_light(self):
        items = self.light_list.selectedItems()
        if items:
            cmds.delete(items[0].text())
            self.refresh_lights()
            self.right_panel.setVisible(False)

    def reset_light(self):
        """***ฟังก์ชันใหม่: ตั้งค่า Light ที่เลือกกลับไปเป็นค่าเริ่มต้น***"""
        items = self.light_list.selectedItems()
        if not items:
            print("Please select a light to reset.")
            return

        light = items[0].text()
        
        # 1. Reset Intensity (ค่าเริ่มต้นของ Maya Light มักเป็น 1.0)
        util.set_intensity(light, 1.0) 

        # 2. Reset Color (สีขาว)
        util.set_color(light, (1.0, 1.0, 1.0))

        # 3. Reset Translate
        util.set_translate(light, (0.0, 0.0, 0.0))

        # 4. Reset Rotate
        util.set_rotate(light, (0.0, 0.0, 0.0))
        
        # 5. อัปเดต UI ให้แสดงค่าที่ถูก Reset
        self.show_light_properties()
        
        print(f"Reset {light} to default values.")

    def pick_color(self):
        current_color = self.color_btn.palette().button().color()
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.color_btn.setStyleSheet(
                f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});"
            )

    def apply_changes(self):
        items = self.light_list.selectedItems()
        if not items:
            return
        light = items[0].text()
        light_shape = util.get_shape(light) 
        
        if not light_shape:
            return

        # Apply Intensity
        util.set_intensity(light, self.intensity_box.value())

        # Apply Color
        color = self.color_btn.palette().button().color()
        util.set_color(light, (color.redF(), color.greenF(), color.blueF()))

        # Apply Translate
        tx_val = self.tx.value()
        ty_val = self.ty.value()
        tz_val = self.tz.value()
        util.set_translate(light, (tx_val, ty_val, tz_val))
        
        # Apply Rotate
        rx_val = self.rx.value()
        ry_val = self.ry.value()
        rz_val = self.rz.value()
        util.set_rotate(light, (rx_val, ry_val, rz_val))
        
        cmds.select(light)
        print(f"Updated {light}: T=({tx_val}, {ty_val}, {tz_val}), R=({rx_val}, {ry_val}, {rz_val})")


def run():
    global ui
    # บังคับ Reload util เพื่อให้แน่ใจว่าได้ฟังก์ชันใหม่ทั้งหมด
    try:
        import importlib
        import lightingtoolUtil as util
        importlib.reload(util)
    except Exception as e:
        print(f"Warning: Could not reload lightingtoolUtil: {e}")

    try:
        # หยุด QTimer และปิด UI เก่า
        if 'ui' in globals() and ui is not None:
             if hasattr(ui, '_timer') and ui._timer.isActive():
                 ui._timer.stop()
        ui.close()
        ui.deleteLater()
    except:
        pass

    # รัน UI ใหม่
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = LightingToolDialog(parent=ptr)
    ui.show()