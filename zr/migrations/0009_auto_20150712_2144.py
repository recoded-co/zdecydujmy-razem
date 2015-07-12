# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0008_profile_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='action',
            field=models.CharField(max_length=16, choices=[(b'UKO', 'UKO'), (b'UAO', 'UAO'), (b'UDO', 'UDO'), (b'UST', 'UST'), (b'UWD', 'UWD'), (b'USD', 'USD'), (b'USK', 'USK'), (b'UFSA', 'UFSA'), (b'UFSD', 'UFSD'), (b'ULO', 'ULO'), (b'UDP', 'UDP'), (b'UPP', 'UPP'), (b'MI', 'MI'), (b'ZSZ', 'ZSZ'), (b'ZSL', 'ZSL'), (b'ZCA', 'ZCA'), (b'MPZPZ', 'MPZPZ'), (b'MPZPO', 'MPZPO'), (b'STUDZ', 'STUDZ'), (b'STUDO', 'STUDO'), (b'MPZS', 'MPZS'), (b'MPMA', 'MPMA'), (b'UDP', 'UDP'), (b'UDPA', 'UDPA'), (b'UDO', 'UDO'), (b'UDOA', 'UDOA'), (b'UDL', 'UDL'), (b'UDLA', 'UDLA'), (b'UFPP', 'UFPP'), (b'UFPO', 'UFPO'), (b'WWPO', 'WWPO'), (b'WOZM', 'WOZM'), (b'ZZOM', 'ZZOM'), (b'ZZSR', 'ZZSR'), (b'WAPM', 'WAPM'), (b'IOMP', 'IOMP'), (b'POM', 'POM'), (b'WFPP', 'WFPP'), (b'DWDC', 'DWDC'), (b'PCD', 'PCD')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, max_length=63, null=True, verbose_name='Wykszta\u0142cenie', choices=[(b'podstawowe', 'Podstawowe'), (b'gimnazjalne', 'Gimnazjalne'), (b'zawodowe', 'Zasadnicze zawodowe'), (b'srednie', '\u015arednie'), (b'wyzsze', 'Wy\u017csze')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='source',
            field=models.CharField(default='inne', max_length=13, verbose_name='Sk\u0105d dowiedzia\u0142 si\u0119 Pan(i) o konsultacjach?', choices=[(b'media', 'Z medi\xf3w'), (b'ulotka_poczta', 'Z ulotki przes\u0142anej poczt\u0105'), (b'facebook', 'Z facebooka'), (b'ulotka_bezp', 'Z bezpo\u015brednio otrzymanej ulotki'), (b'znajomi', 'Od znajomych'), (b'inne', 'Z innego \u017ar\xf3d\u0142a')]),
            preserve_default=False,
        ),
    ]
