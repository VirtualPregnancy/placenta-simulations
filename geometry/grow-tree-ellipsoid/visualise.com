gfx read node output/full_tree 
gfx read elem output/full_tree 

gfx read data output/terminals 

gfx modify g_element villous general clear;
gfx modify g_element villous points domain_datapoints coordinate coordinates tessellation default_points LOCAL glyph sphere size "1*1*1" offset 0,0,0 font default select_on material silver selected_material default_selected render_shaded;

gfx modify g_element placenta general clear;
gfx modify g_element placenta lines domain_mesh1d coordinate coordinates face all tessellation default LOCAL circle_extrusion line_base_size 0.5 select_on material cyan selected_material default_selected render_shaded;


gfx cre win
gfx edit sce

#Window setings pasted from CMGUI

gfx create window 1 double_buffer;
gfx modify window 1 image scene "/" filter default infinite_viewer_lighting two_sided_lighting;
gfx modify window 1 image add_light default;
gfx modify window 1 image add_light default_ambient;
gfx modify window 1 layout simple ortho_axes z -y eye_spacing 0.25 width 811 height 780;
gfx modify window 1 set current_pane 1;
gfx modify window 1 background colour 0 0 0 texture none;
gfx modify window 1 view parallel eye_point 81.8184 69.6067 527.316 interest_point -0.0851707 -0.201813 11.7811 up_vector -0.75307 0.657226 0.0306462 view_angle 40 near_clipping_plane 26.3324 far_clipping_plane 1068.81 relative_viewport ndc_placement -1 1 2 2 viewport_coordinates 0 0 1 1;
gfx modify window 1 set transform_tool current_pane 1 std_view_angle 40 normal_lines no_antialias depth_of_field 0.0 fast_transparency blend_normal;