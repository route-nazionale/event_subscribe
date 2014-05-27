# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'District',
            fields=[
                (b'code', models.CharField(max_length=8, serialize=False, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'db_table': b'camp_districts',
                'verbose_name': b'sottocampo',
                'verbose_name_plural': b'sottocampi',
            },
            bases=(models.Model,),
        ),
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
                'db_table': b'camp_eventtimeslots',
                'verbose_name': b'slot temporale',
                'verbose_name_plural': b'slot temporali',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=128)),
                (b'code', models.CharField(max_length=128, verbose_name=b'codice censimento', blank=True)),
                (b'city', models.CharField(max_length=128, blank=True)),
                (b'kind', models.CharField(default=b'CHIEF', max_length=16, choices=[(b'CHIEF', b'capo'), (b'GUEST', b'ospite')])),
                (b'description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'HeartBeat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
                (b'description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Unit',
            fields=[
                (b'name', models.CharField(max_length=128, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': b'scout_units',
                'verbose_name': b'gruppo scout',
                'verbose_name_plural': b'gruppi scout',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'ScoutChief',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'code', models.CharField(unique=True, max_length=128, verbose_name=b'codice censimento')),
                (b'scout_unit', models.ForeignKey(to=b'base.Unit', to_field=b'name')),
                (b'name', models.CharField(max_length=32, verbose_name=b'nome')),
                (b'surname', models.CharField(max_length=32, verbose_name=b'cognome')),
                (b'birthday', models.DateField()),
            ],
            options={
                'db_table': b'scout_chiefs',
                'verbose_name': b'capo scout',
                'verbose_name_plural': b'capi scout',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
                (b'description', models.TextField(blank=True)),
                (b'kind', models.CharField(default=b'LAB', max_length=32, choices=[(b'LAB', b'laboratorio'), (b'TAV', b'tavola rotonda')])),
                (b'district', models.ForeignKey(to=b'base.District', to_field=b'code')),
                (b'topic', models.ForeignKey(to=b'base.HeartBeat', to_field='id', verbose_name=b'strada di coraggio')),
                (b'num', models.IntegerField(verbose_name=b'codice numerico')),
                (b'seats_tot', models.IntegerField(blank=True)),
                (b'seats_n_boys', models.IntegerField(blank=True)),
                (b'seats_n_chiefs', models.IntegerField(blank=True)),
                (b'min_seats', models.IntegerField(default=1, blank=True)),
                (b'max_boys_seats', models.IntegerField(default=30, blank=True)),
                (b'max_chiefs_seats', models.IntegerField(default=5, blank=True)),
                (b'min_age', models.IntegerField(verbose_name=b'et\xc3\xa0 minima', blank=True)),
                (b'max_age', models.IntegerField(verbose_name=b'et\xc3\xa0 massima', blank=True)),
                (b'state_handicap', models.CharField(default=b'ENABLED', max_length=16, verbose_name=b'accessibilit\xc3\xa0 ai diversamente abili', choices=[(b'ENABLED', b'abilitato'), (b'DISABLED', b'disabilitato')])),
                (b'state_chief', models.CharField(default=b'ENABLED', max_length=16, verbose_name=b'rivolto ai capi', choices=[(b'ENABLED', b'abilitato'), (b'RESERVED', b'riservato'), (b'DISABLED', b'disabilitato')])),
                (b'state_activation', models.CharField(default=b'ACTIVE', max_length=16, verbose_name=b'stato di attivazione', choices=[(b'CREATING', b'in creazione'), (b'ACTIVE', b'attivo'), (b'DISMISSED', b'dismesso')])),
                (b'state_subscription', models.CharField(default=b'OPEN', max_length=16, verbose_name=b'stato di iscrizione', choices=[(b'OPEN', b'aperte'), (b'CLOSED', b'chiuse')])),
            ],
            options={
                'db_table': b'camp_events',
                'verbose_name': b'definizione evento',
                'verbose_name_plural': b'definizione eventi',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'EventHappening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'timeslot', models.ForeignKey(to=b'base.EventTimeSlot', to_field='id')),
                (b'event', models.ForeignKey(to=b'base.Event', to_field='id')),
            ],
            options={
                'db_table': b'camp_eventhappenings',
                'verbose_name': b'evento',
                'verbose_name_plural': b'eventi',
            },
            bases=(models.Model,),
        ),
    ]
