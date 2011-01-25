exi/*

  Copyright 1995-2002, Advanced Computer Systems , Inc.
  Via Della Bufalotta, 378 - 00139 Roma - Italy
  http://www.acsys.it

  All Rights Reserved.

  This is UNPUBLISHED PROPRIETARY SOURCE CODE of Advanced Computer Systems;
  the contents of this file may not be disclosed to third parties, copied or
  duplicated in any form, in whole or in part, without the prior written
  permission of Advanced Computer Systems, Inc.

  $Prod: A.C.S. quick look library $

  $Id: libql.h,v 1.8 2007/11/22 14:15:47 aleber Exp $

  $Author: aleber $

  $Log: libql.h,v $
  Revision 1.8  2007/11/22 14:15:47  aleber
  further DEFINES from LandAuxMetadata.h added
  
  Revision 1.7  2007/11/14 17:21:09  aleber
  structure AUXILIARY_LANDSAT used to read file CluodAux for Landsat 7 ETM added
  
  Revision 1.6  2007/07/06 10:35:50  marpas
  C++style comments changed in C-Style
  
  Revision 1.5  2007/07/06 10:33:42  marpas
  define guarded
  
  Revision 1.4  2007/07/06 10:31:19  marpas
  header fixed
  
  Revision 1.3  2006/12/06 09:27:04  lucio.pulvirenti
  MAGIC_QLCLOUDCOVER_FILE define moved from opsMagic.h file
  
  Revision 1.2  2006/11/16 14:16:37  lucio.pulvirenti
  Structures moved from Quick_Look.h
  
  Revision 1.1  2006/11/15 10:44:40  enrcar
  file libql.h moved from libql to sgiDTIncludes
  
  Revision 1.4  2004/08/06 09:45:05  achval
  remove small bugs
  
  Revision 1.3  2004/08/04 15:31:47  achval
  added same feature for envisat satellite
  
  Revision 1.2  2004/06/18 17:25:10  serfol
  adding Endian flag to compile automaticcaly reading flag from system
  
  Revision 1.1.1.1  2004/01/07 16:10:00  envisat
  import libql
  
 
*/

#include <endian.h>

#if __BYTE_ORDER == __LITTLE_ENDIAN
#ifndef _BL_ENDiAN_
# define _BL_ENDiAN_
#endif
#endif  
    
#ifndef __LIBQL_H__
#define __LIBQL_H__

#define QL_DEBUG

#ifndef MI_SERVBUILD

#undef MI_TPRINTF
#undef MI_TFLAG
#undef MI_DPRINTF
#undef DPRINTF

#define MI_TPRINTF printf
#ifdef QL_DEBUG
#define MI_TFLAG(flag, lev) 1 
#else
#define MI_TFLAG(flag, lev) 0
#endif
#define MI_DPRINTF(flag, level, args) if (MI_TFLAG(flag, level)) MI_TPRINTF args ; if (MI_TFLAG(flag, level)) MI_TPRINTF(" line : %d\n",__LINE__)
#define DPRINTF  MI_DPRINTF  

#endif 

/*
 * local macros
 */
#ifndef min
#define min(a, b) ( (a)<(b) ? (a) : (b))
#endif
#ifndef max
#define max(a, b) ( (a)>(b) ? (a) : (b))
#endif
#ifndef DEFAULT_QL_BAND
#define DEFAULT_QL_BAND  -1
#endif
/*
 * provided constants, macros and structures
 */
#ifndef MAGIC_QLMSS_FILE_JPEG
#define MAGIC_QLMSS_FILE_JPEG       0x00003025 /* 12325 */
#endif
#ifndef MAGIC_QLTM_FILE_JPEG
#define MAGIC_QLTM_FILE_JPEG        0x00003026 /*  12326 */
#endif
#ifndef MAGIC_QLETM_FILE_JPEG
#define MAGIC_QLETM_FILE_JPEG       0x00003027 /* 12327 decimal */
#endif
#ifndef MAGIC_QLSWIR_FILE_JPEG
#define MAGIC_QLSWIR_FILE_JPEG      0x00002013 /* 8211 decimal */
#endif
#ifndef MAGIC_QLVNIR_FILE_JPEG
#define MAGIC_QLVNIR_FILE_JPEG      0x00002014 /* 8212 decimal */
#endif
#ifndef MAGIC_QLIQL_FILE_JPEG
#define MAGIC_QLIQL_FILE_JPEG       0x034A7AFB  /* IQL_Magic_Number  55212795*/
#endif
#ifndef MAGIC_QLSPOT_FILE_JPEG
#define MAGIC_QLSPOT_FILE_JPEG      0x034A7AFA  /* SPOT_Magic_Number 55212794*/
#endif
#ifndef MAGIC_QLERS_FILE_JPEG
#define MAGIC_QLERS_FILE_JPEG       0x034A7AF9  /* ERS_Magic_Number  55212793 */
#endif
#ifndef MAGIC_QLSPOT_NEW_FILE_JPEG
#define MAGIC_QLSPOT_NEW_FILE_JPEG      0x034A7AFF  /* SPOT_Magic_Number 55212799*/
#endif

