# Generated by Django 2.0.5 on 2019-01-08 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eres', '0010_auto_20190108_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenperfil',
            name='perfil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eres.Perfil'),
        ),
    ]
