# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'event',
            name=b'dt_start',
            field=models.DateTimeField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name=b'event',
            name=b'dt_stop',
            field=models.DateTimeField(default=datetime.date(2014, 5, 9)),
            preserve_default=False,
        ),
    ]
