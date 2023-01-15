import bpy

class OBJECT_PT_xfr_uvs(bpy.types.Panel):
    bl_idname = "OBJECT_PT_xfr_uvs"
    bl_label = "Transfer UVs"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UV Xfr"


    def draw(self, context):
        props = context.window_manager.uv_xfr_pg
        layout = self.layout
        # row = layout.row()
        col = layout.column()
        row = col.row()
        row.label(text="Collection")
        row.label(text="Recursive Children")
        row = col.row()
        row.prop(props, "src_coll", text="Source")
        row.prop(props, "src_coll_recur", text="")
        row = col.row()
        row.prop(props, "tgt_coll", text="Target")
        row.prop(props, "tgt_coll_recur", text="")
        col.prop(props, "clear_uvs")
        col.prop(props, "compare_enum")
        col.prop(props, "objname_sep", text="Separator")
        op = col.operator("mesh.xfr_uvs", icon='MESH_CUBE', text="Transfer UVs")
        op.name_compare_type = props.compare_enum
        op.name_sep = props.objname_sep


def register():
    bpy.utils.register_class(OBJECT_PT_xfr_uvs)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_xfr_uvs)