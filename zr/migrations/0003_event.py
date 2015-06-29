# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zr', '0002_post_is_removed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=3, choices=[(b'UKO', 'UKO'), (b'UAO', 'UAO'), (b'UDO', 'UDO'), (b'UST', 'UST'), (b'UWD', 'UWD'), (b'USD', 'USD'), (b'USK', 'USK'), (b'UFSA', 'UFSA'), (b'UFSD', 'UFSD'), (b'ULO', 'ULO'), (b'UDP', 'UDP'), (b'UPP', 'UPP'), (b'MI', 'MI'), (b'ZSZ', 'ZSZ'), (b'ZSL', 'ZSL'), (b'ZCA', 'ZCA'), (b'MPZPZ', 'MPZPZ'), (b'MPZPO', 'MPZPO'), (b'STUDZ', 'STUDZ'), (b'STUDO', 'STUDO'), (b'MPZS', 'MPZS'), (b'MPMA', 'MPMA'), (b'UDP', 'UDP'), (b'UDPA', 'UDPA'), (b'UDO', 'UDO'), (b'UDOA', 'UDOA'), (b'UDL', 'UDL'), (b'UDLA', 'UDLA'), (b'UFPP', 'UFPP'), (b'UFPO', 'UFPO'), (b'WWPO', 'WWPO'), (b'WOZM', 'WOZM'), (b'ZZOM', 'ZZOM'), (b'ZZSR', 'ZZSR'), (b'WAPM', 'WAPM'), (b'IOMP', 'IOMP'), (b'POM', 'POM'), (b'WFPP', 'WFPP')])),
                ('obj', models.CharField(max_length=128, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
