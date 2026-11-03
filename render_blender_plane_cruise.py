import bpy
import math
from pathlib import Path
import subprocess

out_dir = Path("flows/image_content_generator/remotion/public/avion_hielo_assets").resolve()
frames_dir = out_dir / "cruise_frames"
frames_dir.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 90

def create_mat(name, color, metallic=0.1, roughness=0.2, emission=(0,0,0,1), emission_strength=0.0):
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

mat_white = create_mat("WhiteBody", (0.95, 0.96, 0.98, 1.0), metallic=0.1, roughness=0.15)
mat_blue = create_mat("StripeBlue", (0.05, 0.22, 0.65, 1.0), metallic=0.3, roughness=0.2)
mat_red = create_mat("StripeRed", (0.85, 0.12, 0.12, 1.0), metallic=0.2, roughness=0.2)
mat_cockpit = create_mat("CockpitGlass", (0.05, 0.08, 0.15, 1.0), metallic=0.8, roughness=0.1)
mat_ice = create_mat("FrostedIce", (0.85, 0.95, 1.0, 1.0), metallic=0.1, roughness=0.5, emission=(0.7, 0.9, 1.0, 1.0), emission_strength=1.5)
mat_engine_dark = create_mat("EngineDark", (0.1, 0.12, 0.15, 1.0), metallic=0.8, roughness=0.3)
mat_engine_glow = create_mat("EngineGlow", (1.0, 0.5, 0.1, 1.0), emission=(1.0, 0.5, 0.1, 1.0), emission_strength=5.0)

plane_root = bpy.data.objects.new("AirplaneRoot", None)
scene.collection.objects.link(plane_root)

# Fuselage
bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=5.5, location=(0, 0, 0))
fuselage = bpy.context.active_object
fuselage.rotation_euler = (math.radians(90), 0, 0)
fuselage.data.materials.append(mat_white)
fuselage.parent = plane_root

# Streamlined Nose Cone
bpy.ops.mesh.primitive_cone_add(radius1=0.48, depth=2.0, location=(0, 3.75, -0.05))
nose = bpy.context.active_object
nose.rotation_euler = (math.radians(-90), 0, 0)
nose.data.materials.append(mat_white)
nose.parent = plane_root

# Cockpit Windows
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 2.9, 0.32))
cockpit = bpy.context.active_object
cockpit.scale = (0.7, 0.75, 0.3)
cockpit.rotation_euler = (math.radians(-25), 0, 0)
cockpit.data.materials.append(mat_cockpit)
cockpit.parent = plane_root

# Wings
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.2, -0.15))
wings = bpy.context.active_object
wings.scale = (7.0, 1.1, 0.1)
wings.data.materials.append(mat_white)
wings.parent = plane_root

# Winglets
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 3.5, 0.2, 0.25))
    wlet = bpy.context.active_object
    wlet.scale = (0.08, 0.5, 0.7)
    wlet.rotation_euler = (0, math.radians(side * 15), 0)
    wlet.data.materials.append(mat_blue)
    wlet.parent = plane_root

# Engines
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=1.6, location=(side * 0.88, -1.6, 0.32))
    eng = bpy.context.active_object
    eng.rotation_euler = (math.radians(90), 0, 0)
    eng.data.materials.append(mat_white)
    eng.parent = plane_root
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.1, location=(side * 0.88, -2.4, 0.32))
    exhaust = bpy.context.active_object
    exhaust.rotation_euler = (math.radians(90), 0, 0)
    exhaust.data.materials.append(mat_engine_glow)
    exhaust.parent = plane_root

# T-Tail
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.3, 1.0))
v_stab = bpy.context.active_object
v_stab.scale = (0.1, 1.1, 1.6)
v_stab.rotation_euler = (math.radians(25), 0, 0)
v_stab.data.materials.append(mat_white)
v_stab.parent = plane_root

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.7, 1.8))
h_stab = bpy.context.active_object
h_stab.scale = (2.6, 0.6, 0.08)
h_stab.data.materials.append(mat_blue)
h_stab.parent = plane_root

# Stripes
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.49, 0.5, 0.02))
    st_b = bpy.context.active_object
    st_b.scale = (0.02, 4.6, 0.1)
    st_b.data.materials.append(mat_blue)
    st_b.parent = plane_root

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.49, 0.5, -0.1))
    st_r = bpy.context.active_object
    st_r.scale = (0.02, 4.4, 0.06)
    st_r.data.materials.append(mat_red)
    st_r.parent = plane_root

# Dynamic Ice Formation
ice_objs = []
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 1.8, 0.78, -0.12))
    ice = bpy.context.active_object
    ice.scale = (3.4, 0.22, 0.16)
    ice.data.materials.append(mat_ice)
    ice.parent = plane_root
    ice_objs.append(ice)

# Cruise orientation: Plane flying rightwards across screen (heading +X / +Y)
plane_root.rotation_euler = (math.radians(-5), math.radians(8), math.radians(-70))
plane_root.location = (0, 0, 0)

# Camera Setup: Side profile view
cam_data = bpy.data.cameras.new("CamCruise")
cam_data.lens = 38
cam_obj = bpy.data.objects.new("CamCruise", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, -7.5, 0.5)

constraint = cam_obj.constraints.new(type='TRACK_TO')
constraint.target = fuselage
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Animate gentle aerodynamic floating & growing ice
for f in range(1, 91):
    scene.frame_set(f)
    t = f / 90.0 * math.pi * 2
    plane_root.location.z = math.sin(t * 2) * 0.08
    plane_root.rotation_euler.y = math.radians(8) + math.sin(t * 2) * math.radians(1.5)
    plane_root.keyframe_insert(data_path="location", frame=f)
    plane_root.keyframe_insert(data_path="rotation_euler", frame=f)
    
    # Ice scale grows over time
    ice_scale_factor = 0.5 + (f / 90.0) * 0.6
    for ice_o in ice_objs:
        ice_o.scale.y = 0.22 * ice_scale_factor
        ice_o.scale.z = 0.16 * ice_scale_factor
        ice_o.keyframe_insert(data_path="scale", frame=f)

# Lighting: Storm Moonlight & Freezing Rim
sun_data = bpy.data.lights.new("MoonSun", type='SUN')
sun_data.energy = 4.0
sun_obj = bpy.data.objects.new("MoonSun", sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.location = (5, -3, 8)
sun_obj.rotation_euler = (math.radians(35), math.radians(-20), math.radians(20))

rim_data = bpy.data.lights.new("RimIce", type='POINT')
rim_data.energy = 1200.0
rim_data.color = (0.7, 0.9, 1.0)
rim_obj = bpy.data.objects.new("RimIce", rim_data)
scene.collection.objects.link(rim_obj)
rim_obj.location = (-5, 2, 2)

scene.render.filepath = str(frames_dir / "frame_###.png")
bpy.ops.render.render(animation=True)

out_mp4 = out_dir / "plane_cruise_loop.mp4"
cmd_ff = [
    "ffmpeg", "-y",
    "-framerate", "30",
    "-i", str(frames_dir / "frame_%03d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "18",
    str(out_mp4)
]
subprocess.run(cmd_ff, check=True)
print(f"COMPILED {out_mp4} SUCCESSFULLY!")
