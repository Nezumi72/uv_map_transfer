import bpy

def p_filter(self, coll):
    return coll in bpy.context.scene.collection.children_recursive

class UVXFR_PG_props(bpy.types.PropertyGroup):
    src_coll: bpy.props.PointerProperty(
        type=bpy.types.Collection,
        poll=p_filter,
        )
    src_coll_recur: bpy.props.BoolProperty(
        name="src_coll_recur",
        description="Use recursive children search",
        default=False,
    )
    tgt_coll: bpy.props.PointerProperty(
        type=bpy.types.Collection,
        poll=p_filter,
        )
    tgt_coll_recur: bpy.props.BoolProperty(
        name="tgt_coll_recur",
        description="Use recursive children search",
        default=False,
    )
    clear_uvs: bpy.props.BoolProperty(
        name="clear_uvs",
        description="Remove all existing target object UV maps",
        default=True,
    )
    compare_enum: bpy.props.EnumProperty(
        name="compare_enum",
        items=(
            ("strip_src_ext", "Strip Source", "Strip source name characters from last instance of separator to match target name"),
            ("strip_tgt_ext", "Strip Target", "Strip target name characters from last instance of separator to match source name"),
            ("strip_both_ext", "Strip Both", "Strip both names characters from last instance of separator to match"),
        ),
        description="",
        default="strip_tgt_ext",
    )
    objname_sep: bpy.props.StringProperty(
        name="objname_sep",
        description="Separator between name parts",
        default=".",
    )

classes = [
    UVXFR_PG_props,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.uv_xfr_pg = bpy.props.PointerProperty(
        type=UVXFR_PG_props)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.uv_xfr_pg