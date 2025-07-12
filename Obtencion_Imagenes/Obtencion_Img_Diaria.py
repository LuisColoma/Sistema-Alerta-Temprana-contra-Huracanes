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
import datetime
from datetime import datetime
#################################################################################

#startdate = datetime.date(2025,1,1) 
#enddate = datetime.date(2025,1,2)
#date = startdate

fecha_utc = datetime.utcnow().isoformat() + "Z"
fecha_formateada = fecha_utc[:10]


    
background_image_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
version=1.3.0&service=WMS&request=GetMap&\
format=image/jpeg&STYLE=default&bbox=-45,-90,0,-45&CRS=EPSG:4326&\
HEIGHT=512&WIDTH=512&TIME={0}&layers=MODIS_Terra_SurfaceReflectance_Bands143'.format(fecha_formateada)

GHRSST_overlay_image_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
version=1.3.0&service=WMS&request=GetMap&\
format=image/jpeg&STYLE=default&bbox=-45,-90,0,-45&CRS=EPSG:4326&\
HEIGHT=512&WIDTH=512&TIME={0}&layers=IMERG_Precipitation_Rate'.format(fecha_formateada)



##############################################################################   
background = plimg.open(urllib.request.urlopen(background_image_url))
overlay = plimg.open(urllib.request.urlopen(GHRSST_overlay_image_url))

background = background.convert("RGBA")
overlay = overlay.convert("RGBA")

# .75 is the transparency for this example
GHRSST_Overlay = plimg.blend(background, overlay, 0)
GHRSST_Overlay2 = plimg.blend(overlay, background, .63)

##############################################################################

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection = ccrs.Mercator.GOOGLE)
plt.imshow(GHRSST_Overlay, extent = (-10.4e6, -9.6e6, 1.4e6, 2.3e6), origin = 'upper')
ax.coastlines(color='blue', linewidth=1)
shp_file = '.\Bases de datos\gadm41_GTM_1.shp'  # Replace with your actual shapefile path
reader = shpreader.Reader(shp_file)
for geometry in reader.geometries():
    ax.add_geometries([geometry], crs=ccrs.PlateCarree(), edgecolor='blue', facecolor='none', linewidth=0.8)
##ax.gridlines()

# Guardar la figura como un archivo PNG... OJO con ruta de salida ....
output_path = os.path.join('/home/luis/proyect_p39/static/images', 'img_{0}.jpg'.format(fecha_formateada))  # Ruta de salida
fig.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)  # Guardar la imagen

##############################################################################
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection = ccrs.Mercator.GOOGLE)
plt.imshow(GHRSST_Overlay2, extent = (-10.4e6, -9.6e6, 1.4e6, 2.3e6), origin = 'upper')
ax.coastlines(color='white', linewidth=1)
shp_file = '.\Bases de datos\gadm41_GTM_1.shp'  # Replace with your actual shapefile path
reader = shpreader.Reader(shp_file)
for geometry in reader.geometries():
    ax.add_geometries([geometry], crs=ccrs.PlateCarree(), edgecolor='white', facecolor='none', linewidth=0.8)

# Guardar la figura como un archivo PNG... OJO con ruta de salida ....
output_path = os.path.join('/home/luis/proyect_p39/deteccion/Imagenes satelitales/Validate', 'img_{0}.jpg'.format(fecha_formateada))  # Ruta de salida
fig.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)  # Guardar la imagen
    