#ifndef MAGIC_QLENVISAT_FILE_JPEG
#define MAGIC_QLENVISAT_FILE_JPEG       0x034A7AF8  /* ENVISAT_Magic_Number  55212792 */
#endif

/*
 * LP imported from opsMagic.h
 */
#define  MAGIC_QLCLOUDCOVER_FILE        0x00002012
/*
 * video format
 */
#ifndef BW 
#define BW  1 /* Quick Look BW Video Format  */
#endif
#ifndef RGB
#define RGB 3 /* Quick Look RGB Video Format */
#endif

/*
 * conversion constants
 */
#ifndef qlMSECSINADAY
#define  qlMSECSINADAY 86400000
#endif

enum { /* internale satellite id number
  * they should be aligned(32) with 
  * data code fom db
  */
    qlLANDSAT = 1, 
    qlJERS = 3, 
    qlSPOT = 4, 
    qlERS = 5, 
    qlENVISAT = 6,
    qlIQL = 14
};

/*
 * November 2007 - AB imported from LandAuxMetadata.h
 */

/* fill value for unvoted frame quarter */
#define FILLCLOUDVOTE  '*'
#define RANKFORFILLVOTE 9

/* values for field FULL_OR_PARTIAL_SCENE */
#define SCENEPARTIAL  'P'
#define SCENEFULL    'F'

/* values for field SCENE_BAND(x)_PRESENT */
#define BANDPRESENT  'Y'
#define BANDMISSING  'N'
#define BANDUNKNOWN  'U'

/* values for field BAND(x)_GAIN */
#define GAINLOW  'L'
#define GAINHIGH  'H'
#define GAINUNKNOWN  'U'

/* values for field BAND(x)_GAIN_CHANGE */
#define NOCHANGE  '0'    /* atoi(NOCHANGE) is used as nochange value in BAND(x)_SL_GAIN_CHANGE */
#define LOWTOHIGH  '+'
#define HIGHTOLOW  '-'

/*
 * November 2007 - AB imported from LandAuxMetadata.hh - Structure used  to read CloudAux file for Landsat 7 ETM
 */

#ifndef AUXILIARY_LANDSAT
typedef struct {            

  /* ** VERSION NUMBER OF METADATA (they could be updated) ***/
  char            MetadataVersionNo;        /* 1      - FIELD: FILE_VERSION_NO        */
  char            AlignSpare1[1];        /* 1      - int (and short int) align spare */
     
  /* ** Ground Station Identification Fields ***/
  unsigned short      Station_ID;         /* 2      - Receiving station id        */
  
  /* ** Orbit And Acquisitiation Identification Fields ***/
  int            Track_Number;        /* 4      - Track            */
  int            Orbit_Number;        /* 4      - Number of orbit          */
  int            Number_of_Frames;        /* 4      - number of frames          */
  int            First_Frame;        /* 4      - number of the first frame       */

  /* ** FORMAT(1 and 2) DEPENDING DATA ***/
   
  char        BandPresent[15];        /* 15   - FIELD: BAND(x)_PRESENT         */

  /* ** SCENE DEPENDING DATA ***/
   
  char        FullOrPartialScene[36];     /* 36   - FIELD: FULL_OR_PARTIAL_SCENE        */
  char        SceneBandPresent[36][15];     /* 540  - FIELD: SCENE_BAND(x)_PRESENT        */
  char        AlignSpare2[1];       /* 1      - int align spare                  */

  signed int       HorizontalDisplayShift[36];    /* 36*4 - FIELD: HORIZONTAL_DISPLAY_SHIFT        */
  char        BandGain[36][15];       /* 540  - FIELD: BAND(x)_GAIN          */
  char        BandGainChange[36][15];     /* 540  - FIELD: BAND(x)_GAIN_CHANGE         */
  unsigned short int  BandSLGainChange[36][15];     /* 540*2 - FIELD: BAND(x)_SL_GAIN_CHANGE        */
  signed short int    SceneQuality[36];             /* 36*2     - FIELD: SCENE_QUALITY        */
  
  /* ** SPARE DATA ***/
   
  char        AuxLandsatSpare[1024];     /* 1024         - spare                     */
  
} AUXILIARY_LANDSAT;   /* total 4012 bytes */
#endif

/*
 * Landsat QL header and stuff
 */
 
