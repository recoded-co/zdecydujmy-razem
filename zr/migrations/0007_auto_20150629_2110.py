# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0006_auto_20150629_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(null=True, verbose_name='Wiek', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Wykszta\u0142cenie', choices=[(b'podstawowe', 'Podstawowe'), (b'gimnazjalne', 'Gimnazjalne'), (b'zawodowe', 'Zasadnicze zawodowe'), (b'srednie', '\u015arednie'), (b'wyzsze', 'Wy\u017csze')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='P\u0142e\u0107', choices=[(b'k', 'Kobieta'), (b'm', 'M\u0119\u017cczyzna')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='gis_portals',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Czy korzysta Pan(i) z portali mapowych (np. Google Maps, OpenStreetMap, zumi.pl)?', choices=[(b'tak', 'Tak'), (b'nie', 'Nie')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='job',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Aktualnie wykonywane zaj\u0119cie', choices=[(b'uczen', 'Ucze\u0144'), (b'student', 'Student'), (b'administracja', 'Pracownik administracji publicznej'), (b'etat', 'Zatrudniony w prywatnej firmie'), (b'przedsiebiorca', 'Przedsi\u0119biorca/ w\u0142a\u015bciciel firmy'), (b'wolny', 'Wolny zaw\xf3d'), (b'emeryt', 'Emeryt/ rencista'), (b'bezrobotny', 'Nie pracuj\u0105cy'), (b'inne', 'Inne zaj\u0119cie')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='social_portals',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Czy korzysta Pan(i) z portali spo\u0142eczno\u015bciowych (np. Facebook, nk.pl)?', choices=[(b'tak', 'Tak'), (b'nie', 'Nie')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='source',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Sk\u0105d dowiedzia\u0142 si\u0119 Pan(i) o konsultacjach?', choices=[(b'media', 'Z medi\xf3w'), (b'ulotka_poczta', 'Z ulotki przes\u0142anej poczt\u0105'), (b'facebook', 'Z facebooka'), (b'ulotka_bezp', 'Z bezpo\u015brednio otrzymanej ulotki'), (b'znajomi', 'Od znajomych'), (b'inne', 'Z innego \u017ar\xf3d\u0142a')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(max_length=6, null=True, verbose_name='Kod pocztowy', blank=True),
            preserve_default=True,
        ),
    ]
