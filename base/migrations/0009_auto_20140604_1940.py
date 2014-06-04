# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20140604_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtimeslot',
            name='name',
            field=models.CharField(max_length=32, unique=True, null=True, blank=True),
        ),
    ]
