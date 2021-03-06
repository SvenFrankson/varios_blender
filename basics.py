import bpy
import bmesh

# version v01 tested in blender 2.77
# for import this library in blender put this file in:
# blender-version/version/scripts/modules/zlibs
# from zlibs.basics import *

'''
2016 Jorge Hernandez - Melendez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

bpy.app.debug = True

def getObjectSelected():
    if len(bpy.context.selected_objects) > 0:
        ob = bpy.context.object
        return ob
    else:
        print("Error, no any selected object.")

def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')

def selectAll():
    bpy.ops.object.select_all(action='SELECT')

def selectByName(name):
    scn = bpy.context.scene
    bpy.data.objects[name].select = True
    scn.objects.active = bpy.data.objects[name]

def deselectByName(name):
    scn = bpy.context.scene
    bpy.data.objects[name].select = False

def enterEditMode():
    if bpy.context.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

def exitEditMode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

def deselectAllInEditMode(ob):
    if ob.mode != 'EDIT':
        enterEditMode()
    bpy.ops.mesh.select_all(action='DESELECT')

def selectAllInEditMode(ob):
    if ob.mode != 'EDIT':
        enterEditMode()
    deselectAllInEditMode(ob)
    bpy.ops.mesh.select_all(action='SELECT')

def whatVertexIsSelected(ob):
    current_mode = ob.mode
    if ob.mode != 'EDIT':
        enterEditMode()
    bm = bmesh.from_edit_mesh(ob.data)
    for v in bm.verts:
        if v.select:
            print("The vertex " + str(v.index) + " are selected.")
    # restore mode:
    bpy.ops.object.mode_set(mode=current_mode)

def selectOnlyThisVertex(ob,v):
    current_mode = ob.mode
    me = ob.data
    enterEditMode()
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()
    if v <= len(bm.verts)-1:
        for vert in bm.verts:
            if vert.index == v:
                vert.select = True
            else:
                vert.select = False
    else:
        print("Index incorrect")
    bmesh.update_edit_mesh(me)
    # restore mode:
    bpy.ops.object.mode_set(mode=current_mode)

def deleteVertex(ob,v):
    current_mode = ob.mode
    me = ob.data
    enterEditMode()
    bm = bmesh.from_edit_mesh(me) # <- inside editmesh
    bm.verts.ensure_lookup_table() # <- inside editmesh
    bm.verts.remove(bm.verts[v]) # <- inside editmesh
    bmesh.update_edit_mesh(me) # <- inside editmesh
    # restore mode:
    bpy.ops.object.mode_set(mode=current_mode)

def deleteVertexsSelected(ob):
    current_mode = ob.mode
    me = ob.data
    enterEditMode()
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()
    for vert in bm.verts:
        if vert.select:
            deleteVertex(ob,vert.index)
            bmesh.update_edit_mesh(me)
    # restore mode:
    bpy.ops.object.mode_set(mode=current_mode)

def hide(ob):
    ob.hide = True

def unhide(ob):
    ob.hide = False

def viewOnlyThisNumberLayer(number):
    if number > 19 or number < 0:
        print("Index layer incorrect.")
    else:
        current_layer = bpy.context.scene.active_layer
        for scn in bpy.data.scenes:
            layers = scn.layers
            # first disable all layer
            for i in range(len(layers)):
                layers[i] = False
            # after active layer
            for i in range(len(layers)):
                if i == number:
                    layers[i] = True
            # disable first current layer:
            layers[current_layer] = False

def activeObjectLayerOnlyThisNumber(layer):
    for l in range(len(bpy.context.scene.layers)):
        if l ==  layer:
            bpy.context.scene.layers[1] = True
        else:
            bpy.context.scene.layers[1] = False

# remove all objects in the current scene:
def removeAllObjectsInScene():
    # blender 2.75a have 20 layers
    for i in range(20):
        activeObjectLayerOnlyThisNumber(i)
        exitEditMode()
        deselectAll()
        for ob in bpy.data.objects:
            unhide(ob)
        selectAll()
        bpy.ops.object.delete(use_global=False)
    # return to 0 initial layer standar in blender:
    activeObjectLayerOnlyThisNumber(0)

def createMeshes(name, vertex=[], edges=[], faces=[], tipo='none'):
    mesh = bpy.data.meshes.new(name+'_Mesh')
    ob = bpy.data.objects.new(name, mesh)
    ob.show_name = True
    ob.data.show_extra_indices = True
    # si se hacen edges no se especifican facer
    # y si se hace faces no se especifican edges:
    mesh.from_pydata(vertex, edges, faces)
    # Update mesh with new data
    mesh.update()
    ob.data = mesh
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    if tipo == 'convex':
        deselectAll()
        selectByName(ob.name)
        enterEditMode()
        bpy.ops.mesh.convex_hull()
        exitEditMode()
    return ob
