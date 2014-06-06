# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_scoutchief_is_spalla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='max_chiefs_seats',
            field=models.IntegerField(default=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_boys_seats',
            field=models.IntegerField(default=30, null=True, blank=True),
        ),
    ]
