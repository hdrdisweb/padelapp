# Generated by Django 5.1.6 on 2025-03-14 14:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padelapp', '0006_singlematch_lugar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='ubicacion',
            new_name='lugar',
        ),
        migrations.RemoveField(
            model_name='match',
            name='max_jugadores',
        ),
        migrations.RemoveField(
            model_name='match',
            name='motivo_cancelacion',
        ),
        migrations.AlterField(
            model_name='match',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='estado',
            field=models.CharField(choices=[('Abierto', 'Abierto'), ('Cerrado', 'Cerrado')], default='Abierto', max_length=10),
        ),
        migrations.CreateModel(
            name='PartidoAbierto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('lugar', models.CharField(max_length=200)),
                ('estado', models.CharField(choices=[('Abierto', 'Abierto'), ('Cerrado', 'Cerrado')], default='Abierto', max_length=10)),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_creados', to=settings.AUTH_USER_MODEL)),
                ('jugadores', models.ManyToManyField(blank=True, related_name='partidos_jugados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='SingleMatch',
        ),
    ]
