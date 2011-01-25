SELECT 
  to_char(framecommon."trackOrbit",'999') AS path, 
  '0' || framecommon.frame AS "row", 
  to_char( localization."timeStamp",'YYYY/MM/DD')  AS date, 
  sensor."name",
  'L' || segmentcommon.mission as sensor
FROM 
  public.sensor, 
  public.localization, 
  public.framecommon, 
  public.segmentcommon, 
  public.satellite
WHERE 
  framecommon.localization_id = localization.id AND
  framecommon.segment_id = segmentcommon.id AND
  segmentcommon.sensor_id = sensor.id AND
  satellite.id = segmentcommon.satellite_id AND
  satellite."name" = 'Landsat'
ORDER BY
  localization."timeStamp"
;
