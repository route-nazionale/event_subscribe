# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0003_event_timeslot_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'scoutchief',
            name=b'birthday',
            field=models.DateField(verbose_name=b'data di nascita'),
        ),
    ]
