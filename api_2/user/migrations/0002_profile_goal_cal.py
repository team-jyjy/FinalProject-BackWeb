# Generated by Django 4.0.4 on 2022-05-11 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='goal_cal',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
    ]
