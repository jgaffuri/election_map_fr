import geopandas as gpd
from shapely.geometry import box
from shapely.geometry import mapping, shape
import json
from shapely.validation import make_valid


folder = "/home/juju/geodata/elections_fr/circonscriptions/insee/"
input_file = folder + 'circonscriptions_legislatives_030522.gpkg'

#load
gdf = gpd.read_file(input_file)

terr = "met"
epsg = "2154"
extent = box(90000, 6100000, 1130000, 7140000)


#change projection
gdf = gdf.to_crs("EPSG:"+epsg)

#make valid geometries
gdf['geometry'] = gdf['geometry'].apply(make_valid)

#clip
gdf = gdf.clip(extent)

#save
gdf.to_file(terr + '.geojson', driver='GeoJSON')






#apply rounding to each geometry in the GeoDataFrame
#gdf['geometry'] = gdf['geometry'].apply(lambda geom: round_coordinates(geom, precision=0))

'''
def round_coordinates(geom, precision=0):
    if geom.is_empty:
        return geom
    rounded_coords = json.loads(json.dumps(mapping(geom), rounding=precision))
    return shape(rounded_coords)
'''
