## Setup Blender
In the Blender Scene Properties set Unit Scale to `0.01` and Length Units to Centimeters. To ensure that the scene is always visible show the sidebar via the workspace `View` menu, and in `View` tab set the `End` value to something like `7500`.

These settings can be saved for convinience as defaults via `File/Defaults`.


## Add Melee Weapon bone to Skeleton

### 1 Export Mech Skeleton

Save the mech's SKM to the mod and export it to FBX. All options can be unchecked.

### 2 Import the SKM into Blender
Import the skeleton FBX in Blender via `File/Import/FBX`.

### 3 Mirror the Melee Weapon Bone
- Find the `Weapon_Melee_Left` bone in the Scene tree view. Look for the SKM, then Root/Pelvis/Torso_Twist/Torso_Animation/Torso_Pitch/Clavicle_Left/....
- Select the bone by clicking on it
- Duplicate it (Shift-D) (+ ESC to keep the position)
- Rename it to `Weapon_Melee_Right` (double-click on the name)
- Select "Bone Properties" and then "Relations"
- Change the parent bone to its right arm counterpart
- Reposition the new bone in the right hand. On most mechs this just means to invert the Y values for the transform. Sometimes manual placement needs to be done.

### 4 Export the Skeleton from Blender
- Select the first Root node and remove the parent relation
- Select the entire hierarchy
- Export to FBX (only selected, no animations, no leaf bones)

### 5 Re-Import the Skeleton into Unreal


## Mirror Melee Animations with Blender

### 1 Export the animation from Unreal
Export the animation you want to mirror via `Asset Actions/Export`. Everything can be unchecked since we only need the raw animation. I went with FBX2020 which worked fine (all options can be unchecked).

### 2 Import the Animation in Blender
Import the animation in Blender via `File/Import/FBX` and just leave it there.

### 3 Mirror the Animation
In the `Scripting` workspace load the mirroring script:
```python
import bpy
import math

def mirror_frames(fcu):
    # remember first frame value
    first = False
    for key in fcu.keyframe_points:
        #key.co[1] = -1 * key.co[1]
        if first == False:
            first = key.co[1]
        else:
            # invert difference to first
            diff = key.co[1] - first
            key.co[1] = first - diff

def clone_frame_points(p):
    x = {}
    for key in p:
        x[key.co[0]] = key.co[1]
    return x

def mirror_animation(obj_list):
    rot = {}
    
    for obj in obj_list:
        anim = obj.animation_data
        if anim is not None and anim.action is not None:
            for fcu in anim.action.fcurves:
                if "bone" in fcu.data_path:
                    # replace right/left in bone references
                    old_path = fcu.data_path
                    new_path = old_path.replace("Left","Right")
                    if old_path == new_path:
                        new_path = old_path.replace("Right","Left")
                        
                    # for all bones we want to flip, cache their rotation values
                    if old_path != new_path:
                        if fcu.data_path.endswith(('rotation_euler','rotation_quaternion')):
                            rot.setdefault(fcu.data_path, {})[fcu.array_index] = clone_frame_points(fcu.keyframe_points)
                                    
                    # for all other bones we can simply mirror the rotation
                    else:
                        if fcu.data_path.endswith(('rotation_euler','rotation_quaternion')):
                            if fcu.array_index in (1,2): # rotation values are W,X,Y,Z
                                mirror_frames(fcu)
                        
	# flip rotation values of all Left/Right bones based on the cached ones
    for obj in obj_list:
        anim = obj.animation_data
        if anim is not None and anim.action is not None:
            for fcu in anim.action.fcurves:
                if "bone" in fcu.data_path:
                    old_path = fcu.data_path
                    new_path = old_path.replace("Left","Right")
                    if old_path == new_path:
                        new_path = old_path.replace("Right","Left")

                    if fcu.data_path.endswith(('rotation_euler','rotation_quaternion')):
                        if old_path != new_path:
                            f = -1.0 if (fcu.array_index in (1,2)) else 1.0
                            for key in fcu.keyframe_points:
                                key.co[1] = f * rot[new_path][fcu.array_index][key.co[0]]
                            
        
# get all selected objects
selection = bpy.context.selected_objects

# check if selection is not empty
if selection:
    mirror_animation(selection)
else:
    print ('nothing selected')
```

Since the imported animation is already selected simply run the script. The animation is now mirrored

### 4 Export the Animation
Export the animation via `File/Export/FBX` and give it a useful name. Uncheck `Armature/Add Leaf Bones` to avoid warnings in Unreal. Essentially the leaf bones are a Blender speciality which are ignored by Unreal.

### 5 Copy the Original Animation in Unreal
In Unreal make a copy of the original animation and give it a useful name.

### 6 Import the Mirrored Animation
Import the mirrored animation via right click on the new asset and `Reimport with new file`. Select the mirrored FBX and that's it.

**Caution: the import sometimes failed for me when I tried to reuse a Blender file to mirror more than one animation or when I played with the animation in other workspaces. I solved this by creating a new file in Blender and simply running the script again.**
