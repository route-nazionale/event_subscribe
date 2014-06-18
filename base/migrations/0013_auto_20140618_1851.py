# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0012_event_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'event',
            name=b'name',
            field=models.CharField(max_length=128),
        ),
    ]
