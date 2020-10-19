# Generated by Django 3.1.1 on 2020-10-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201019_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Upcoming', 'Upcoming'), ('Ended', 'Ended')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Reserved', 'Reserved'), ('Expired', 'Expired')], max_length=100, null=True),
        ),
    ]