#ifndef qlLANDSAT_HDR

    typedef struct {
  4 unsigned int File_Key;              /* This Key is Used to Recognize the Quick Look RGB Files */
  2 unsigned short Satellite_ID;        /* Satellite Identification Flag */
  2 unsigned short Mission_ID;          /* Mission Identification Number */
  2 unsigned short Instrument_Type_ID;  /* Instrument Type Identification Flag */
  2 unsigned short Instrument_Number;   /* Instrument Number */
  2 unsigned short Station_ID;          /* Receiving Ground Station Identification Field */
  2 unsigned short Hddt_Number;         /* High Density Digital Tape Number */
  2 unsigned short Video_Format;        /* Format of the Video Data (BW/RGB) */
  2 unsigned short Lines_per_Jpeg_Block;/* Number of Compressed Lines per Jpeg Block */
  2 unsigned short Line_Size;           /* Length of the Quick Look Video Line for the Given Sensor */
  2 unsigned short Frame_Size;          /* Length of the Quick Look Frame fof the Given Sensor */
  2 unsigned short Spectral_Bands[3];   /* Selected Spectral Bands for Red, Green, Blue */
  2 unsigned short Compression_Flag;    /* Flag for Video Data Compression 0/1 true/false */
  4 int Track_Number;                   /* Track Number (if applicable) */
  4 int Orbit_Number;                   /* Orbit Number (if applicable)       */
  4 int Number_of_Frames;               /* Number of Acquisible Frames for the Present Track */
  4 int First_Frame;                    /* First Frame Realy Acquired */
  8 double QL_Line_Time __attribute__ ((aligned(8)));                /* Fly Time for Acquiring a Single Quick Look Line * 10000 */
  8 double QL_Ifov_X __attribute__ ((aligned(8)));                   /* Pixel Size in the X direction in radiants */
  8 double QL_Ifov_Y __attribute__ ((aligned(8)));                   /* Pixel Size in the Y direction in radiants */
  2 unsigned short QL_X_Offset;         /* Pointing offset in X direction of Quick Look */
  2 unsigned short Acquisition_Date[3]; /* Acquisition Date of the Satellite Pass in Year, Monts, Days */
  2 unsigned short Acquisition_Day;     /* Day in the Year of the Acquisition */ 
  2 unsigned short Acquisition_Start[4];/* Start of Acquisition in Hours, Min, Sec, Millisec */
  2 unsigned short Acquisition_End[4];  /* End of Acquisition in Hours, Min, Sec, Millisec */
  2 unsigned short Production_Date[3];  /* Production Date of the Satellite Pass in Days, Monts, Year */
  2 unsigned short Production_Start[3]; /* Start of Production in Hours, Minute, Seconds */
  2 unsigned short Production_End[3];   /* End of Production in Hours, Minute, Seconds */
  4 unsigned int Loaded_Lines;          /* Number of Lines Loaded on Disk */
  4 unsigned int Mission_Dependent[100];/* Fields for mission dependent data and contingenty */
    } qlLANDSAT_HDR  ; /* ex. Quick_Look_File_Description_Header; */
#endif
/* #ifndef Quick_Look_File_Description_Header   */ 
    typedef qlLANDSAT_HDR Quick_Look_File_Description_Header; /* for backward compatibility */
/* #endif */
#ifndef qlLANDSAT_JPGBD    

    typedef struct {
        8  double Satellite_Time __attribute__ ((aligned(8)));
        4  unsigned int Delta_Time;
        4  unsigned int Jpeg_Block_Size;
    } qlLANDSAT_JPGBD  ; /* ex. QL_Jpeg_Block_Descriptor;*/
#endif
/* #ifndef QL_Jpeg_Block_Descriptor   */
    
    typedef qlLANDSAT_JPGBD QL_Jpeg_Block_Descriptor; /* for backward compatibility */

