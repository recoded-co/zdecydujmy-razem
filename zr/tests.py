from django.test import TestCase
from zr.models import Configuration, Plan
from django.contrib.gis.db.models.fields import PointField


class TestFixturesLoad(TestCase):

    fixtures = ['data.json']

    def test_fixture_plan_loaded(self):
        plansLen = len(Plan.objects.all())
        plan = Plan.objects.get(id=1)

        self.assertEqual(1, plansLen)
        self.assertEqual(plan.name, 'demo')
        self.assertEqual(plan.after_search_zoom, 16)
        self.assertEqual(plan.center, 'POINT (16.8900203681322338 52.3961602418916144)')
        self.assertEqual(plan.geocoding_scope, '')
        self.assertEqual(plan.zoom_level, 14)

    def test_fixtures_configuration_loaded(self):
        confLen = len(Configuration.objects.all())
        conf = Configuration.objects.get(id=1)
        plan = Plan.objects.get(id=1)

        self.assertEqual(1, confLen)
        self.assertEqual(conf.side, 'L')
        self.assertEqual(conf.max, 50)
        self.assertEqual(conf.min, 30)
        self.assertEqual(conf.default, 50)
        self.assertEqual(conf.plan, plan)
