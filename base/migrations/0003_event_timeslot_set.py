# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0002_eventperson'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'event',
            name=b'timeslot_set',
            field=models.ManyToManyField(to=b'base.EventTimeSlot', through=b'base.EventHappening'),
            preserve_default=True,
        ),
    ]
