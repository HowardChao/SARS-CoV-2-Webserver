# Generated by Django 2.2.6 on 2020-07-31 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadSeq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='fastafile',
            field=models.FileField(upload_to='fasta_files/'),
        ),
    ]
