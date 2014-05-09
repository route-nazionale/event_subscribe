# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'base', b'0002_auto_20140509_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'EventTimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=32)),
                (b'dt_start', models.DateTimeField()),
                (b'dt_stop', models.DateTimeField()),
            ],
            options={
                'ordering': (b'dt_start',),
                'verbose_name': b'slot temporale',
                'verbose_name_plural': b'slot temporali',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'ScoutChief',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'code_membership', models.CharField(unique=True, max_length=128, verbose_name=b'codice censimento')),
                (b'scout_group', models.ForeignKey(to=b'base.ScoutGroup', to_field='id', verbose_name=b'gruppo scout')),
            ],
            options={
                'verbose_name': b'capo scout',
                'verbose_name_plural': b'capi scout',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name=b'event',
            name=b'timeslot',
            field=models.ForeignKey(to=b'base.EventTimeSlot', default=1, to_field='id'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name=b'event',
            name=b'dt_start',
        ),
        migrations.RemoveField(
            model_name=b'event',
            name=b'dt_stop',
        ),
        migrations.DeleteModel(
            name=b'Chief',
        ),
    ]
