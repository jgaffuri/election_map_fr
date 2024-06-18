import geopandas as gpd
from shapely.geometry import box

input_file = '/home/juju/geodata/elections_fr/circonscriptions/insee/circonscriptions_legislatives_030522.gpkg'

#load
gdf = gpd.read_file(input_file)

terr = "met"
epsg = "2154"
extent = box(90000, 6100000, 1130000, 7140000)

#change projection
gdf = gdf.to_crs("EPSG:"+epsg)

#clip
gdf = gdf.clip(extent)

#save
gdf.to_file(terr + '.geojson', driver='GeoJSON')