/* #endif */
#ifndef qlLANDSAT_FTDCF   

    typedef struct  {
  long MagicNumber;      /* file magic number */
  long OrderNumber;      /* order number */
  long Station;          /* station identification field  */
  long Satellite;        /* satellite identification field */
  long Mission;          /* mission number */
  long Orbit;            /* orbit number */
  long Track;            /* track number */
  long Frame;            /* frame number */
  long WrsPath;          /* WRS path number */
  long UTM_Zone;         /* UTM zone number */
  long Center_Time[7];   /* GMT frame center time */
  double  datej __attribute__ ((aligned(8)));         /* Julian date of frame center time  */
  double GHA __attribute__ ((aligned(8)));            /* Greenwich Hour Angle */
  double Osculating[6] __attribute__ ((aligned(8)));  /* Keplerian Osculanting Elements */
  double Pos[3] __attribute__ ((aligned(8)));         /* Position vector */
  double Vel[3] __attribute__ ((aligned(8)));         /* Velocity vector */
  double Radius __attribute__ ((aligned(8)));         /* Satellite Orbit Radius */
  double Height __attribute__ ((aligned(8)));         /* Satellite Height at Center Frame  */
  double Heightdot __attribute__ ((aligned(8)));      /* Time derivative of S/C Height at Center Frame */
  double Latitude __attribute__ ((aligned(8)));       /* Frame Center Latitude */
  double Longitude __attribute__ ((aligned(8)));      /* Frame Center Longitude */
  double LatitudeDeg __attribute__ ((aligned(8)));    /* Frame Center Latitude */
  double LongitudeDeg __attribute__ ((aligned(8)));   /* Frame Center Longitude  */
  double Ant_Elevation __attribute__ ((aligned(8)));  /* Antenna Elevation at Center Frame */
  double Ant_Azimuth __attribute__ ((aligned(8)));    /* Antenna Azimuth at Center Frame */
  double Sun_Elevation __attribute__ ((aligned(8)));  /* Sun Elevation at Center Frame */
  double Sun_Azimuth __attribute__ ((aligned(8)));    /* Sun Azimuth at Center Frame */
  double Skew_Angle __attribute__ ((aligned(8)));     /* Skew Angle at Center Frame */
  double Tang_Skew __attribute__ ((aligned(8)));      /* Tangent of Skew Angle */
  double Skew_Angle_dot __attribute__ ((aligned(8))); /* Time derivative of Skew Angle */
  double Heading __attribute__ ((aligned(8)));        /* Satellite Heading [ Radians ] */
  double Velocity __attribute__ ((aligned(8)));       /* Nadir Satellite Velocity Km/Sec */
  double Velocity_Rate __attribute__ ((aligned(8)));  /* Velocity Change Rate Km/Sec/Sec */
  double UTM_Northing __attribute__ ((aligned(8)));   /* UTM Norting of Center Frame */
  double UTM_Easting __attribute__ ((aligned(8)));    /* UTM Easting of Center Frame */
  double theta __attribute__ ((aligned(8)));          /* Orientation to UTM grid */
  long DescendingFlag;   /* 1 = descending, 0 = ascending */
    } qlLANDSAT_FTDCF  ; /* ex. Ftdcf; */ 
#endif
#ifndef Ftdcf    
    
    typedef qlLANDSAT_FTDCF Ftdcf; /* for backward compatibility */
    
#endif
#ifndef qlIQL_HDR    

/*
 * IQL header and stuff
 */
    typedef struct  {
  long MagicNumber;              /* file magic number */
  int Video_Format;              /* Video Data format (BW/RGB) */
  int Line_Size;                 /* Length in pixels of the Quick Look Video Line */
  int Lines_Number;              /* Number of Lines of the original QL */
  int Lines_per_Jpeg_Block;      /* Number of Compressed Lines per Jpeg Block */
  int JPEG_BLock_Number;         /* Number of JPEG Blocks  */
  int Lines_per_Last_Jpeg_Block; /* Number of Compressed Lines for the last Jpeg Block */
  int Padding_at_segment_start;  /* Number of Black Lines from the QL beginning */
  int Padding_at_segment_end;    /* Number of Black Lines to the QL end */
  int Number_of_Frames;          /* Number of Acquisible Frames for the Present Track */
  int First_Frame;               /* First Frame Realy Acquired */
  double Acquisition_Start __attribute__ ((aligned(8))) ;      /* J-Date of acquisition */
  double QL_Line_Time __attribute__ ((aligned(8))) ;           /* Fly Time for Acquiring a Single Quick Look Line */
  float PixelSizeX;              /* Pixel Size in the X direction in meters */
  float PixelSizeY;              /* Pixel Size in the Y direction in meters */
    } qlIQL_HDR ; /* ex. IQL_Quick_Look_File_Description_Header;*/
    
#endif
#ifndef IQL_Quick_Look_File_Description_Header

    typedef qlIQL_HDR IQL_Quick_Look_File_Description_Header; /* for backward compatibility */

#endif
#ifndef qlIQL_JPGBD

    typedef struct {
  int Jpeg_Block_Start;
  int Jpeg_Block_Size;
    } qlIQL_JPGBD  ; /* ex. IQL_QL_Jpeg_Block_Descriptor;*/
    
#endif
#ifndef IQL_QL_Jpeg_Block_Descriptor

    typedef qlIQL_JPGBD IQL_QL_Jpeg_Block_Descriptor; /* for backward compatibility */

#endif
#ifndef qlIQL_FRAME

    typedef struct  {
  long                    Frame;      /* frame number      */
  long      StartLine;  /* start line of the frame (can be negative !) */
  long      EndLine;    /* end   line of the frame (can exceed Lines_Number !) */
    } qlIQL_FRAME  ; /* IQLFrame; */ 
    
#endif
#ifndef IQLFrame

    typedef qlIQL_FRAME IQLFrame; /* for backward compatibility */
    
#endif
#ifndef qlSPOT_HDR


