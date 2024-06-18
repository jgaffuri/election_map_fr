import geopandas as gpd
from shapely.geometry import box, Polygon, Point, LineString, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
from shapely.validation import make_valid

from lib import convert_multipolygon_to_centroid



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
