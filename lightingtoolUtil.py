from maya import cmds

def create_light(light_type):
    transform = None
    shape = None
    
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

    parent = cmds.listRelatives(shape, parent=True, fullPath=False)
    
    if parent:
        transform = parent[0]

        transform = cmds.rename(transform, transform) 
        
        cmds.select(transform)
    
    return transform


def get_all_lights():
    shapes = cmds.ls(lights=True, long=True)
    transforms = set()

    if shapes:
        for s in shapes:
            parent = cmds.listRelatives(s, parent=True, fullPath=False)
            if parent:
                transforms.add(parent[0])

    return sorted(list(transforms))


def get_shape(transform):
    shapes = cmds.listRelatives(transform, shapes=True, fullPath=False)
    if shapes:
        return shapes[0]
    return None


def set_intensity(light, value):
    shape = get_shape(light)
    if shape and cmds.attributeQuery("intensity", node=shape, exists=True):
        cmds.setAttr(shape + ".intensity", value)


def set_color(light, rgb):
    shape = get_shape(light)
    if shape and cmds.attributeQuery("color", node=shape, exists=True):
        cmds.setAttr(shape + ".color", rgb[0], rgb[1], rgb[2], type="double3")


def set_translate(light, pos):
    if cmds.objExists(light):
        cmds.setAttr(light + ".translate", pos[0], pos[1], pos[2], type="double3")


def set_rotate(light, rot):
    if cmds.objExists(light):
        cmds.setAttr(light + ".rotate", rot[0], rot[1], rot[2], type="double3")
