import bpy
import math
from mathutils import Vector
from pathlib import Path

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def create_mat(name, color, metallic=0.0, roughness=0.3, emission=(0,0,0,1), emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = emission
            bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

mat_white = create_mat("WhiteBody", (0.94, 0.95, 0.98, 1.0), metallic=0.1, roughness=0.2)
mat_blue = create_mat("StripeBlue", (0.05, 0.22, 0.65, 1.0), metallic=0.3, roughness=0.2)
mat_red = create_mat("StripeRed", (0.85, 0.12, 0.12, 1.0), metallic=0.2, roughness=0.2)
mat_cockpit_glow = create_mat("CockpitGlow", (1.0, 0.9, 0.4, 1.0), emission=(1.0, 0.85, 0.3, 1.0), emission_strength=3.0)
mat_ice = create_mat("FrostedIce", (0.85, 0.95, 1.0, 1.0), metallic=0.1, roughness=0.6, emission=(0.7, 0.88, 1.0, 1.0), emission_strength=0.8)
mat_engine_dark = create_mat("EngineDark", (0.15, 0.16, 0.18, 1.0), metallic=0.8, roughness=0.3)

# Root object for the airplane
plane_root = bpy.data.objects.new("AirplaneRoot", None)
scene.collection.objects.link(plane_root)

# 1. Main Fuselage
bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=6.0, location=(0, 0, 0))
fuselage = bpy.context.active_object
fuselage.name = "Fuselage"
fuselage.rotation_euler = (math.radians(90), 0, 0)
fuselage.data.materials.append(mat_white)
fuselage.parent = plane_root

# 2. Nose Cone (streamlined aerodynamically)
bpy.ops.mesh.primitive_cone_add(radius1=0.55, depth=2.2, location=(0, 4.1, -0.05))
nose = bpy.context.active_object
nose.name = "Nose"
nose.rotation_euler = (math.radians(-90), 0, 0)
nose.data.materials.append(mat_white)
nose.parent = plane_root

# 3. Cockpit Windshield (angled glass)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 3.2, 0.38))
cockpit = bpy.context.active_object
cockpit.name = "Cockpit"
cockpit.scale = (0.75, 0.8, 0.35)
cockpit.rotation_euler = (math.radians(-25), 0, 0)
cockpit.data.materials.append(mat_cockpit_glow)
cockpit.parent = plane_root

# 4. Main Swept Wings
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.2, -0.15))
wings = bpy.context.active_object
wings.name = "Wings"
wings.scale = (7.5, 1.2, 0.12)
wings.data.materials.append(mat_white)
wings.parent = plane_root

# Winglets
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 3.75, 0.2, 0.3))
    wlet = bpy.context.active_object
    wlet.scale = (0.08, 0.6, 0.8)
    wlet.rotation_euler = (0, math.radians(side * 15), 0)
    wlet.data.materials.append(mat_blue)
    wlet.parent = plane_root

# 5. Twin Jet Engines (mounted on rear pylons)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=1.8, location=(side * 0.95, -1.8, 0.35))
    eng = bpy.context.active_object
    eng.name = f"Engine_{side}"
    eng.rotation_euler = (math.radians(90), 0, 0)
    eng.data.materials.append(mat_white)
    eng.parent = plane_root
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.2, location=(side * 0.95, -0.9, 0.35))
    intake = bpy.context.active_object
    intake.rotation_euler = (math.radians(90), 0, 0)
    intake.data.materials.append(mat_engine_dark)
    intake.parent = plane_root

# 6. T-Tail Vertical & Horizontal Stabilizer
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.5, 1.1))
v_stab = bpy.context.active_object
v_stab.scale = (0.12, 1.2, 1.8)
v_stab.rotation_euler = (math.radians(25), 0, 0)
v_stab.data.materials.append(mat_white)
v_stab.parent = plane_root

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.9, 2.0))
h_stab = bpy.context.active_object
h_stab.scale = (2.8, 0.7, 0.08)
h_stab.data.materials.append(mat_blue)
h_stab.parent = plane_root

# 7. Paint Stripes (Blue & Red lines on side)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.56, 0.5, 0.02))
    stripe_b = bpy.context.active_object
    stripe_b.scale = (0.02, 5.0, 0.12)
    stripe_b.data.materials.append(mat_blue)
    stripe_b.parent = plane_root
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.56, 0.5, -0.12))
    stripe_r = bpy.context.active_object
    stripe_r.scale = (0.02, 4.8, 0.07)
    stripe_r.data.materials.append(mat_red)
    stripe_r.parent = plane_root

# 8. Ice Spikes Layer on Wings
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 2.0, 0.82, -0.12))
    ice = bpy.context.active_object
    ice.name = f"Ice_Wing_{side}"
    ice.scale = (3.6, 0.25, 0.18)
    ice.data.materials.append(mat_ice)
    ice.parent = plane_root

# Position the plane in a dramatic vertical nose-down dive (like the reference video!)
plane_root.rotation_euler = (math.radians(-75), math.radians(15), math.radians(-25))
plane_root.location = (0, 0, 0)

# Camera Setup
cam_data = bpy.data.cameras.new("MainCam")
cam_data.lens = 45 # focal length
cam_obj = bpy.data.objects.new("MainCam", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

cam_obj.location = (1.5, -9.0, 3.5)

# Use Track-To constraint to look directly at the airplane nose
constraint = cam_obj.constraints.new(type='TRACK_TO')
constraint.target = nose
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Lights
sun_data = bpy.data.lights.new("Sun", type='SUN')
sun_data.energy = 5.0
sun_obj = bpy.data.objects.new("Sun", sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.location = (5, -5, 10)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(30))

rim_data = bpy.data.lights.new("RimIce", type='POINT')
rim_data.energy = 800.0
rim_data.color = (0.6, 0.85, 1.0)
rim_obj = bpy.data.objects.new("RimIce", rim_data)
scene.collection.objects.link(rim_obj)
rim_obj.location = (-4, 2, -1)

# Render Single Frame Preview
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

out_preview = Path("C:/Users/Vanes/.gemini/antigravity/brain/74b1259e-ae10-4a5b-b811-7dfee0d04ad5/blender_jet_preview.png")
scene.render.filepath = str(out_preview)

bpy.ops.render.render(write_still=True)
print(f"SAVED PREVIEW TO {out_preview}")
