# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-19 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('localizacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleActaCongresal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('votos', models.IntegerField()),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleActaPresidencial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField()),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDisenioActaCongresal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero1', models.BooleanField(default=False)),
                ('numero2', models.BooleanField(default=False)),
                ('numero3', models.BooleanField(default=False)),
                ('numero4', models.BooleanField(default=False)),
                ('numero5', models.BooleanField(default=False)),
                ('numero6', models.BooleanField(default=False)),
                ('numero7', models.BooleanField(default=False)),
                ('numero8', models.BooleanField(default=False)),
                ('numero9', models.BooleanField(default=False)),
                ('numero10', models.BooleanField(default=False)),
                ('numero11', models.BooleanField(default=False)),
                ('numero12', models.BooleanField(default=False)),
                ('numero13', models.BooleanField(default=False)),
                ('numero14', models.BooleanField(default=False)),
                ('numero15', models.BooleanField(default=False)),
                ('numero16', models.BooleanField(default=False)),
                ('numero17', models.BooleanField(default=False)),
                ('numero18', models.BooleanField(default=False)),
                ('numero19', models.BooleanField(default=False)),
                ('numero20', models.BooleanField(default=False)),
                ('numero21', models.BooleanField(default=False)),
                ('numero22', models.BooleanField(default=False)),
                ('numero23', models.BooleanField(default=False)),
                ('numero24', models.BooleanField(default=False)),
                ('numero25', models.BooleanField(default=False)),
                ('numero26', models.BooleanField(default=False)),
                ('numero27', models.BooleanField(default=False)),
                ('numero28', models.BooleanField(default=False)),
                ('numero29', models.BooleanField(default=False)),
                ('numero30', models.BooleanField(default=False)),
                ('numero31', models.BooleanField(default=False)),
                ('numero32', models.BooleanField(default=False)),
                ('numero33', models.BooleanField(default=False)),
                ('numero34', models.BooleanField(default=False)),
                ('numero35', models.BooleanField(default=False)),
                ('numero36', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDisenioActaPresidencial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presidente', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DisenioActaCongresal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Region')),
            ],
        ),
        migrations.CreateModel(
            name='DisenioActaPresidencial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MesaNacional',
            fields=[
                ('numero', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('total_electores', models.IntegerField()),
                ('procesada_presidencial', models.BooleanField(default=False)),
                ('procesada_congresal', models.BooleanField(default=False)),
                ('procesada_parlandino', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VotacionCongresalCandidato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('votos', models.IntegerField(default=0)),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Region')),
            ],
        ),
        migrations.CreateModel(
            name='VotacionCongresalTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField(default=0)),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Region')),
            ],
        ),
        migrations.CreateModel(
            name='VotacionPresidente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField(default=0)),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido')),
            ],
        ),
        migrations.CreateModel(
            name='ActaCongresal',
            fields=[
                ('mesa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nacional.MesaNacional')),
                ('votos_blancos', models.IntegerField()),
                ('votos_nulos', models.IntegerField()),
                ('votos_impugnados', models.IntegerField()),
                ('votos_emitidos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ActaPresidencial',
            fields=[
                ('mesa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='nacional.MesaNacional')),
                ('votos_blancos', models.IntegerField()),
                ('votos_nulos', models.IntegerField()),
                ('votos_impugnados', models.IntegerField()),
                ('votos_emitidos', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='mesanacional',
            name='centro_votacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.CentroVotacion'),
        ),
        migrations.AddField(
            model_name='detalledisenioactapresidencial',
            name='disenio_acta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nacional.DisenioActaPresidencial'),
        ),
        migrations.AddField(
            model_name='detalledisenioactapresidencial',
            name='partido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido'),
        ),
        migrations.AddField(
            model_name='detalledisenioactacongresal',
            name='disenio_acta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nacional.DisenioActaCongresal'),
        ),
        migrations.AddField(
            model_name='detalledisenioactacongresal',
            name='partido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localizacion.Partido'),
        ),
        migrations.AddField(
            model_name='detalleactapresidencial',
            name='acta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nacional.ActaPresidencial'),
        ),
        migrations.AddField(
            model_name='detalleactacongresal',
            name='acta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nacional.ActaCongresal'),
        ),
        migrations.AlterUniqueTogether(
            name='detalleactapresidencial',
            unique_together=set([('acta', 'partido')]),
        ),
        migrations.AlterUniqueTogether(
            name='detalleactacongresal',
            unique_together=set([('acta', 'partido', 'numero')]),
        ),
    ]