bl_info = {
    "name": "Render TO Specific Directory",
    "blender": (2, 80, 0),
    "category": "Render",
}



import bpy, os, ntpath
import os.path
from os import path
from os.path import expanduser



home = expanduser("~")
RenderOutputDir = home + "/Documents/Blender Render Outputs/"
RenderAnimationDir = home + "/Documents/Blender Video Outputs/"


def checkIfDirectoriesExist(projectName):
    if (path.exists(RenderOutputDir) == False):
        os.mkdir(RenderOutputDir)
    
    if (path.exists(RenderOutputDir + projectName) == False):
        os.mkdir(RenderOutputDir + projectName)
    
    if (path.exists(RenderAnimationDir) == False):
        os.mkdir(RenderAnimationDir)
    
    if (path.exists(RenderAnimationDir + projectName) == False):
        os.mkdir(RenderAnimationDir + projectName)

def getVersion(projectName, dir):
    location = dir + projectName + "/config"
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


def getFileNameAndLocation(dir):
    projectName = os.path.splitext(ntpath.basename(bpy.data.filepath))[0]
    checkIfDirectoriesExist(projectName=projectName)
    version = getVersion(projectName=projectName, dir=dir)
    fileName = dir + projectName + "/" + projectName + "_v" + version + "." + str(bpy.context.scene.render.image_settings.file_format).lower()
    return fileName
    

class SimpleRender(bpy.types.Operator):
    bl_idname = "myops.render"
    bl_label = "Render"
    
    def execute(self, context):
        bpy.context.scene.render.image_settings.file_format = "PNG"
        bpy.context.scene.render.filepath = getFileNameAndLocation(RenderOutputDir)
        bpy.ops.render.render('INVOKE_DEFAULT',animation=False, write_still=True)
        return {'FINISHED'}

class SimpleRenderAnimation(bpy.types.Operator):
    bl_idname = "myops.renderanimation"
    bl_label = "Render Animation"
    
    def execute(self, context):
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.context.scene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"
        bpy.context.scene.render.filepath = getFileNameAndLocation(RenderAnimationDir)
        bpy.ops.render.render('INVOKE_DEFAULT',animation=True, write_still=True)
        return {'FINISHED'}

        


class TOPBAR_MT_custom_menu(bpy.types.Menu):
    bl_label = "Custom Render"

    def draw(self, context):
        layout = self.layout
        layout.operator("myops.render", text="render")
        layout.operator("myops.renderanimation", text="render Animation")

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_custom_menu")




def register():
    bpy.utils.register_class(SimpleRender)
    bpy.utils.register_class(SimpleRenderAnimation)
    bpy.utils.register_class(TOPBAR_MT_custom_menu)
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_custom_menu.menu_draw)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_custom_menu.menu_draw)
    bpy.utils.unregister_class(SimpleRender)
    bpy.utils.unregister_class(SimpleRenderAnimation)
    bpy.utils.unregister_class(TOPBAR_MT_custom_menu)



if __name__ == "__main__":
    register()
