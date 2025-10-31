# lightingtoolUtil.py - FINAL: รองรับ Light พื้นฐาน, พร้อม set_rotate/set_translate

from maya import cmds

def create_light(light_type):
    """สร้างแสงตามชนิดที่เลือก แล้วคืนชื่อ transform"""
    transform = None
    shape = None
    
    # 1. สร้าง Shape Node ของ Light ทุกชนิด
    if light_type == "point":
        shape = cmds.shadingNode("pointLight", asLight=True, name="pointLightShape#")
    elif light_type == "spot":
        shape = cmds.shadingNode("spotLight", asLight=True, name="spotLightShape#")
    elif light_type == "directional":
        shape = cmds.shadingNode("directionalLight", asLight=True, name="directionalLightShape#")
    elif light_type == "area":
        shape = cmds.shadingNode("areaLight", asLight=True, name="areaLightShape#")
    else:
        return None

    # 2. หา Transform Node
    parent = cmds.listRelatives(shape, parent=True, fullPath=False)
    
    if parent:
        transform = parent[0]
        
        # 3. สำคัญ: ทำการ Rename ตัวเองเพื่อบังคับให้ได้ Short Name ที่ถูกต้อง (แก้ปัญหาชื่อซ้ำซ้อน)
        transform = cmds.rename(transform, transform) 
        
        cmds.select(transform)
    
    return transform


def get_all_lights():
    """คืนชื่อ transform ของไฟทั้งหมด"""
    shapes = cmds.ls(lights=True, long=True)
    transforms = set()

    if shapes:
        for s in shapes:
            # ใช้ fullPath=False เพื่อให้ได้ Short Name ของ Parent
            parent = cmds.listRelatives(s, parent=True, fullPath=False)
            if parent:
                transforms.add(parent[0])

    return sorted(list(transforms))


def get_shape(transform):
    """คืนชื่อ shape node จาก transform"""
    shapes = cmds.listRelatives(transform, shapes=True, fullPath=False)
    if shapes:
        return shapes[0]
    return None


def set_intensity(light, value):
    """ตั้งค่า Intensity"""
    shape = get_shape(light)
    if shape and cmds.attributeQuery("intensity", node=shape, exists=True):
        cmds.setAttr(shape + ".intensity", value)


def set_color(light, rgb):
    """ตั้งค่า Color"""
    shape = get_shape(light)
    if shape and cmds.attributeQuery("color", node=shape, exists=True):
        cmds.setAttr(shape + ".color", rgb[0], rgb[1], rgb[2], type="double3")


def set_translate(light, pos):
    """ตั้งค่าการเคลื่อนที่ (Translate)"""
    if cmds.objExists(light):
        cmds.setAttr(light + ".translate", pos[0], pos[1], pos[2], type="double3")


def set_rotate(light, rot):
    """ตั้งค่าการหมุน (Rotate)"""
    if cmds.objExists(light):
        cmds.setAttr(light + ".rotate", rot[0], rot[1], rot[2], type="double3")

# ฟังก์ชัน create_ai_light ถูกลบออกไปแล้ว