import geopandas as gpd
from shapely.geometry import box
from shapely.validation import make_valid

from lib import convert_multipolygon_to_centroid, make_multipolygonal
from reduceGeoJSON import reduceGeoJSONFile


def prepare(input_file, code, output_folder):

    #load
    gdf = gpd.read_file(input_file)

    #TODO do other territories
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
    mmm = output_folder + code + "_" + terr
    gdf.to_file(mmm + '.gpkg', driver='GPKG')

    #save to points
    convert_multipolygon_to_centroid(mmm + '.gpkg', mmm + '_pt.gpkg')

    #gpkg to geojson
    gpd.read_file(mmm + '.gpkg').to_file(mmm + '.geojson', driver='GeoJSON')
    gpd.read_file(mmm + '_pt.gpkg').to_file(mmm + '_pt.geojson', driver='GeoJSON')





out = "/home/juju/geodata/elections_fr/out_units/"
#circonscriptions
#prepare('/home/juju/geodata/elections_fr/circonscriptions/insee/circonscriptions_legislatives_030522.gpkg', "circ", out)
#bureaux de vote
#prepare("/home/juju/geodata/elections_fr/bv/contours-france-entiere-latest-v2.gpkg", "bv", out)


#reduceGeoJSONFile(out+'bv_met_pt.geojson', 0, out+'bv_met_pt___.geojson')

