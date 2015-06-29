# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0005_auto_20150629_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='action',
            field=models.CharField(max_length=16, choices=[(b'UKO', 'UKO'), (b'UAO', 'UAO'), (b'UDO', 'UDO'), (b'UST', 'UST'), (b'UWD', 'UWD'), (b'USD', 'USD'), (b'USK', 'USK'), (b'UFSA', 'UFSA'), (b'UFSD', 'UFSD'), (b'ULO', 'ULO'), (b'UDP', 'UDP'), (b'UPP', 'UPP'), (b'MI', 'MI'), (b'ZSZ', 'ZSZ'), (b'ZSL', 'ZSL'), (b'ZCA', 'ZCA'), (b'MPZPZ', 'MPZPZ'), (b'MPZPO', 'MPZPO'), (b'STUDZ', 'STUDZ'), (b'STUDO', 'STUDO'), (b'MPZS', 'MPZS'), (b'MPMA', 'MPMA'), (b'UDP', 'UDP'), (b'UDPA', 'UDPA'), (b'UDO', 'UDO'), (b'UDOA', 'UDOA'), (b'UDL', 'UDL'), (b'UDLA', 'UDLA'), (b'UFPP', 'UFPP'), (b'UFPO', 'UFPO'), (b'WWPO', 'WWPO'), (b'WOZM', 'WOZM'), (b'ZZOM', 'ZZOM'), (b'ZZSR', 'ZZSR'), (b'WAPM', 'WAPM'), (b'IOMP', 'IOMP'), (b'POM', 'POM'), (b'WFPP', 'WFPP'), (b'DWDC', 'DWDC')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
