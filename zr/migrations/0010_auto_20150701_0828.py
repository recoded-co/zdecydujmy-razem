# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0009_auto_20150701_0818'),
    ]

    operations = [
        migrations.AlterField(
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
