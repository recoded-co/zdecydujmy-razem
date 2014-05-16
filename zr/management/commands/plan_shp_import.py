__author__ = 'dwa'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.contrib.gis.gdal import DataSource
from zr.models import Subject, SubjectFeat, SubjectFeatProperty
import os



class Command(BaseCommand):
    args = '<a a ...>'
    help = 'Closes the specified poll for voting'

    def marcator_wkt_to_point(self, wkt):
        from django.contrib.gis.gdal import SpatialReference, CoordTransform
        from django.contrib.gis.geos import Point
        from django.contrib.gis.geos import fromstr
        from django.contrib.gis.geos import GEOSGeometry
        dst_coord = SpatialReference(4326)
        org_coord = SpatialReference(3857)
        trans = CoordTransform(org_coord, dst_coord)
        pnt = fromstr(wkt, srid=3857)
        pnt.transform(trans)
        return pnt

    def handle(self, *args, **options):
        self.stdout.write('Updating index...')

        if len(args) < 2:
            self.stdout.write('call plan_shp_import name path')
            return 1

        plan_name = args[0] # args[1] == plan name
        file_path = args[1] # args[2] == file path

        subject, created = Subject.objects.get_or_create(label=plan_name)
        shp_file = os.path.abspath(file_path)
        ds = DataSource(shp_file)

        for layer in ds:
            print 'layer start'
            print layer
            properties = layer.fields
            for feature in layer:
                print 'layer feature'
                print feature
                if feature.geom_type == 'Polygon':
                    print 'Polygon'
                    color = 'blue'
                    if 'color' in properties:
                        color = feature.get('color', 'blue')
                        del properties['color']

                    #sf = SubjectFeat(subject=subject, geom=self.marcator_wkt_to_point(feature.geom.wkt))
                    sf = SubjectFeat(subject=subject, geom=feature.geom.wkt, color=color)
                    sf.save()

                    for p in properties:
                        sfp = SubjectFeatProperty(feat=sf, key=p, value=feature.get(p))
                        sfp.save()
                else:
                    print 'NON POLYGON!'
        self.stdout.write('... done!')
