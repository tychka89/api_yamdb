# Generated by Django 2.2.16 on 2022-11-06 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221106_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genretitle',
            old_name='genre',
            new_name='genre_id',
        ),
        migrations.RenameField(
            model_name='genretitle',
            old_name='title',
            new_name='title_id',
        ),
    ]