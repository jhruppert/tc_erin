GCIP/EOP Surface: Precipitation NCEP/CPC 4KM Gridded (Grib) Stage IV Data

   The Stage IV analysis is based on the multi-sensor hourly/6-hourly 'Stage III' analyses (on local 4km polar-stereographic grids) produced by the 12 River Forecast Centers (RFCs) in CONUS.  NCEP mosaics the Stage III into a national product (the Stage IV).  Hourly, 6-hourly and 24-hourly (accumulated from the 6-hourly) analyses are available.  The Stage IV differs from the NCEP Stage II chiefly in that the NCEP Stage II contains no manual quality control (QC), while the Stage IV benefits from manual QC performed on the Stage III data at the RFCs.                                                                         
   The Stage 4 data is a combination of observations and radar calculated reflectivity. Therefore the dataset combines the advantages of ground-truth provided by gauges with the spatially complete and high resolution radar data. On the other hand, it also becomes susceptible to the inaccuracies inherent to both radar or gauge data.

   Each River Forecast Center (RFC) has the ability to manually quality control the Multisensor Precipitation Estimates (MPE) precipitation data in its region of responsibility before it is sent to be included in the Stage IV mosaic. The precipitation values,however, are not intentionally modified downwards during snow events. Rather, due to inaccurate measuring of liquid equivalents at many gauge locations (e.g., a lack of the equipment to melt and measure the frozen precip), zero or very low values are reported at these locations. These "bad" gauge values then go into the MPE algorithm, resulting in liquid precip estimates that are too low during winter storms. There are also problems with zero or too low precipitation values at many RFC gauge locations even outside of heavy snowfall events.

   For specific questions about the MPE data, please contact the RFCs directly, such as the Mid-Atlantic River Forecast Center (marfc.webmaster@noaa.gov). 

   The format of the Stage IV analysis files is                                       
                                                                                  
      ST4.yyyymmddhh.xxh.Z                                                        
   'xx' (=01,06 or 24) is the accumulating length, and yyyymmddhh is the ending time of the accumulation period.                                    


   The Stage IV data are on the same 4km polar-stereographic (1121x881) NWS HRAP grid as the NCEP Stage II.        

The unit of precipitation reported is mm.  Additional documentation on the Stage II and Stage IV analysis can be found
at http://www.emc.ncep.noaa.gov/mmb/SREF/pcpanl/

   There are problems with the RFC precip data in the eastern U.S. during heavy snow events. While ASOS stations have the equipment to melt the snow and derive the liquid equivalent precip, the RFC stations in the East do not. So when there are big snowfall events such as the January 2016 blizzard, the snow accumulations get recorded, but the corresponding liquid equivalents often come in as zero or near zero amounts, which are incorrect.
