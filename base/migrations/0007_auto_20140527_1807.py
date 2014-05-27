# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0006_auto_20140527_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'heartbeat',
            name=b'code',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name=b'heartbeat',
            name=b'description',
        ),
    ]
