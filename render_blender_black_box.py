import bpy
import math
from pathlib import Path
import subprocess

repo_root = Path(r"C:\Users\Vanes\.gemini\antigravity\scratch\AI-Content-Automation-Engine1")
out_dir = repo_root / "flows" / "image_content_generator" / "remotion" / "public" / "avion_hielo_assets"
frames_dir = out_dir / "blackbox_frames"
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

def create_mat(name, color, metallic=0.2, roughness=0.3, emission=(0,0,0,1), emission_strength=0.0):
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

mat_orange = create_mat("SafetyOrange", (1.0, 0.28, 0.02, 1.0), metallic=0.15, roughness=0.35)
mat_metal_silver = create_mat("BeaconSilver", (0.85, 0.88, 0.9, 1.0), metallic=0.9, roughness=0.15)
mat_dark_steel = create_mat("DarkSteel", (0.12, 0.14, 0.16, 1.0), metallic=0.8, roughness=0.4)
mat_white_stripe = create_mat("ReflectiveWhite", (0.95, 0.95, 0.95, 1.0), metallic=0.1, roughness=0.2)
mat_yellow_stripe = create_mat("CautionYellow", (0.95, 0.85, 0.05, 1.0), metallic=0.1, roughness=0.2)

bb_root = bpy.data.objects.new("BlackBoxRoot", None)
scene.collection.objects.link(bb_root)

# Main Box Chassis
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
chassis = bpy.context.active_object
chassis.scale = (1.6, 2.8, 1.4)
chassis.data.materials.append(mat_orange)
chassis.parent = bb_root

# Base mounting plate / handles
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.75))
base_plate = bpy.context.active_object
base_plate.scale = (1.9, 3.1, 0.12)
base_plate.data.materials.append(mat_dark_steel)
base_plate.parent = bb_root

# Cylindrical Crash-Survivable Memory Unit (CSMU) mounted on rear
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=1.5, location=(0, -0.6, 1.0))
csmu = bpy.context.active_object
csmu.rotation_euler = (math.radians(90), 0, 0)
csmu.data.materials.append(mat_orange)
csmu.parent = bb_root

# CSMU Dome Cap
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(0, -1.35, 1.0))
dome = bpy.context.active_object
dome.scale = (1.0, 0.5, 1.0)
dome.data.materials.append(mat_orange)
dome.parent = bb_root

# Underwater Locator Beacon (ULB / Pinger cylinder)
bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.1, location=(0.6, 0.8, 0.4))
ulb = bpy.context.active_object
ulb.rotation_euler = (math.radians(90), 0, 0)
ulb.data.materials.append(mat_metal_silver)
ulb.parent = bb_root

# ULB bracket rings
for y_pos in [0.4, 1.2]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.12, location=(0.6, y_pos, 0.4))
    bracket = bpy.context.active_object
    bracket.rotation_euler = (math.radians(90), 0, 0)
    bracket.data.materials.append(mat_dark_steel)
    bracket.parent = bb_root

# Stencil stripes / Decals
for z_pos in [0.2, -0.2]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.81, 0, z_pos))
    stripe = bpy.context.active_object
    stripe.scale = (0.02, 2.5, 0.12)
    stripe.data.materials.append(mat_white_stripe)
    stripe.parent = bb_root

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.81, 0, z_pos))
    stripe2 = bpy.context.active_object
    stripe2.scale = (0.02, 2.5, 0.12)
    stripe2.data.materials.append(mat_white_stripe)
    stripe2.parent = bb_root

# Black Box Front Handle
bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.06, location=(0, 1.45, 0))
handle = bpy.context.active_object
handle.rotation_euler = (math.radians(90), 0, 0)
handle.data.materials.append(mat_dark_steel)
handle.parent = bb_root

# Slight tilt for dynamic isometric view
bb_root.rotation_euler = (math.radians(18), 0, 0)

# Camera Setup
cam_data = bpy.data.cameras.new("CamBB")
cam_data.lens = 50
cam_obj = bpy.data.objects.new("CamBB", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, -6.8, 1.8)

constraint = cam_obj.constraints.new(type='TRACK_TO')
constraint.target = chassis
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Animate 360-degree rotation
for f in range(1, 91):
    scene.frame_set(f)
    angle = (f - 1) / 90.0 * math.pi * 2
    bb_root.rotation_euler.z = angle
    bb_root.location.z = math.sin(angle * 2) * 0.05
    bb_root.keyframe_insert(data_path="rotation_euler", frame=f)
    bb_root.keyframe_insert(data_path="location", frame=f)

# Lighting: Dramatic Studio 3-point
key_light = bpy.data.lights.new("KeyLight", type='AREA')
key_light.energy = 800.0
key_light.size = 2.0
key_obj = bpy.data.objects.new("KeyLight", key_light)
scene.collection.objects.link(key_obj)
key_obj.location = (4, -4, 5)

fill_light = bpy.data.lights.new("FillLight", type='AREA')
fill_light.energy = 300.0
fill_light.color = (0.8, 0.9, 1.0)
fill_obj = bpy.data.objects.new("FillLight", fill_light)
scene.collection.objects.link(fill_obj)
fill_obj.location = (-4, -3, 3)

rim_light = bpy.data.lights.new("RimLight", type='SUN')
rim_light.energy = 4.0
rim_obj = bpy.data.objects.new("RimLight", rim_light)
scene.collection.objects.link(rim_obj)
rim_obj.location = (0, 6, 4)
rim_obj.rotation_euler = (math.radians(-45), 0, 0)

scene.render.filepath = str(frames_dir / "frame_###.png")
print("Rendering Black Box 3D Turntable...")
bpy.ops.render.render(animation=True)

out_mp4 = out_dir / "black_box_3d.mp4"
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
print(f"BLACK BOX 3D MP4 COMPILED: {out_mp4}")
