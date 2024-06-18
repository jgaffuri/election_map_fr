from lib import convert_multipolygon_to_centroid
import geopandas as gpd

folder = "/home/juju/geodata/elections_fr/bv/"
convert_multipolygon_to_centroid(folder + "contours-france-entiere-latest-v2.gpkg", folder + "bv_pt.gpkg")

#gpkg to geojson
gpd.read_file(folder + "bv_pt.gpkg").to_file(folder + "bv_pt.geojson", driver='GeoJSON')
