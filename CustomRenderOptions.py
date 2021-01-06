bl_info = {
    "name": "Render TO Specific Directory",
    "blender": (2, 80, 0),
    "category": "Render",
}



import bpy, os, sys, ntpath
import os.path
from os import path
from os.path import expanduser



home = expanduser("~")
RenderOutputDir = home + "/Documents/Blender Render Outputs"


def checkIfDirectoriesExist(projectName):
    if (path.exists(RenderOutputDir) == False):
        os.mkdir(RenderOutputDir)
    
    if (path.exists(RenderOutputDir + "/" + projectName) == False):
        os.mkdir(RenderOutputDir + "/" + projectName)

def getVersion(projectName):
    location = RenderOutputDir + "/" + projectName + "/config.json"
    v = ""
    print("starting")
    if os.path.isfile(location):
        config = open(location, 'r+')
        version = config.readlines()[0]
        if (version[len(version)-1] == "9"):
            stringVersion = str(version)
            strings = []
            for i in stringVersion:
                strings.append(i)

            bigNumber = ""
            for i in range(0, len(stringVersion)-1):
                if (strings[i] != "."):
                    bigNumber += strings[i]

            numberAsInt = int(bigNumber)
            numberAsInt += 1
            numberAsString = str(numberAsInt)

            writeToFile = [numberAsString, ".", "0"]
            config.seek(0)
            config.writelines(writeToFile)
            for i in writeToFile:
                v += i
            
        else:
            stringVersion = str(version)
            strings = []
            for i in stringVersion:
                strings.append(i)
            numberAsInt = int(version[len(version)-1])
            numberAsInt = numberAsInt + 1
            numberAsString = str(numberAsInt)
            strings[len(stringVersion)-1] = numberAsString
            finalVersion = ""
            for i in strings:
                finalVersion += i
            config.seek(0)
            config.writelines(finalVersion)
            v = finalVersion
        
    else:
        config = open(location, 'w+')
        config.writelines("1.0")
        v = "1.0"

    return v


def getFileNameAndLocation():
    projectName = os.path.splitext(ntpath.basename(bpy.data.filepath))[0]
    checkIfDirectoriesExist(projectName=projectName)
    version = getVersion(projectName=projectName)
    fileName = "C:/Users/Joseph/Documents/Blender Render Outputs/" + projectName + "/" + projectName + "_v" + version + ".png"
    return fileName
    

class SimpleOperator(bpy.types.Operator):
    bl_idname = "myops.render"
    bl_label = "Render"
    

    
    
    def execute(self, context):
        bpy.data.filepath
        
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.filepath = getFileNameAndLocation()
        bpy.ops.render.render(write_still = 1)
        return {'FINISHED'}



        


class TOPBAR_MT_custom_menu(bpy.types.Menu):
    bl_label = "Custom Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("myops.render", text="render")

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_custom_menu")





def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(TOPBAR_MT_custom_menu)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_custom_menu.menu_draw)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_custom_menu.menu_draw)
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(TOPBAR_MT_custom_menu)



if __name__ == "__main__":
    register()
