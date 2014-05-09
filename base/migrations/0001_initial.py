# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'SubCamp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'ScoutGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'verbose_name': b'gruppo scout',
                'verbose_name_plural': b'gruppi scout',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Chief',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'code_membership', models.CharField(unique=True, max_length=128)),
                (b'scout_group', models.ForeignKey(to=b'base.ScoutGroup', to_field='id')),
            ],
            options={
                'verbose_name': b'capo',
                'verbose_name_plural': b'capi',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
                (b'description', models.TextField(blank=True)),
                (b'kind', models.CharField(default=b'lab', max_length=32, choices=[(b'lab', b'laboratorio'), (b'round-table', b'tavola rotonda')])),
                (b'tot_seats', models.IntegerField(blank=True)),
                (b'n_seats', models.IntegerField(blank=True)),
                (b'is_handicap_compatible', models.BooleanField(default=True)),
                (b'subcamp', models.ForeignKey(to=b'base.SubCamp', to_field='id')),
            ],
            options={
                'verbose_name': b'evento',
                'verbose_name_plural': b'eventi',
            },
            bases=(models.Model,),
        ),
    ]
