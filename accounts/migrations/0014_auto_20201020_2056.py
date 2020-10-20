# Generated by Django 3.1.1 on 2020-10-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_ticket_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='name',
            new_name='event_name',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='email',
            new_name='host_email',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='name',
            new_name='host_name',
        ),
        migrations.RenameField(
            model_name='visitor',
            old_name='email',
            new_name='visitor_email',
        ),
        migrations.RenameField(
            model_name='visitor',
            old_name='name',
            new_name='visitor_name',
        ),
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.RemoveField(
            model_name='event',
            name='status',
        ),
        migrations.RemoveField(
            model_name='host',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='phone',
        ),
        migrations.AddField(
            model_name='event',
            name='event_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='host_phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='visitor_phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
