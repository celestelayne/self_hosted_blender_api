import bpy
import sys
import os
import json

# Get command line arguments after the "--" separator
# Format: blender --background --python process_script.py -- input_file output_file [options]
argv = sys.argv
argv = argv[argv.index("--") + 1:] # Get all the arguments after "--"

# Basic argument validation (checks for three arguments) 
if len(argv) < 3:
    print("Error: Not enough arguments. Usage: blender --background --python process_script.py -- input_file output_file [options]")
    sys.exit(1)

# Get input parameters
input_file = argv[0]
output_format = argv[1]
output_directory = argv[2]

# Validate input
if not os.path.exists(input_file):
    print(f"Error: File {input_file} not found.")
    sys.exit(1)

# Extract file name and set output path
filename = os.path.basename(input_file).split('.')[0]
output_file = os.path.join(output_directory, f"{filename}.{output_format.lower()}")

print('file name:', filename)
print('output file:', output_file)

# Load the model into Blender
def load_model(input_path):
    file_extension = input_path.split('.')[-1].lower()
    try:
        if file_extension == "obj":
            bpy.ops.wm.obj_import(filepath=input_path)
        elif file_extension == "fbx":
            bpy.ops.import_scene.fbx(filepath=input_path)
        elif file_extension in ["glb", "gltf"]:
            bpy.ops.import_scene.gltf(filepath=input_path)
        else:
            print(f"Unsupported file format: {file_extension}")
            sys.exit(1)
        print(f"Successfully loaded {input_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

# apply processing to all imported pbjects
def process_model():
    imported_objects = bpy.context.selected_objects
    if not imported_objects:
        print("Error: No object selected after import.")
        sys.exit(1)

    for obj in imported_objects:
        obj.scale = (1.0, 1.0, 1.0)  # Reset scale
        bpy.ops.object.transform_apply(scale=True)

    # Optimize geometry: Decimate for low-poly
    if bpy.context.object and bpy.context.object.type == 'MESH':
        mod = bpy.context.object.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = 0.5  # Reduce to 50% of original polycount
        bpy.ops.object.modifier_apply(modifier=mod.name)

    print("Model processing complete.")

# Export the model
def export_model(output_path, format_type):
    try:
        if format_type == "glb":
            bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
        elif format_type == "fbx":
            bpy.ops.export_scene.fbx(filepath=output_path)
        elif format_type == "usdz":
            bpy.ops.export_scene.usd(filepath=output_path)
        else:
            print(f"Unsupported export format: {format_type}")
            sys.exit(1)
        print(f"Exported processed model to {output_path}")
    except Exception as e:
        print(f"Error exporting model: {e}")
        sys.exit(1)

# Store metadata
def store_metadata(output_file):
    metadata = {
        "filename": os.path.basename(output_file),
        "format": output_format.upper(),
        "size_kb": os.path.getsize(output_file), # 1024,
        "processing_status": "Completed"
    }
    metadata_file = os.path.join(output_directory, f"{filename}_metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved at {metadata_file}")

# Run the processing workflow
load_model(input_file)
process_model()
export_model(output_file, output_format)
store_metadata(output_file)

print("✅ Model processing pipeline completed successfully!")
sys.exit(0)