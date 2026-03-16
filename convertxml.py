import re

# Read the XML file
xml_path = 'stretch.xml'  # Change this to your actual XML file path
with open(xml_path, 'r') as f:
    content = f.read()

# Find all meshes with inertia="shell"
meshes_to_fix = [
    'base_link_2',
    'base_link_6',
    'link_aruco_right_base',
    'link_aruco_left_base',
    'link_lift_1',
    'link_aruco_shoulder',
    'link_aruco_inner_wrist',
    'link_aruco_top_wrist',
    'link_SG3_aruco_d405',
    'link_SG3_gripper_left_finger_aruco',
    'link_SG3_gripper_right_finger_aruco'
]

# Step 1: Remove inertia="shell" from all mesh definitions in <asset> section
content = re.sub(r' inertia="shell"', '', content)

# Step 2: Add shellinertia="true" to corresponding geom tags
for mesh_name in meshes_to_fix:
    # Pattern to match geom tags with this mesh that don't already have shellinertia
    # We need to be careful to only add it once and to visual geoms
    pattern = rf'(<geom[^>]*mesh="{mesh_name}"[^>]*class="visual"[^>]*)(/?>)'
    
    def add_shellinertia(match):
        geom_tag = match.group(1)
        closing = match.group(2)
        # Only add if not already present
        if 'shellinertia' not in geom_tag:
            return geom_tag + ' shellinertia="true"' + closing
        return match.group(0)
    
    content = re.sub(pattern, add_shellinertia, content)

# Write the fixed version
output_path = 'stretch_mujoco3.xml'
with open(output_path, 'w') as f:
    f.write(content)

print(f"✓ Converted XML saved as {output_path}")
print(f"✓ Fixed {len(meshes_to_fix)} meshes for MuJoCo 3.x compatibility")
print("\nChanges made:")
print("  - Removed inertia='shell' from <mesh> tags")
print("  - Added shellinertia='true' to corresponding <geom> tags")