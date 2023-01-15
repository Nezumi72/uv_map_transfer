import bpy


def get_obj_names(coll, coll_recur):
    try:
        obj_names = [object.name for object in coll.objects if object.type == 'MESH']
        if coll_recur:
            for child_coll in coll.children_recursive:
                obj_names += [object.name for object in child_coll.objects if object.type == 'MESH']
    except KeyError:
        obj_names = None
    return obj_names


def rem_uvs(obj):
    while len(obj.data.uv_layers) > 0:
        obj.data.uv_layers.remove(obj.data.uv_layers[0])


def get_src_obj(cmp_name, cmp_list, name_sep):
    obj = None
    if len(cmp_name.split(name_sep)) > 2:
        name_parts = cmp_name.split(name_sep)[:-1]
        test_name = name_sep.join(name_parts)
        if test_name in cmp_list:
            obj = bpy.data.objects.get(test_name)
    else:
        test_name = cmp_name.split(name_sep)[0]
        if test_name in cmp_list:
            obj = bpy.data.objects.get(test_name)
    return obj


def cmp_both(cmp_name, cmp_list, name_sep):
    obj = None
    test_src_name = test_tgt_name = ""
    if len(cmp_name.split(name_sep)) > 2:
        name_parts = cmp_name.split(name_sep)[:-1]
        test_src_name = name_sep.join(name_parts)
    else:
        test_src_name = cmp_name.split(name_sep)[0]
    for tgt_name in cmp_list:
        if len(tgt_name.split(name_sep)) > 2:
            name_parts = tgt_name.split(name_sep)[:-1]
            test_tgt_name = name_sep.join(name_parts)
        else:
            test_tgt_name = tgt_name.split(name_sep)[0]
        if test_src_name == test_tgt_name:
            obj = bpy.data.objects.get(tgt_name)
            return obj
    return obj

class MESH_OT_xfr_uvs(bpy.types.Operator):
    bl_idname = 'mesh.xfr_uvs'
    bl_label = 'Transfer UVs'
    bl_options = {"REGISTER", "UNDO"}

    name_compare_type: bpy.props.StringProperty()
    name_sep: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        props = context.window_manager.uv_xfr_pg
        return props.src_coll and props.tgt_coll


    def execute(self, context):
        # print(f"{self.bl_idname} executed with {self.name_compare_type} value")
        props = context.window_manager.uv_xfr_pg
        obj_names_src_coll = get_obj_names(props.src_coll, props.src_coll_recur)
        obj_names_tgt_coll = get_obj_names(props.tgt_coll, props.tgt_coll_recur)
        if self.name_compare_type == 'strip_tgt_ext':
            for obj_name_tgt in obj_names_tgt_coll:
                bpy.ops.object.select_all(action='DESELECT')
                obj_tgt = bpy.data.objects.get(obj_name_tgt)
                obj_src = get_src_obj(obj_name_tgt, obj_names_src_coll, self.name_sep)
                if obj_tgt and obj_src:
                    obj_tgt.select_set(True)
                    obj_src.select_set(True)
                    context.view_layer.objects.active = obj_src
                    # print(f"{obj_tgt.name} matches {obj_src.name}")
                    if props.clear_uvs:
                        rem_uvs(obj_tgt)
                    for uv in obj_src.data.uv_layers:
                        uv.active = True
                        if props.clear_uvs:
                            new_uv = obj_tgt.data.uv_layers.new(name = uv.name)
                            new_uv.active = True
                        else:
                            try:
                                obj_tgt.data.uv_layers.active = obj_tgt.data.uv_layers[uv.name]
                            except KeyError:
                                new_uv = obj_tgt.data.uv_layers.new(name = uv.name)
                                new_uv.active = True
                        bpy.ops.object.join_uvs()
                # else:
                #     print(f"no match found for {obj_name_tgt}")
        elif self.name_compare_type == 'strip_src_ext':
            for obj_name_src in obj_names_src_coll:
                bpy.ops.object.select_all(action='DESELECT')
                obj_tgt = get_src_obj(obj_name_src, obj_names_tgt_coll, self.name_sep)
                obj_src = bpy.data.objects.get(obj_name_src)
                if obj_tgt and obj_src:
                    obj_tgt.select_set(True)
                    obj_src.select_set(True)
                    context.view_layer.objects.active = obj_src
                    # print(f"{obj_tgt.name} matches {obj_src.name}")
                    if props.clear_uvs:
                        rem_uvs(obj_tgt)
                    for uv in obj_src.data.uv_layers:
                        uv.active = True
                        if props.clear_uvs:
                            new_uv = obj_tgt.data.uv_layers.new(name = uv.name)
                            new_uv.active = True
                        else:
                            try:
                                obj_tgt.data.uv_layers.active = obj_tgt.data.uv_layers[uv.name]
                            except KeyError:
                                new_uv = obj_tgt.data.uv_layers.new(name = uv.name)
                                new_uv.active = True
                        bpy.ops.object.join_uvs()
                # else:
                #     print(f"no match found for {obj_name_src}")
        elif self.name_compare_type == 'strip_both_ext':
            for obj_name_src in obj_names_src_coll:
                bpy.ops.object.select_all(action='DESELECT')
                obj_tgt = cmp_both(obj_name_src, obj_names_tgt_coll, self.name_sep)
                obj_src = bpy.data.objects.get(obj_name_src)
                if obj_tgt and obj_src:
                    obj_tgt.select_set(True)
                    obj_src.select_set(True)
                    context.view_layer.objects.active = obj_src
                    # print(f"{obj_tgt.name} matches {obj_src.name}")
                    if props.clear_uvs:
                        rem_uvs(obj_tgt)
                    for uv in obj_src.data.uv_layers:
                        uv.active = True
                        if props.clear_uvs:
                            new_uv = obj_tgt.data.uv_layers.new(name = uv.name)
                            new_uv.active = True
                        else:
                            try:
                                obj_tgt.data.uv_layers.active = obj_tgt.data.uv_layers[uv.name]
                            except KeyError:
                                new_uv = obj_tgt.data.uv_layers.new(name = uv.name)
                                new_uv.active = True
                        bpy.ops.object.join_uvs()
                # else:
                #     print(f"no match found for {obj_name_src}")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(MESH_OT_xfr_uvs)


def unregister():
    bpy.utils.unregister_class(MESH_OT_xfr_uvs)