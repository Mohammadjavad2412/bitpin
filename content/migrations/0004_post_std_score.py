# Generated by Django 4.2.13 on 2024-06-03 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0003_post_rate_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="std_score",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
