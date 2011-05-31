BEGIN;

--generate grid
SELECT heatmap_grid_gen(0.25);

--populate grid
SELECT update_heatmap('1900-1-1'::DATE);

COMMIT;