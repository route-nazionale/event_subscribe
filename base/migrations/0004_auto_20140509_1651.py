# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0003_auto_20140509_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'scoutchief',
            name=b'scout_group',
            field=models.ForeignKey(to=b'base.ScoutGroup', to_field='id'),
        ),
    ]
