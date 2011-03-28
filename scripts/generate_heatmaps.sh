#!/bin/bash

DB_NAME="sac"
OUTPUT_DIR="/tmp"
HEATMAP_COLORS="heatmap.txt"

#last week
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'7 days'::interval))" PG:dbname=$DB_NAME $OUTPUT_DIR/hm_data_lastweek.tif

gdaldem color-relief $OUTPUT_DIR/hm_data_lastweek.tif $HEATMAP_COLORS $OUTPUT_DIR/heatmap-lastweek.tif

#last month
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'1 month'::interval))" PG:dbname=$DB_NAME $OUTPUT_DIR/hm_data_lastmonth.tif

gdaldem color-relief $OUTPUT_DIR/hm_data_lastmonth.tif $HEATMAP_COLORS $OUTPUT_DIR/heatmap-lastmonth.tif

#last 3 months
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap(date(now()-'3 month'::interval))" PG:dbname=$DB_NAME $OUTPUT_DIR/hm_data_last3month.tif

gdaldem color-relief $OUTPUT_DIR/hm_data_last3month.tif $HEATMAP_COLORS $OUTPUT_DIR/heatmap-last3month.tif

#total
gdal_grid -ot Float32 -a invdist:power=2.0:smoothing=2.0:radius1=1:radius2=1 -of GTiff -txe -180 180 -tye 90 -90 -outsize 1440 720 -zfield hits -sql "select * from heatmap()" PG:dbname=$DB_NAME $OUTPUT_DIR/hm_data_total.tif

gdaldem color-relief $OUTPUT_DIR/hm_data_total.tif $HEATMAP_COLORS $OUTPUT_DIR/heatmap-total.tif