/*
 * SPOT QL header and stuff
 */
    typedef struct  {
  long MagicNumber;              /* file magic number */
  int Video_Format;              /* Video Data format (BW/RGB) */
  int Line_Size;                 /* Length in pixels of the Quick Look Video Line */
  int Lines_Number;              /* Number of Lines of the original QL */
  int Lines_per_Jpeg_Block;      /* Number of Compressed Lines per Jpeg Block */
  int JPEG_BLock_Number;         /* Number of JPEG Blocks  */
  int Lines_per_Last_Jpeg_Block; /* Number of Compressed Lines for the last Jpeg Block */
  int Padding_at_segment_start;  /* Number of Black Lines from the QL beginning */
  int Padding_at_segment_end;    /* Number of Black Lines to the QL end */
  int Number_of_Frames;          /* Number of Acquisible Frames for the Present Track */
  int First_Frame;               /* First Frame Realy Acquired */
  double Acquisition_Start __attribute__ ((aligned(8)));      /* J-Date of acquisition */
  double QL_Line_Time __attribute__ ((aligned(8)));           /* Fly Time for Acquiring a Single Quick Look Line */
  float PixelSizeX;              /* Pixel Size in the X direction in meters */
  float PixelSizeY;              /* Pixel Size in the Y direction in meters */
    } qlSPOT_HDR  ; /* ex. SPOT_Quick_Look_File_Description_Header;*/
    
#endif
#ifndef SPOT_Quick_Look_File_Description_Header

    typedef qlSPOT_HDR SPOT_Quick_Look_File_Description_Header; /* for backward compatibility */
 
#endif
#ifndef qlSPOT_JPGBD

    typedef struct {
  int Jpeg_Block_Start;
  int Jpeg_Block_Size;
    } qlSPOT_JPGBD  ; /* ex. SPOT_QL_Jpeg_Block_Descriptor;*/
 
#endif
#ifndef SPOT_QL_Jpeg_Block_Descriptor
    
    typedef qlSPOT_JPGBD SPOT_QL_Jpeg_Block_Descriptor; /* for backward compatibility */
 
#endif
#ifndef qlSPOT_FTDCF

    typedef struct  {
  long Frame;             /* frame number */
  double CenterFrameTime __attribute__ ((aligned(8))) ; /* Julian Date frame center time */
    } qlSPOT_FTDCF  ; /* ex. SpotFtdcf; */ 
 
#endif
#ifndef SpotFtdcf
    
    typedef qlSPOT_FTDCF SpotFtdcf; /* for backward compatibility */
 
#endif
#ifndef qlERS_HDR

/*
 * ERS QL header and stuff
 */
    typedef struct 
    {
  long MagicNumber;              /* file magic number */
  int Video_Format;              /*  Video Data Format (BW/RGB) */
  int Line_Size;                 /* Length in pixels of the Quick Look Video Line */
  int Lines_Number;              /* Number of Lines of the original QL */
  int Lines_per_Jpeg_Block;      /* Number of Compressed Lines per Jpeg Block */
  int JPEG_BLock_Number;         /* Number of JPEG Blocks   */
  int Lines_per_Last_Jpeg_Block; /* Number of Compressed Lines for the last Jpeg Block */
  int Padding_at_segment_start;  /* Number of Black Lines from the QL beginning */
  int Padding_at_segment_end;    /* Number of Black Lines to the QL end */
  float PixelSizeX ;              /* Pixel Size in the X direction in meters */
  float PixelSizeY ;              /* Pixel Size in the Y direction in meters */
    } qlERS_HDR  ; /* ex. SAR_Quick_Look_File_Description_Header;*/
 
#endif
#ifndef SAR_Quick_Look_File_Description_Header

    typedef qlERS_HDR SAR_Quick_Look_File_Description_Header; /* for backward compatibility */
 
#endif
#ifndef qlERS_JPGBD

    typedef struct {
  int Jpeg_Block_Start;
  int Jpeg_Block_Size;
    } qlERS_JPGBD  ; /* ex. SAR_QL_Jpeg_Block_Descriptor;*/
 
#endif
#ifndef SAR_QL_Jpeg_Block_Descriptor

    typedef qlERS_JPGBD SAR_QL_Jpeg_Block_Descriptor; /* for backward compatibility */
 
#endif

#ifndef qlENVISAT_HDR

/*
 * ENVISAT QL header and stuff
 */
    typedef struct 
    {
  long MagicNumber;              /* file magic number */
  int Video_Format;              /*  Video Data Format (BW/RGB) */
  int Line_Size;                 /* Length in pixels of the Quick Look Video Line */
  int Lines_Number;              /* Number of Lines of the original QL */
  int Lines_per_Jpeg_Block;      /* Number of Compressed Lines per Jpeg Block */
  int JPEG_BLock_Number;         /* Number of JPEG Blocks   */
  int Lines_per_Last_Jpeg_Block; /* Number of Compressed Lines for the last Jpeg Block */
  int Padding_at_segment_start;  /* Number of Black Lines from the QL beginning */
  int Padding_at_segment_end;    /* Number of Black Lines to the QL end */
  float PixelSizeX ;              /* Pixel Size in the X direction in meters */
  float PixelSizeY ;              /* Pixel Size in the Y direction in meters */
    } qlENVISAT_HDR  ; /* ex. SAR_Quick_Look_File_Description_Header;*/
 
#endif

