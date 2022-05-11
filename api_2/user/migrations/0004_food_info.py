# Generated by Django 4.0.4 on 2022-05-11 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_profile_goal_cal'),
    ]

    operations = [
        migrations.CreateModel(
            name='food_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=255)),
                ('food_cal', models.IntegerField()),
                ('food_protein', models.FloatField()),
                ('food_fat', models.FloatField()),
                ('food_carbo', models.FloatField()),
                ('food_sugar', models.FloatField()),
                ('food_chole', models.FloatField()),
                ('food_sodium', models.FloatField()),
                ('food_saturated_fat', models.FloatField()),
                ('food_trans_fat', models.FloatField()),
            ],
        ),
    ]