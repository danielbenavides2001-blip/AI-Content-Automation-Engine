import bpy
import math
from pathlib import Path
import subprocess

repo_root = Path(r"C:\Users\Vanes\.gemini\antigravity\scratch\AI-Content-Automation-Engine1")
out_dir = repo_root / "flows" / "image_content_generator" / "remotion" / "public" / "avion_hielo_assets"
frames_dir = out_dir / "airfoil_frames"
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

mat_wing = create_mat("AirfoilWing", (0.15, 0.22, 0.35, 1.0), metallic=0.7, roughness=0.2)
mat_ice = create_mat("IceRough", (0.8, 0.95, 1.0, 1.0), metallic=0.1, roughness=0.6, emission=(0.7, 0.95, 1.0, 1.0), emission_strength=2.0)
mat_streamline_cyan = create_mat("StreamCyan", (0.2, 0.8, 1.0, 1.0), emission=(0.2, 0.8, 1.0, 1.0), emission_strength=4.0)
mat_streamline_red = create_mat("StreamRed", (1.0, 0.2, 0.1, 1.0), emission=(1.0, 0.2, 0.1, 1.0), emission_strength=5.0)

airfoil_root = bpy.data.objects.new("AirfoilRoot", None)
scene.collection.objects.link(airfoil_root)

# Create 3D Airfoil cross-section
# Profile: curve extruded along Y axis
verts = [
    (-2.2, 0, 0),      # Leading edge
    (-1.8, 0, 0.4),
    (-1.0, 0, 0.65),   # Max camber top
    (0.0, 0, 0.6),
    (1.0, 0, 0.35),
    (2.0, 0, 0.05),    # Trailing edge top
    (2.2, 0, 0),       # Trailing edge tip
    (2.0, 0, -0.05),
    (1.0, 0, -0.2),
    (0.0, 0, -0.3),
    (-1.0, 0, -0.35),  # Lower surface
    (-1.8, 0, -0.25)
]

mesh = bpy.data.meshes.new("AirfoilMesh")
# Extrude in Y from -2.5 to +2.5
all_verts = []
for y in [-3.0, 3.0]:
    for vx, vy, vz in verts:
        all_verts.append((vx, y, vz))

faces = []
n_v = len(verts)
for i in range(n_v):
    next_i = (i + 1) % n_v
    faces.append((i, next_i, next_i + n_v, i + n_v))

mesh.from_pydata(all_verts, [], faces)
mesh.update()

airfoil_obj = bpy.data.objects.new("Airfoil", mesh)
scene.collection.objects.link(airfoil_obj)
airfoil_obj.data.materials.append(mat_wing)
airfoil_obj.parent = airfoil_root

# Add Ice formation on leading edge (-2.2, 0, 0)
ice_parent = bpy.data.objects.new("IceGroup", None)
scene.collection.objects.link(ice_parent)
ice_parent.parent = airfoil_root

for i in range(12):
    y_pos = -2.8 + i * 0.5
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.25, location=(-2.25, y_pos, 0.05))
    ice_chunk = bpy.context.active_object
    ice_chunk.scale = (1.2, 0.8, 1.4)
    ice_chunk.data.materials.append(mat_ice)
    ice_chunk.parent = ice_parent

# Streamline tubes flowing past the airfoil
stream_lines = []
for s_idx in range(8):
    z_offset = -0.8 + s_idx * 0.35
    curve_data = bpy.data.curves.new(f"Streamline_{s_idx}", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.035
    polyline = curve_data.splines.new('BEZIER')
    polyline.bezier_points.add(3)
    
    # Points from X=-6 to X=5
    p0 = polyline.bezier_points[0]
    p0.co = (-5.5, 0, z_offset)
    p0.handle_right = (-4.0, 0, z_offset)
    
    p1 = polyline.bezier_points[1]
    # Deflection over airfoil
    lift_dz = 0.6 if z_offset > 0 else -0.3
    p1.co = (-1.0, 0, z_offset + lift_dz)
    p1.handle_left = (-2.5, 0, z_offset + lift_dz)
    p1.handle_right = (0.5, 0, z_offset + lift_dz)
    
    p2 = polyline.bezier_points[2]
    p2.co = (2.2, 0, z_offset + lift_dz * 0.5)
    p2.handle_left = (1.2, 0, z_offset + lift_dz)
    p2.handle_right = (3.5, 0, z_offset + lift_dz * 0.2)
    
    p3 = polyline.bezier_points[3]
    p3.co = (5.5, 0, z_offset - 0.2)
    p3.handle_left = (4.0, 0, z_offset)
    
    stream_obj = bpy.data.objects.new(f"Stream_{s_idx}", curve_data)
    scene.collection.objects.link(stream_obj)
    stream_obj.data.materials.append(mat_streamline_cyan if z_offset < 0.2 else mat_streamline_red)
    stream_lines.append(stream_obj)

# Camera: Profile side view
cam_data = bpy.data.cameras.new("CamAirfoil")
cam_data.lens = 45
cam_obj = bpy.data.objects.new("CamAirfoil", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, -11.0, 0.4)
cam_obj.rotation_euler = (math.radians(90), 0, 0)

# Rotate Airfoil root from 10 deg to 35 deg (Stall pitch up)
for f in range(1, 91):
    scene.frame_set(f)
    t = (f - 1) / 90.0
    # Tilt up: start at 8 deg pitch, increase to 32 deg stall
    pitch = math.radians(8 + t * 24)
    airfoil_root.rotation_euler = (0, 0, -pitch)
    airfoil_root.keyframe_insert(data_path="rotation_euler", frame=f)

# Studio Lights
sun_data = bpy.data.lights.new("SunTech", type='SUN')
sun_data.energy = 3.5
sun_obj = bpy.data.objects.new("SunTech", sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.location = (5, -5, 8)

fill_data = bpy.data.lights.new("FillTech", type='AREA')
fill_data.energy = 500.0
fill_data.color = (0.2, 0.6, 1.0)
fill_obj = bpy.data.objects.new("FillTech", fill_data)
scene.collection.objects.link(fill_obj)
fill_obj.location = (-4, -6, 2)

scene.render.filepath = str(frames_dir / "frame_###.png")
print("Rendering 3D Airfoil Stall Animation...")
bpy.ops.render.render(animation=True)

out_mp4 = out_dir / "airfoil_stall.mp4"
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
print(f"AIRFOIL STALL MP4 COMPILED: {out_mp4}")
