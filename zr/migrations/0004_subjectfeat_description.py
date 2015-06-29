# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0003_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectfeat',
            name='description',
            field=models.TextField(max_length=5000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
