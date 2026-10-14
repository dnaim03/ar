import bpy

def create_material(name, color, roughness=0.4):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
    return mat

def clear_mesh_objects():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def make_low_mb_dragon():
    clear_mesh_objects()

    # Materials
    body_mat  = create_material("DragonBody", (0.12, 0.65, 0.38, 1.0))
    belly_mat = create_material("DragonBelly", (0.95, 0.85, 0.45, 1.0))
    spike_mat = create_material("DragonSpikes", (0.9, 0.3, 0.25, 1.0))
    eye_mat   = create_material("DragonEyes", (0.02, 0.02, 0.02, 1.0), roughness=0.1)
    white_mat = create_material("DragonHighlights", (1.0, 1.0, 1.0, 1.0), roughness=0.1)

    dragon_parts = []

    # 1. Head (Low poly resolution)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.75, location=(0, 0, 2.3))
    head = bpy.context.active_object
    head.scale = (1.0, 1.05, 0.95)
    head.data.materials.append(body_mat)
    dragon_parts.append(head)

    # 2. Snout & Nostrils
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.5, location=(0, -0.65, 2.1))
    snout = bpy.context.active_object
    snout.scale = (0.9, 1.2, 0.75)
    snout.data.materials.append(body_mat)
    dragon_parts.append(snout)

    for x_offset in [-0.15, 0.15]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.06, location=(x_offset, -1.15, 2.25))
        nostril = bpy.context.active_object
        nostril.data.materials.append(body_mat)
        dragon_parts.append(nostril)

    # 3. Body & Belly
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.9, location=(0, 0, 1.15))
    body = bpy.context.active_object
    body.scale = (0.95, 1.05, 1.3)
    body.data.materials.append(body_mat)
    dragon_parts.append(body)

    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.75, location=(0, -0.32, 1.05))
    belly = bpy.context.active_object
    belly.scale = (0.7, 0.65, 1.05)
    belly.data.materials.append(belly_mat)
    dragon_parts.append(belly)

    # 4. Eyes & Highlights
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.15, location=(side * 0.35, -0.55, 2.45))
        eye = bpy.context.active_object
        eye.data.materials.append(eye_mat)
        dragon_parts.append(eye)

        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.04, location=(side * 0.32, -0.68, 2.52))
        shine = bpy.context.active_object
        shine.data.materials.append(white_mat)
        dragon_parts.append(shine)

    # 5. Horns
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.14, depth=0.7, location=(side * 0.35, 0.25, 2.85))
        horn = bpy.context.active_object
        horn.rotation_euler = (-0.3, side * 0.3, 0)
        horn.data.materials.append(spike_mat)
        dragon_parts.append(horn)

    # 6. Spine Spikes
    spike_configs = [
        ((0, 0.5, 2.7), (0.2, 0, 0), 0.12),
        ((0, 0.65, 2.3), (0.4, 0, 0), 0.13),
        ((0, 0.7, 1.8), (0.5, 0, 0), 0.14),
        ((0, 0.75, 1.3), (0.6, 0, 0), 0.12),
        ((0, 0.7, 0.8), (0.8, 0, 0), 0.10),
        ((0, 0.85, 0.4), (1.1, 0, 0), 0.08),
    ]
    for loc, rot, rad in spike_configs:
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=rad, depth=rad*3, location=loc)
        spike = bpy.context.active_object
        spike.rotation_euler = rot
        spike.data.materials.append(spike_mat)
        dragon_parts.append(spike)

    # 7. Limbs
    for side in [-1, 1]:
        # Feet
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.3, location=(side * 0.65, -0.2, 0.25))
        foot = bpy.context.active_object
        foot.scale = (0.9, 1.4, 0.6)
        foot.data.materials.append(body_mat)
        dragon_parts.append(foot)

        # Arms
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.2, location=(side * 0.6, -0.4, 1.25))
        arm = bpy.context.active_object
        arm.scale = (0.7, 1.1, 0.7)
        arm.rotation_euler = (0.4, side * -0.4, -0.2 * side)
        arm.data.materials.append(body_mat)
        dragon_parts.append(arm)

    # 8. Tail
    tail_segments = [
        ((0, 0.65, 0.6), (0.5, 0, 0), (0.32, 0.32, 0.5)),
        ((0, 1.0, 0.35), (0.9, 0, 0), (0.25, 0.25, 0.5)),
        ((0.15, 1.3, 0.25), (1.2, 0, 0.4), (0.18, 0.18, 0.4)),
    ]
    for loc, rot, sca in tail_segments:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=1.0, location=loc)
        tail = bpy.context.active_object
        tail.scale = sca
        tail.rotation_euler = rot
        tail.data.materials.append(body_mat)
        dragon_parts.append(tail)

    # 9. Wings
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.55, depth=0.08, location=(side * 0.85, 0.45, 1.45))
        wing = bpy.context.active_object
        wing.scale = (1.2, 0.7, 1.0)
        wing.rotation_euler = (1.3, side * 0.7, -0.2)
        wing.data.materials.append(spike_mat)
        dragon_parts.append(wing)

    # 10. Join & Smooth
    bpy.ops.object.select_all(action='DESELECT')
    for obj in dragon_parts:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = head
    bpy.ops.object.join()
    head.name = "Compact_Dragon"
    bpy.ops.object.shade_smooth()

make_low_mb_dragon()