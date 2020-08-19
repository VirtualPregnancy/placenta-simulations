gfx read node terminal

gfx modify g_element "/" general clear;
gfx modify g_element "/" points domain_nodes coordinate coordinates tessellation default_points LOCAL glyph sphere size "2*2*2" offset 0,0,0 font default select_on material default data flow spectrum default selected_material default_selected render_shaded;

gfx mod spec default linear reverse range 0.0 0.5 extend_above extend_below rainbow colour_range 0 1 component 1

gfx cre win
gfx edit sce
