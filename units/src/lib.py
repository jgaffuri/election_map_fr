import fiona
from shapely.geometry import shape, mapping, Polygon, Point, LineString, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
from shapely.validation import make_valid



def convert_multipolygon_to_centroid(input_gpkg, output_gpkg):

    with fiona.open(input_gpkg, layer=0) as source:
        schema = source.schema.copy()
        schema['geometry'] = 'Point'

        new_features = []
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
            
            new_features.append(new_feature)

        with fiona.open(output_gpkg, 'w', driver='GPKG', crs=source.crs, schema=schema) as out:
            out.writerecords(new_features)







def make_polygonal(geom):
    if isinstance(geom, Polygon):
        return geom
    if isinstance(geom, MultiPolygon):
        return geom
    if isinstance(geom, GeometryCollection):
        ps = []
        for g in geom.geoms:
            if not isinstance(g, Polygon): continue
            if g.area == 0: continue
            ps.append(g)
        l = len(ps)
        if l == 0: return Polygon()
        if l == 1: return ps[0]
        return MultiPolygon(ps)
    return Polygon()



def make_multipolygonal(geom):
    if isinstance(geom, MultiPolygon):
        return geom
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    if isinstance(geom, GeometryCollection):
        ps = []
        for g in geom.geoms:
            if not isinstance(g, Polygon): continue
            if g.area == 0: continue
            ps.append(g)
        return MultiPolygon(ps)
    return MultiPolygon()





def round_coordinates(geom, precision=3):
    if isinstance(geom, Point):
        return Point(round(geom.x, precision), round(geom.y, precision))
    elif isinstance(geom, LineString):
        cs = []
        for c in geom.coords:
            x, y = c
            cs.append((round(x, precision), round(y, precision)))
        return make_valid(LineString(cs))
    elif isinstance(geom, Polygon):
        exterior_ring = round_coordinates(geom.exterior, precision)
        if isinstance(exterior_ring, Point): return exterior_ring
        if Polygon(exterior_ring).area == 0: return exterior_ring
        interior_rings = []
        for ir in geom.interiors:
            ir = round_coordinates(ir, precision)
            if isinstance(ir, Point): continue
            if Polygon(ir).area == 0: continue
            interior_rings.append(ir)
        return make_valid(Polygon(exterior_ring, interior_rings))
    elif isinstance(geom, (MultiPoint, MultiLineString, MultiPolygon, GeometryCollection)):
        ps = [ round_coordinates(p, precision) for p in geom.geoms ]
        return make_valid(GeometryCollection(ps))

    print("unsupported geometry type: " + geom.geom_type)
    return geom

