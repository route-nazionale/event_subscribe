# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0004_auto_20140527_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'event',
            name=b'num',
            field=models.CharField(max_length=32, verbose_name=b'codice numerico'),
        ),
    ]
