# Generated by Django 4.2.13 on 2024-06-03 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="avg_score",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="total_score",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]