# Generated by Django 3.0.4 on 2020-04-29 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200429_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejecarchch',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivosCh/'),
        ),
    ]
