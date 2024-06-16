import fiona
from shapely.geometry import shape, mapping
from shapely.geometry import MultiPolygon, Polygon


def convert_multipolygon_to_centroid(input_gpkg, output_gpkg):
    with fiona.open(input_gpkg, layer=0) as source:
        schema = source.schema.copy()
        schema['geometry'] = 'Point'

        with fiona.open(output_gpkg, 'w', driver='GPKG', crs=source.crs, schema=schema) as out_gpkg:
            for feature in source:
                geom = shape(feature['geometry'])
                
                if isinstance(geom, MultiPolygon):
                    largest_polygon = max(geom.geoms, key=lambda a: a.area)
                elif isinstance(geom, Polygon):
                    largest_polygon = geom
                else:
                    print("Unexpected geometry type: " + feature['geometry']['type'])
                    continue

                centroid = largest_polygon.centroid
                
                new_feature = {
                    'type': 'Feature',
                    'geometry': mapping(centroid),
                    'properties': feature['properties']
                }
                
                out_gpkg.write(new_feature)


folder = "/home/juju/geodata/elections_fr/bv/"
convert_multipolygon_to_centroid(folder + "contours-france-entiere-latest-v2.gpkg", folder + "bv_pt.gpkg")
