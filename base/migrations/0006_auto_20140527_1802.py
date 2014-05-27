# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0005_auto_20140527_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'event',
            name=b'num',
            field=models.IntegerField(verbose_name=b'codice numerico'),
        ),
    ]