#ifndef qlENVISAT_JPGBD

    typedef struct {
  int Jpeg_Block_Start;
  int Jpeg_Block_Size;
    } qlENVISAT_JPGBD  ; /* ex. SAR_QL_Jpeg_Block_Descriptor;*/
 
#endif

#ifndef ql_JPGBD

    typedef struct {
  int Jpeg_Block_Start;
  int Jpeg_Block_Size;
    } ql_JPGBD  ; /* ex. SAR_QL_Jpeg_Block_Descriptor;*/
 
#endif
/*
 * common unified structure
 */
#ifndef qlHDR
typedef union {
    qlLANDSAT_HDR landsat;
    qlSPOT_HDR spot;
    qlIQL_HDR iql;
    qlERS_HDR ers;
    qlENVISAT_HDR envisat;
} qlHDR;
 
#endif
#ifndef qlJPGBD

typedef union {
    qlLANDSAT_JPGBD* landsat;
    qlSPOT_JPGBD* spot;
    qlIQL_JPGBD* iql;
    qlERS_JPGBD* ers;
    qlENVISAT_JPGBD* envisat;
} qlJPGBD;
 
#endif
#ifndef qlFTDCF

typedef union {
    qlLANDSAT_FTDCF* landsat;
    qlSPOT_FTDCF* spot;
    qlIQL_FRAME* iql;
} qlFTDCF;
 
#endif
#ifndef qlFirstFTDCF

typedef union {
    qlLANDSAT_FTDCF landsat;
    qlSPOT_FTDCF spot;
    qlIQL_FRAME iql;
} qlFirstFTDCF;
 
#endif
#ifndef qlJPEGBLOCK

typedef struct {
    long size;
    long addr;
} qlJPEGBLOCK;
 
#endif

#ifndef qlJPEGFRAME

typedef struct {
  long frame ;
    long line;
    long size;
} qlJPEGFRAME;
#endif

#ifndef qlJPEG

typedef struct {
    long satid;               /* satellite id number */
    long linesNumber;         /* ql jpeg decopressed number of lines  */
    long linesPerBlock;       /* lines per jpeg decompressed block */      
    long lineLostPixel;       /* line pixel offset for video */
    long lineSize;            /* decompressed line size */      
    long videoLineSize;       /* decompressed video line size */      
    long videoFormat;         /* video format BW/RGB */
    long numberOfBlocks;      /* number of jpeg compressed block */
    long numberOfWrittenFrames;/* number of frames stored onto the jpeg headers */
    long numberOfFrames;      /* real number of frames in the video data */
    long firstFrame;          /* first ql frame number */
    long lastFrame;           /* last ql frame number */
    long startSegmentPadding; /* black lines from the beginning */
    long endSegmentPadding;   /* black lines to the end */
    double acqTimeStart;      /* ql acquisition start time */
    double lineTime;          /* line acquisition time */
    qlJPEGBLOCK* block;       /* block descriptor array */
    qlJPEGFRAME* frame;       /* frame pointer array */
} qlJPEG;

#endif

#ifndef QLOOK

typedef struct {
    qlHDR hdr;
    qlJPGBD jpgbd;
    qlFTDCF ftdcf;
    qlFirstFTDCF firstFtdcf;
    qlJPEG jpeg;
#ifdef _DATABLADE_MODULE_
  MI_LO_FD  lo_fd ;
#else
  int      qlfp ;
#endif
  int   swap_rgb ;           /* (swap_rgb) ? swap : noswap ; */
} QLOOK;

#endif

#ifndef __IPC_STRCTURE__
#define __IPC_STRCTURE__

#define TCP_PORT  6666

typedef enum {

  BLOCK_INTERLEAVED,
  IMAGE_INTERLEAVED,
  MAX_TRANSFER_MODE

} TransferMode ;

typedef enum {
  
  RAW_IMAGE,
  JPEG_IMAGE,
      
  MAX_OUTPUT_IMAGE_FORMAT
} ImageOutputFormat ;
  
typedef enum {
  
  SRV_RESTART  = 989898,
  SRV_STOP
      
} ServerMessage ;
  
#define MAX_BLOCK_NUMBER  250  
typedef struct {

  int    in_n_block ;  
  char  *blocks[MAX_BLOCK_NUMBER] ;
  int    blocksDim[MAX_BLOCK_NUMBER] ;
} RGB_IMAGE ;


typedef struct {

/*/ image input value */
  unsigned int  in_width ;
  unsigned int  in_left_offset ;
  unsigned int  in_right_offset ;
  int        in_start_line ;
  unsigned int  in_n_lines ;
  unsigned int  in_n_block_lines ;
  unsigned int  in_n_block ;  /*/ for image */
  unsigned int  in_n_band ;    /*/ for image */
  unsigned int  in_n_image ;  /*/ number of input images */
  TransferMode  in_t_mode ;

  unsigned int  out_width ;
/*/ image output value */  
  ImageOutputFormat  out_format ;
  int        in_quality ;  /*/ jpeg compression factor */
  int        out_rgb_swap ;  /*/ (0) ? no swap : swap */
  int        out_auto_lut ;  /*/ (0) ? no lut : lut */
  int        getFrames ;    /*/ (1) ? frame get operation */
  
} WorkDescriptor ;

