from lib import convert_multipolygon_to_centroid

folder = "/home/juju/geodata/elections_fr/bv/"
convert_multipolygon_to_centroid(folder + "contours-france-entiere-latest-v2.gpkg", folder + "bv_pt.gpkg")
