import bpy
import math
from mathutils import Vector
from pathlib import Path
import subprocess

out_dir = Path("flows/image_content_generator/remotion/public/avion_hielo_assets").resolve()
out_dir.mkdir(parents=True, exist_ok=True)
frames_dir = out_dir / "dive_frames"
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
scene.frame_end = 90 # 3.0 sec seamless loop (will be looped in Remotion)

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
mat_ice = create_mat("FrostedIce", (0.85, 0.95, 1.0, 1.0), metallic=0.1, roughness=0.5, emission=(0.7, 0.9, 1.0, 1.0), emission_strength=1.2)
mat_engine_dark = create_mat("EngineDark", (0.1, 0.12, 0.15, 1.0), metallic=0.8, roughness=0.3)
mat_engine_glow = create_mat("EngineGlow", (1.0, 0.5, 0.1, 1.0), emission=(1.0, 0.5, 0.1, 1.0), emission_strength=5.0)

# Airplane Root
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

# Engines on rear pylons
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=1.6, location=(side * 0.88, -1.6, 0.32))
    eng = bpy.context.active_object
    eng.rotation_euler = (math.radians(90), 0, 0)
    eng.data.materials.append(mat_white)
    eng.parent = plane_root
    
    # Engine exhaust glow
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

# Ice on Wings (spikes along leading edge)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 1.8, 0.78, -0.12))
    ice = bpy.context.active_object
    ice.scale = (3.4, 0.22, 0.16)
    ice.data.materials.append(mat_ice)
    ice.parent = plane_root

# Orientation: Diagonal plunge from top-left to bottom-right!
# Pitch down ~75 deg, roll ~25 deg, yaw ~-35 deg
plane_root.rotation_euler = (math.radians(-72), math.radians(24), math.radians(-32))
plane_root.location = (0.2, 0.2, -0.2)

# Camera Setup
cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 42
cam_obj = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (1.2, -7.5, 3.2)

constraint = cam_obj.constraints.new(type='TRACK_TO')
constraint.target = nose
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Animate subtle camera vibration & plane aerodynamic turbulence over 90 frames
for f in range(1, 91):
    scene.frame_set(f)
    t = f / 90.0 * math.pi * 4
    # Subtle wobble
    plane_root.rotation_euler.x = math.radians(-72) + math.sin(t * 3) * math.radians(1.2)
    plane_root.rotation_euler.y = math.radians(24) + math.cos(t * 2.5) * math.radians(1.5)
    plane_root.location.x = 0.2 + math.sin(t * 4) * 0.05
    plane_root.location.z = -0.2 + math.cos(t * 3.5) * 0.04
    plane_root.keyframe_insert(data_path="rotation_euler", frame=f)
    plane_root.keyframe_insert(data_path="location", frame=f)

# Lighting: Key Sun + Cold Rim Lights
sun_data = bpy.data.lights.new("Sun", type='SUN')
sun_data.energy = 5.0
sun_obj = bpy.data.objects.new("Sun", sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.location = (6, -4, 10)
sun_obj.rotation_euler = (math.radians(50), math.radians(15), math.radians(35))

rim_data = bpy.data.lights.new("RimIce", type='POINT')
rim_data.energy = 1000.0
rim_data.color = (0.65, 0.88, 1.0)
rim_obj = bpy.data.objects.new("RimIce", rim_data)
scene.collection.objects.link(rim_obj)
rim_obj.location = (-4, 3, 0)

# Render frames
scene.render.filepath = str(frames_dir / "frame_###.png")
bpy.ops.render.render(animation=True)

print("ALL 90 FRAMES RENDERED. COMPILING MP4 WITH FFMPEG...")
# Compile with ffmpeg
out_mp4 = out_dir / "plane_dive_loop.mp4"
cmd_ff = [
    "ffmpeg", "-y",
    "-framerate", "30",
    "-i", str(frames_dir / "frame_%03d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuva420p",
    "-preset", "fast",
    "-crf", "18",
    str(out_mp4)
]
subprocess.run(cmd_ff, check=True)
print(f"COMPILED {out_mp4} SUCCESSFULLY!")