#define FrameFlagValue  1001
#define WorkOrderOK    "WorkOrderOK"
#define WorkOrderNOOK  "WorkOrderNOOK"
  
#define checkWorkDescriptor(wd)    (( \
    ((wd)->in_n_block > MAX_BLOCK_NUMBER || (wd)->in_n_block == 0) || \
    ((wd)->in_n_image != 1 && (wd)->in_n_image != 3) || \
    ((wd)->in_n_band  != 1 && (wd)->in_n_band  != 3) || \
    ((wd)->in_n_image == 3 && (wd)->in_n_image == 3) || \
    ((wd)->in_t_mode  != BLOCK_INTERLEAVED && (wd)->in_t_mode != IMAGE_INTERLEAVED) || \
    ((wd)->in_width      == 0) || \
    ((wd)->in_n_block_lines  == 0) || \
    ((wd)->in_n_lines    == 0) || \
    ((wd)->out_width    == 0) || \
    ((wd)->out_format != JPEG_IMAGE && (wd)->out_format != RAW_IMAGE)) ? -1 : 0 )



#endif /* __IPC_STRCTURE__ */
  
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    qlUtil.c                      _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
int videoBGR2RGB(
    unsigned char* inbuff,    /* input buffer */
    long sizex,      /* x size of image */
    long sizey      /* y size of image */
) ;

int resampling (
  char      *in_b,
  char      *out_b,
  unsigned int  in_size,
  unsigned int  out_size,
  unsigned int  in_w,
  unsigned int  out_w,
  int        top_o,
  int        but_o,
  unsigned int  left_o,
  unsigned int  right_o,
  unsigned int  videoformat
) ;

int setAutoLut(
  void* inbuff, 
  long xdim, 
  long ydim, 
  int videoformat
) ;

int saveJpegFile(

  char  *buffer,    /*/ IN : image buffer */
  int    sample,      /*/ IN : sample for pixel (1 or 3) */
  char  *filename,    /*/ IN : jpeg filename */
  int    quality,    /*/ IN : compression quality */
  int    width,      /*/ IN : image width */
  int    height      /*/ IN : image height */
              /*/ RET : error code */
) ;

int  getBlockBuffer(
  void  **out_buff,
  long  *out_size,
  WorkDescriptor  *wd,
  RGB_IMAGE  *images
) ;

int  getBuffer(
  void  **out_buff,
  long  *out_size,
  WorkDescriptor  *wd,
  RGB_IMAGE  *images
) ;

int  getJpegBuffer(
  void  **out_buff,
  long  *out_size,
  WorkDescriptor  *wd,
  RGB_IMAGE  *images
) ;

void resetImage(
    RGB_IMAGE  *images,
    int      n_image,
    int      n_block
) ;

int qlCompression(
  void      **out_buff,
  long      *out_size,
  unsigned int  in_size ,
  unsigned int  in_height,
  unsigned char   *in_buffer,
  unsigned int  in_width,
  unsigned int  sample,
  unsigned int  quality
) ;

int qlDecompression(
  void      **out_buff,
  long      *out_size,
  long      *out_width,
  long      *out_comp_sample,
  unsigned int  in_size ,
  unsigned char   *in_buffer,
  unsigned int  subsample
) ;

/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    loader.c                      _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
  
long  getBlockDecompBuffSize  (QLOOK *ql) ;
void  getLineBlocks      (QLOOK *ql, long sline, long nlines, long* sb, long* eb) ;


#ifdef _DATABLADE_MODULE_
int    blockRead        (void **buff, int *size, long n, QLOOK  *ql, MI_CONNECTION *connection) ;
#else
int    blockRead        (void **buff, int *size, long n, QLOOK  *ql) ;
#endif

int qlGetLines(  
  void  **outbuff,
  long  *outbuffsz,
  long  *ydim,
#ifdef _DATABLADE_MODULE_
  MI_CONNECTION  *connection,
#endif
  QLOOK  *ql,
  long  sl,
  long  nl,
  long  linesz,
  long  R,
  ImageOutputFormat  oformat,
  int    lut,
  int    quality
) ;

int qlGetBlocks(  
  void  **outbuff,
  long  *outbuffsz,
  long  *ydim,
#ifdef _DATABLADE_MODULE_
  MI_CONNECTION  *connection,
#endif
  QLOOK  *ql,
  long  sb,
  long  eb,
  long  linesz,
  long  R,
  ImageOutputFormat  oformat,
  int    lut,
  int    quality
) ;

int qlGetBlock(  
  void  **outbuff,
  long  *outbuffsz,
  long  *ydim,
  QLOOK  *ql,
  long  block,
  long  linesz,
  int    lut
) ;

