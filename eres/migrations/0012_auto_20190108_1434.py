# Generated by Django 2.0.5 on 2019-01-08 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eres', '0011_auto_20190108_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagenperfil',
            name='perfil',
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto',
            field=models.ImageField(blank=True, default='avatares/usuario.png', null=True, upload_to='avatares'),
        ),
        migrations.DeleteModel(
            name='ImagenPerfil',
        ),
    ]
