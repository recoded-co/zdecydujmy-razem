# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zr', '0009_auto_20150712_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='Aktualnie wykonywane zaj\u0119cie', choices=[(b'uczen', 'Ucze\u0144'), (b'student', 'Student'), (b'administracja', 'Pracownik administracji publicznej'), (b'etat', 'Zatrudniony w prywatnej firmie'), (b'przedsiebiorca', 'Przedsi\u0119biorca/ w\u0142a\u015bciciel firmy'), (b'wolny', 'Wolny zaw\xf3d'), (b'emeryt', 'Emeryt/ rencista'), (b'bezrobotny', 'Nie pracuj\u0105cy'), (b'inne', 'Inne zaj\u0119cie')]),
            preserve_default=True,
        ),
    ]
