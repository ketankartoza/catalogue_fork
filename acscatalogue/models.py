#for translation
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.gis.db import models
from catalogue.models import *

# Create your models here.
class Sensor(models.Model):
    original_id = models.IntegerField('Original ID', db_index=True,unique=True)
    name = models.CharField('Name', max_length=64)
    common_name = models.CharField('Common Name', max_length=64)
    description = models.CharField('Description', max_length=255)
    has_data = models.BooleanField(help_text='Mark false if there is no data for this sensor')

    class Meta:
        db_table = 'sensor'
        verbose_name = _('Sensor')
        verbose_name_plural = _('Sensors')

    def __unicode__(self):
        return self.common_name

    def cleanName(self):
        return self.name.replace(" ","_").replace(",","_")
###############################################################################
#
# Auxilliary / lookup tables first
#

class DataMode(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    name = models.CharField(max_length=60)

    class Meta:
        db_table='datamode'
        verbose_name=_("Data Mode")
        verbose_name_plural=_("Data Modes")

    def __unicode__(self):
        return self.name

###############################################################################

class EllipsoidType(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    description = models.CharField(max_length=20)

    def __unicode__(self):
        return self.description

    class Meta:
        db_table='ellipsoidtype'
        verbose_name=_("Ellipsoid Type")
        verbose_name_plural=_("Ellipsoid Types")

###############################################################################

class ErsCompMode(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    description = models.CharField(max_length=20)

    def __unicode__(self):
        return self.description

    class Meta:
        db_table='erscompmode'
        verbose_name=_("Ers Comp Mode")
        verbose_name_plural=_("Ers Comp Modes")

###############################################################################

class FileType(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    fileTypeName = models.CharField(max_length=64)

    def __unicode__(self):
        return self.fileTypeName

    class Meta:
        db_table='filetype'
        verbose_name=_("File Type")
        verbose_name_plural=_("File Types")

###############################################################################

class Satellite(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table='satellite'
        verbose_name=_("Satellite")
        verbose_name_plural=_("Satellites")

###############################################################################

class SpotAcquisitionMode(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table='spotacquisitionmode'
        verbose_name=_("Spot Acquisition Mode")
        verbose_name_plural=_("Spot Acquisition Modes")

###############################################################################

class Station(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table='station'
        verbose_name=_("Station")
        verbose_name_plural=_("Stations")

###############################################################################

class Superclass(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table='superclass'
        verbose_name=_("Superclass")
        verbose_name_plural=_("Super class")

###############################################################################

class HeaderType(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table='headertype'
        verbose_name=_("Header Type")
        verbose_name_plural=_("Header Types")

###############################################################################
#
# Main data tables
#
class Medium (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    medium = models.CharField(max_length=12)
    mediumType = models.CharField(max_length=12)
    numOfPasses = models.IntegerField()
    timeCodeType = models.CharField(max_length=8)
    storageStation = models.IntegerField()
    mediumLoc = models.CharField(max_length=12)
    density = models.IntegerField()
    model = models.CharField(max_length=16)
    headerType = models.ForeignKey(HeaderType)

    def __unicode__(self):
        return str(self.medium)

    class Meta:
        db_table='medium'
        verbose_name=_("Medium")
        verbose_name_plural=_("Medium")

###############################################################################

class Localization (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    supertype =  models.ForeignKey(Superclass)
    geometry = models.PolygonField(srid=4326)
    refreshRate = models.IntegerField()
    timeStamp = models.DateTimeField()
    # needed for any model with geom so that we can
    # do geom filters etc
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='localization'
        verbose_name=_("Localization")
        verbose_name_plural=_("Localizations")

###############################################################################

class SegmentCommon (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    satellite = models.ForeignKey( Satellite )
    mission = models.IntegerField()
    sensor = models.ForeignKey( Sensor )
    medium = models.ForeignKey( Medium )
    ascendingFlag = models.BooleanField()
    geometry = models.PolygonField(srid=4326)
    station = models.ForeignKey( Station )
    insertionDate = models.DateTimeField()
    begRecordDate = models.DateTimeField()
    endRecordDate = models.DateTimeField()
    orbit = models.IntegerField()
    cycle = models.IntegerField()
    iLatMin = models.FloatField()
    iLonMin = models.FloatField()
    iLatMax = models.FloatField()
    iLonMax = models.FloatField()
    firstAddress = models.IntegerField()
    secondAddress = models.IntegerField()
    displayedTrack = models.CharField(max_length=64)
    displayedOrbit = models.IntegerField()
    displayedMedium = models.CharField(max_length=12)
    npass = models.IntegerField()
    timeStamp = models.DateTimeField()
    startBlock = models.IntegerField()
    endBlock = models.IntegerField()
    startFeet = models.IntegerField()
    endFeet = models.IntegerField()
    # needed for any model with geom so that we can
    # do geom filters etc
    objects = models.GeoManager() # so we can use spatial queryset methods

    def __unicode__(self):
        return str(self.satellite)

    class Meta:
        db_table='segmentcommon'
        verbose_name=_("Segment Common")
        verbose_name_plural=_("Segment Common")

###############################################################################

class Scene(models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    sensor = models.ForeignKey(Sensor)
    source = models.CharField(max_length=255)
    sourceId = models.CharField(max_length=255)
    aquisitionDate = models.DateTimeField('aquisition date')
    imagePosition = models.PointField(srid=4326)
    objects = models.GeoManager() # so we can use spatial queryset methods

    def __unicode__(self):
        return self.source_id

    class Meta:
        db_table='model'
        verbose_name=_("Model")
        verbose_name_plural=_("Models")

###############################################################################

class AuxFile (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    fileType= models.ForeignKey(FileType)
    segmentCommon = models.ForeignKey(SegmentCommon)
    fileName = models.CharField(max_length=64)
    superType = models.IntegerField()
    fileDescription = models.CharField(max_length=64)
    insertionDate = models.FloatField()
    visible = models.BooleanField()
    #file blob  ,

    def __unicode__(self):
        return str(self.id) + "(original id: " + str(self.original_id) + ") " + self.fileDescription

    class Meta:
        db_table='auxfile'
        verbose_name=_("Aux File")
        verbose_name_plural=_("Aux Files")


###############################################################################

class SpotSegment (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    segmentNumber = models.IntegerField( db_index=True )
    hrvNum = models.IntegerField( null=True, blank=True )
    mode = models.CharField(max_length=2, null=True, blank=True )
    channel = models.IntegerField( null=True, blank=True )
    gain = models.CharField(max_length=4, null=True, blank=True )
    begTimeCod = models.FloatField( null=True, blank=True )
    endTimeCod = models.FloatField( null=True, blank=True )
    begFormat = models.IntegerField( null=True, blank=True )
    endFormat = models.IntegerField( null=True, blank=True )
    qualityFactor = models.IntegerField( null=True, blank=True )
    lookingAngle = models.FloatField( null=True, blank=True )
    firstValidFc = models.IntegerField( null=True, blank=True )
    lastValidFc = models.IntegerField( null=True, blank=True )
    missingLinesFlag = models.NullBooleanField( null=True, blank=True )
    hrvConf = models.IntegerField( null=True, blank=True )
    mirrorStep = models.IntegerField( null=True, blank=True )
    triodeQfactor = models.IntegerField( null=True, blank=True )

    def __unicode__(self):
        return str(self.segmentNumber)

    class Meta:
        db_table='spotsegment'
        verbose_name=_("Spot Segment")
        verbose_name_plural=_("Spot Segments")

###############################################################################

class LandsatSegment (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    segmentOrder = models.IntegerField()
    begTimeCode = models.FloatField()
    endTimeCode = models.FloatField()
    firstFrameFc = models.IntegerField()
    lastFrameFc = models.IntegerField()
    ellipsoid = models.CharField(max_length=8)
    ellipsParam1 = models.FloatField()
    ellipsParam2 = models.FloatField()
    ellipsParam3 = models.FloatField()
    ellipsParam4 = models.FloatField()
    channel = models.IntegerField()
    metaVersionNo = models.IntegerField()
    bandPresent = models.CharField(max_length=15)

    def __unicode__(self):
        return str(self.segmentOrder)

    class Meta:
        db_table='landsatsegment'
        verbose_name=_("Landsat Segment")
        verbose_name_plural=_("Landsat Segments")

###############################################################################

class ErsSegment (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    segmentOrder = models.IntegerField()
    rollAngle = models.IntegerField()
    begTimeCode = models.FloatField()
    endTimeCode = models.FloatField()
    begFormat = models.IntegerField()
    endFormat = models.IntegerField()
    icuOnboardBegTime = models.IntegerField()
    icuOnboardEndTime = models.IntegerField()
    compressionMode = models.ForeignKey(ErsCompMode)
    firstFrameNum = models.IntegerField()
    lastFrameNum = models.IntegerField()
    pulseRepInt = models.FloatField()
    simpleRate = models.FloatField()
    calibSubAtt = models.IntegerField()
    receivGain = models.IntegerField()
    ellipsoid = models.ForeignKey(EllipsoidType)
    ellipsParam1 = models.FloatField()
    ellipsParam2 = models.FloatField()
    ellipsParam3 = models.FloatField()
    ellipsParam4 = models.FloatField()
    padFirstFrame = models.IntegerField()
    padLastFrame = models.IntegerField()

    def __unicode__(self):
        return str(self.segmentOrder)

    class Meta:
        db_table='erssegment'
        verbose_name=_("Ers Segment ")
        verbose_name_plural=_("Ers Segments")

###############################################################################

class NoaaSegment (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    dataMode = models.ForeignKey(DataMode)
    eqcrxTime = models.FloatField()
    eqLon = models.FloatField()
    procLevel = models.CharField(max_length=2)
    bandMode = models.CharField(max_length=7)
    pixFormat = models.IntegerField()
    arcCenter = models.CharField(max_length=5)

    def __unicode__(self):
        return str(self.segmentOrder)

    class Meta:
        db_table='noaasegment'
        verbose_name=_("Noaa Segment")
        verbose_name_plural=_("Noaa Segments")

###############################################################################

class OrbviewSegment (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    dataMode = models.ForeignKey(DataMode)
    eqcrxTime = models.FloatField()
    eqLon = models.FloatField()
    procLevel = models.CharField(max_length=2)
    bandMod = models.CharField(max_length=7)
    pixFormat = models.IntegerField()
    arcCenter = models.CharField(max_length=5)

    def __unicode__(self):
        return str(self.segmentOrder)

    class Meta:
        db_table='orbviewsegment'
        verbose_name=_("Orbview Segment")
        verbose_name_plural=_("Orbview Segments")

###############################################################################

class FrameCommon (models.Model):
    """
      Note that the framecommon has no primary key - it is a join table
      between localization and segment.
    """
    localization = models.ForeignKey(Localization)
    segment = models.ForeignKey(SegmentCommon)
    cloud = models.CharField(max_length=8)
    cloudMean = models.IntegerField()
    trackOrbit = models.IntegerField()
    frame = models.IntegerField()
    ordinal = models.IntegerField()
    llLat = models.FloatField()
    urLon = models.FloatField()
    urLat = models.FloatField()
    ulLon = models.FloatField()
    ulLat = models.FloatField()
    llLon = models.FloatField()
    lrLat = models.FloatField()
    lrLon = models.FloatField()
    processable = models.BooleanField(default = True)
    beginTimeCod = models.FloatField()
    endTimeCod = models.FloatField()

    def __unicode__(self):
        return str(self.segment)

    class Meta:
        db_table='framecommon'
        verbose_name=_("Frame Common")
        verbose_name_plural=_("Frame Common")

###############################################################################

class SpotFrame (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    localization = models.ForeignKey(Localization)
    segmentCommon = models.ForeignKey(SegmentCommon)
    begFormat = models.PositiveIntegerField()
    endFormat = models.IntegerField()
    firstValidFc = models.IntegerField()
    lastValidFc = models.IntegerField()
    dummySceneFlag = models.BooleanField()
    missLines = models.IntegerField()
    satMinVal = models.IntegerField()
    satMaxVal = models.IntegerField()
    centerTimeCod = models.FloatField()
    scLat = models.FloatField()
    scLon = models.FloatField()
    scDevLat = models.FloatField()
    scDevLon = models.FloatField()
    incidence = models.FloatField()
    orientation = models.FloatField()
    sunAz = models.FloatField()
    sunEl = models.FloatField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='spotframe'
        verbose_name=_("Spot Frame")
        verbose_name_plural=_("SpotFrames")

###############################################################################

class LandsatFrame (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    localization = models.ForeignKey(Localization)
    segmentCommon = models.ForeignKey(SegmentCommon)
    centreLat = models.FloatField()
    centreLon = models.FloatField()
    centreTime = models.FloatField()
    sunAz = models.FloatField()
    sunElev = models.FloatField()
    fopScene = models.CharField(max_length=1)
    hdShift = models.IntegerField()
    sQuality = models.IntegerField()
    sbPresent = models.CharField(max_length=15)
    bGain = models.CharField(max_length=15)
    bgChange = models.CharField(max_length=15)
    bslgainchange = models.CharField(max_length=30)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='landsatframe'
        verbose_name=_("Landsat Frame")
        verbose_name_plural=_("Landsat Frames")

###############################################################################

class ErsFrame (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    localization = models.ForeignKey(Localization)
    segmentCommon = models.ForeignKey(SegmentCommon)
    frame = models.IntegerField()
    meanI = models.FloatField()
    meanQ = models.FloatField()
    sdevI = models.FloatField()
    sdevQ = models.FloatField()
    missLinPerc = models.FloatField()
    dopplerCentroid = models.FloatField()
    blockNumber = models.IntegerField()
    lineNumber = models.IntegerField()
    maxI = models.IntegerField()
    maxQ = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='ersframe'
        verbose_name=_("ErsFrame")
        verbose_name_plural=_("ErsFrames")

###############################################################################

class NoaaFrame (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    localization = models.ForeignKey(Localization)
    segmentCommon = models.ForeignKey(SegmentCommon)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='noaaframe'
        verbose_name=_("Noaa Frame")
        verbose_name_plural=_("Noaa Frames")

###############################################################################

class OrbviewFrame (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    localization = models.ForeignKey(Localization)
    segmentCommon = models.ForeignKey(SegmentCommon)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='orbviewframe'
        verbose_name=_("Orbview Frame")
        verbose_name_plural=_("OrbviewFrames")

###############################################################################

class OtherFrame (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    localization = models.ForeignKey(Localization)
    segmentCommon = models.ForeignKey(SegmentCommon)
    dataMode = models.ForeignKey(DataMode)
    eqCrxTime = models.FloatField()
    eqLon = models.FloatField()
    procLevel = models.CharField(max_length=2)
    bandNumber = models.CharField(max_length=7)
    pixFormat = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='otherframe'
        verbose_name=_("Other Frame")
        verbose_name_plural=_("Other Frames")

###############################################################################

class ErsCalNoise (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    begNoise1 = models.IntegerField()
    begNoise2 = models.IntegerField()
    endNoise1 = models.IntegerField()
    endNoise2 = models.IntegerField()
    begCalib1 = models.IntegerField()
    begCalib2 = models.IntegerField()
    endCalib1 = models.IntegerField()
    endCalib2 = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='erscalnoise'
        verbose_name=_("Ers Calibration Noise")
        verbose_name_plural=_("Ers Calibration Noise")

###############################################################################

class ErsDopCent (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    ordinal = models.IntegerField()
    value = models.FloatField()
    format = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='ersdopcent'
        verbose_name=_("Ers Doppler Center")
        verbose_name_plural=_("Ers Doppler Centers")

###############################################################################

class ErsQuality (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    numberofmlines = models.IntegerField()
    overallquality = models.IntegerField()
    qualitydensity = models.IntegerField()
    missingLines = models.CharField(max_length=513)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='ersquality'
        verbose_name=_("Ers Quality")
        verbose_name_plural=_("Ers Quality")

###############################################################################

class ErsSampTime (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    ordinal = models.IntegerField()
    value = models.FloatField()
    format = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='erssamptime'
        verbose_name=_("Ers Sample Time")
        verbose_name_plural=_("Ers Sample Times")

###############################################################################

class ErsStateVector (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    segmentCommon = models.ForeignKey(SegmentCommon)
    svtype = models.IntegerField()
    posX = models.FloatField()
    posY = models.FloatField()
    posZ = models.FloatField()
    velX = models.FloatField()
    velY = models.FloatField()
    velZ = models.FloatField()
    ascNodeJdt = models.FloatField()
    referenceJdt = models.FloatField()
    binaryTime = models.IntegerField()
    clockStepLength = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table='ersstatevector'
        verbose_name=_("Ers State Vector")
        verbose_name_plural=_("Ers State Vectors")

###############################################################################

class SatRelation (models.Model):
    original_id = models.IntegerField(db_index=True,unique=True)
    satellite = models.ForeignKey(Satellite)
    mission = models.IntegerField()
    sensor = models.ForeignKey(Sensor)

    def __unicode(self):
        return str(self.id)

    class Meta:
        db_table='satrelation'
        verbose_name=_("Satellite Relation")
        verbose_name_plural=_("Satellite Relations")

###############################################################################

class AcsFrame(models.Model):
    """This is a *special*, *read-only* model intended to
    be used as the basis for performing searches against
    vw_acs_frame on the backend database. This model is not
    managed, meaning that no table will be created on the
    backend database when running syncdb. To create the
    view associated with this model, run the create_views.sh
    script in the top level of the sac_catalogue source dir."""
    id = models.IntegerField( primary_key=True )
    frame_geometry = models.PolygonField(srid=4326, null=False, blank=False,
        help_text='Footprint for the scene.')
    segment_id = models.IntegerField()
    segment_geometry = models.PolygonField(srid=4326, null=False, blank=False,
        help_text='Footprint for the segment.')
    frame_number = models.IntegerField()
    time = models.DateTimeField()
    cloud_mean = models.IntegerField()
    frame = models.IntegerField() #J
    trackOrbit = models.IntegerField() #K
    sensor_name = models.CharField(max_length=64)
    sensor_id = models.IntegerField()
    satellite_name = models.CharField(max_length=64)
    satellite_id = models.IntegerField()
    filename = models.CharField(max_length=64)
    objects = models.GeoManager()

    def __unicode(self):
        return str(self.id)

    class Meta:
        db_table = u'vw_acs_frame'
        #requires django 1.1
        #managed = False
