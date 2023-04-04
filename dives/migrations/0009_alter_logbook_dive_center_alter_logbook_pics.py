# Generated by Django 4.1.6 on 2023-03-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dives", "0008_alter_logbook_buddy_alter_logbook_guide_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logbook",
            name="dive_center",
            field=models.CharField(
                default="https://www.padi.com/dive-shops/nearby/?lang=en",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="logbook",
            name="pics",
            field=models.FileField(blank=True, upload_to=""),
        ),
    ]
