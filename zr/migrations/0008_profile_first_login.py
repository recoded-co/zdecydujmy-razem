# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0007_auto_20150629_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_login',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
