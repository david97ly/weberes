# Generated by Django 2.0.5 on 2020-01-12 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eres', '0024_permisos_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permisos',
            name='perfil',
        ),
        migrations.AddField(
            model_name='perfil',
            name='permiso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eres.Permisos'),
        ),
    ]