int qlGetFrames(  
  void  **outbuff,
  long  *outbuffsz,
  long  *ydim,
#ifdef _DATABLADE_MODULE_
  MI_CONNECTION  *connection,
#endif
  QLOOK  *ql,
  long  sf,
  long  ef,
  long  linesz,
  long  R,
  ImageOutputFormat  oformat,
  int    lut,
  int    quality
) ;

int qlErsGetFrames(  
  void  **outbuff,
  long  *outbuffsz,
  long  *ydim,
#ifdef _DATABLADE_MODULE_
  MI_CONNECTION  *connection,
#endif
  QLOOK  *ql,
  long  startBlock,
  long  startLine,
  long  endBlock,
  long  endBlockStartLine,
  long  linesz,
  long  R,
  ImageOutputFormat  oformat,
  int    lut,
  int    quality
  
) ;

int qlEnvisatGetFrames(  
  void  **outbuff,
  long  *outbuffsz,
  long  *ydim,
#ifdef _DATABLADE_MODULE_
  MI_CONNECTION  *connection,
#endif
  QLOOK  *ql,
  long  totalFrames,
  long  firstFrame,
  long  lastFrame,
  long  linesz,
  long  R,
  ImageOutputFormat  oformat,
  int    lut,
  int    quality
  
) ;


/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    qlHeader.c _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/


void qlClose(
#ifdef _DATABLADE_MODULE_
  QLOOK  *ql
#else
  QLOOK  *ql
#endif
) ;

#ifdef _DATABLADE_MODULE_
mi_integer qlLoad(
  MI_CONNECTION  *connection,
  QLOOK  *ql
#else
int qlLoad(
  QLOOK  *ql  
#endif
) ;

void qlFree(
  void *buff
) ;

long getBlockHeight(long linesz, QLOOK  *ql) ;
/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    loaderSpot.c                  _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
void printHdr_SPOT(qlSPOT_HDR* hdr)  ;

double  JDATEtoMSECS      (double j) ;

#ifdef _DATABLADE_MODULE_
mi_integer  qlSpotLoad(
    MI_CONNECTION  *connection,
    QLOOK      *ql
) ;
#else
int qlSpotLoad(
    QLOOK      *ql
) ;
#endif

void qlSpotFree(
  QLOOK  *ql
) ;

/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    loaderLandsat.c                  _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
void printHdr_LANDSAT(qlLANDSAT_HDR* hdr)  ;

#ifdef _DATABLADE_MODULE_
int  qlLandsatLoad(
    MI_CONNECTION  *connection,
    QLOOK      *ql
) ;
#else
int qlLandsatLoad(
    QLOOK      *ql
) ;
#endif

void qlLandsatFree(
  QLOOK  *ql
) ;

/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    loaderIql.c                  _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
void printHdr_IQL(qlIQL_HDR* hdr)  ;

#ifdef _DATABLADE_MODULE_
int  qlIqlLoad(
MI_CONNECTION  *connection,
QLOOK      *ql
) ;
#else
int qlIqlLoad(
QLOOK      *ql
) ;
#endif

void qlIqlFree(
QLOOK  *ql
) ;



/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    loaderErs.c                   _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
void printHdr_ERS(qlERS_HDR* hdr) ;
#ifdef _DATABLADE_MODULE_
mi_integer  qlErsLoad(
MI_CONNECTION  *connection,
QLOOK      *ql
) ;
#else
int qlErsLoad(
    QLOOK      *ql
) ;
#endif

void qlErsFree(
  QLOOK  *ql
) ;


/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    loaderEnvisat.c                   _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
void printHdr_ENVISAT(qlENVISAT_HDR* hdr) ;
#ifdef _DATABLADE_MODULE_
mi_integer  qlEnvisatLoad(
MI_CONNECTION  *connection,
QLOOK      *ql
) ;
#else
int qlEnvisatLoad(
    QLOOK      *ql
) ;
#endif

void qlEnvisatFree(
  QLOOK  *ql
) ;

/*
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/    writer.c                   _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
*/
int writeQL (
  ql_JPGBD    *jpgdb,      /* IN/OUT: array of blocks dimension */
  int        NumOfBlocks,  /* num of block */
  char      *buffer,    /* input file buffer */
  int        Jpeg_file_descriptor,      /* file descriptor */
  int        offset,      /* start write point */
  int        LinesBlock,    /* line for block */
  int       Video_Format,  /* Video Data Format (BW/RGB) */
  int       Line_Size,    /* Length in pixels of the Quick Look Video Line */
  int       Lines_Number,  /* Number of Lines of the original QL */
  int       cFactor      /* compression factor (70 is a good value) */
) ;

int getNumOfBlocks(
  int        LinesBlock,    /* line for block */
  int       Lines_Number  /* Number of Lines of the original QL */
) ;


#ifdef __cplusplus
}
#endif /* __cplusplus */
#endif /* !__LIBQL_H__ */
