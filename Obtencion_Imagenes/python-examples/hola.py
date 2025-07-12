import os
from io import BytesIO
from skimage import io
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import folium
import urllib.request
import urllib.parse
import mapbox_vector_tile
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
from PIL import Image as plimg
from PIL import ImageDraw
import numpy as np
import pandas as pd
from owslib.wms import WebMapService
from IPython.display import Image, display
import geopandas as gpd
from shapely.geometry import box
import urllib.request
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.plot import show
import fiona
from datetime import datetime, timedelta
import cartopy.io.shapereader as shpreader
from PIL import Image
#################################################################################



#proj3857 = 'https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?\
#version=1.3.0&service=WMS&\
#request=GetMap&format=image/png&STYLE=default&bbox=-8000000,-8000000,8000000,8000000&\
#CRS=EPSG:3857&HEIGHT=2048&WIDTH=2048&TIME=2002-12-01&layers=MODIS_Aqua_Cloud_Top_Pressure_Day'

# Request image.
#img=io.imread(proj3857)
#img = np.squeeze(img)


# Display image on map.
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1, projection = ccrs.Mercator.GOOGLE)
#plt.imshow(img, extent = (-10.4e6, -9.6e6, 1.4e6, 2.3e6), origin = 'upper')
#ax.coastlines(color='white', linewidth=1.5)

#shp_file = '.\Bases de datos\gadm41_GTM_1.shp'  # Replace with your actual shapefile path
#reader = shpreader.Reader(shp_file)

#for geometry in reader.geometries():
    #ax.add_geometries([geometry], crs=ccrs.PlateCarree(), edgecolor='white', facecolor='none', linewidth=0.7)


#ax.gridlines()
#plt.show()

#print('')


################################################################################################

import datetime

#startdate = datetime.date(2021,12,25)
#enddate = datetime.date(2022,1,1)

#outdir = os.path.join(os.getcwd(), "python-examples", "SurfaceReflectance_{}_to_{}".format(startdate,enddate))
#currentdate = startdate
#extents = (-10.4e6, -9.6e6, 1.4e6, 2.3e6)
# Create directory if it doesn't exist yet
#if not os.path.exists(outdir):
    #os.mkdir(outdir)

#while currentdate < enddate:
#    print("Downloading images for {}...".format(currentdate))

#    url = 'https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?\
#version=1.3.0&service=WMS&request=GetMap&\
#format=image/png&STYLE=default&bbox=-8000000,-8000000,8000000,8000000&CRS=EPSG:3857&\
#HEIGHT=2048&WIDTH=2048&TIME=2002-12-01&layers=MODIS_Aqua_Cloud_Top_Pressure_Day'
    
#    img_data = io.imread(url)
#    img_data = np.squeeze(img_data)

#    img_pil = Image.fromarray(img_data)

#    img_pil.save(os.path.join(outdir,'img_{0}_{1}.png'.format(currentdate, extents)))
 
#currentdate += datetime.timedelta(1)

#print("Number of images downloaded:", len(os.listdir(outdir)))

#########################

startdate = datetime.date(2023,10,20) 
enddate = datetime.date(2023,10,25)
date = startdate

while date < enddate:
    
    proj3857 = 'https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?\
version=1.3.0&service=WMS&\
request=GetMap&format=image/png&STYLE=default&bbox=-8000000,-8000000,8000000,8000000&\
CRS=EPSG:3857&HEIGHT=2048&WIDTH=2048&TIME={0}&layers=IMERG_Precipitation_Rate'.format(date)
    
    background_image_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
version=1.3.0&service=WMS&request=GetMap&\
format=image/jpeg&STYLE=default&bbox=-45,-90,0,-45&CRS=EPSG:4326&\
HEIGHT=512&WIDTH=512&TIME={0}&layers=MODIS_Terra_SurfaceReflectance_Bands143'.format(date)
    
    GHRSST_overlay_image_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
version=1.3.0&service=WMS&request=GetMap&\
format=image/jpeg&STYLE=default&bbox=-45,-90,0,-45&CRS=EPSG:4326&\
HEIGHT=512&WIDTH=512&TIME={0}&layers=IMERG_Precipitation_Rate'.format(date)
    
    GHRSST_overlay2_image_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
version=1.3.0&service=WMS&request=GetMap&\
format=image/jpeg&STYLE=default&bbox=-45,-90,0,-45&CRS=EPSG:4326&\
HEIGHT=512&WIDTH=512&TIME={0}&layers=AMSRU2_Wind_Speed_Day '.format(date)
 

##############################################################################   
    background = plimg.open(urllib.request.urlopen(background_image_url))
    overlay = plimg.open(urllib.request.urlopen(GHRSST_overlay_image_url))
    overlay2 = plimg.open(urllib.request.urlopen(GHRSST_overlay2_image_url))

    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    overlay2 = overlay2.convert("RGBA")

    # .75 is the transparency for this example
    GHRSST_Overlay = plimg.blend(background, overlay, .70)
    #GHRSST_Overlay2 = plimg.blend(background, overlay2, 0.65)
    #GHRSST_Overlay.save("GHRSST_Overlay.png","PNG")

##############################################################################

    # Request image.
    #img=io.imread(proj3857)
    #img = np.squeeze(img)

    # Display image on map.
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection = ccrs.Mercator.GOOGLE)
    plt.imshow(GHRSST_Overlay, extent = (-10.4e6, -9.6e6, 1.4e6, 2.3e6), origin = 'upper')
    ax.coastlines(color='white', linewidth=1.5)
    shp_file = '.\Bases de datos\gadm41_GTM_1.shp'  # Replace with your actual shapefile path
    reader = shpreader.Reader(shp_file)
    for geometry in reader.geometries():
        ax.add_geometries([geometry], crs=ccrs.PlateCarree(), edgecolor='white', facecolor='none', linewidth=0.7)
    ax.gridlines()
    # Guardar la figura como un archivo PNG
    output_path = os.path.join(os.getcwd(), 'img_{0}.png'.format(date))  # Ruta de salida
    fig.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)  # Guardar la imagen

    #plt.show()

    #print('')

    date += datetime.timedelta(1)
    