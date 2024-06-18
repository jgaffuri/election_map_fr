import geopandas as gpd
from shapely.geometry import box, Polygon, Point, LineString, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
from shapely.validation import make_valid

from lib import convert_multipolygon_to_centroid

#bureaux de vote
#folder = "/home/juju/geodata/elections_fr/bv/"
#convert_multipolygon_to_centroid(folder + "contours-france-entiere-latest-v2.gpkg", folder + "bv_pt.gpkg")

#circonscriptions
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
gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.buffer(0))
gdf['geometry'] = gdf['geometry'].apply(lambda geom: make_multipolygonal(geom))
gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.buffer(0))
#gdf['geometry'] = gdf['geometry'].apply(make_valid)

#clip
gdf = gdf.clip(extent)

#make valid geometries
gdf['geometry'] = gdf['geometry'].apply(make_valid)

#apply rounding to each geometry in the GeoDataFrame
#gdf['geometry'] = gdf['geometry'].apply(lambda geom: round_coordinates(geom, precision=0))
#gdf['geometry'] = gdf['geometry'].apply(lambda geom: make_multipolygonal(geom))
#make valid geometries
#gdf['geometry'] = gdf['geometry'].apply(make_valid)

#save
gdf.to_file(folder + terr + '.gpkg', driver='GPKG')

#save to points
convert_multipolygon_to_centroid(folder + terr + '.gpkg', folder + terr + '_pt.gpkg')

#gpkg to geojson
gpd.read_file(folder + terr + '.gpkg').to_file(folder + terr + '.geojson', driver='GeoJSON')
