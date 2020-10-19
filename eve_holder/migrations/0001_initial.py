# Generated by Django 3.1.2 on 2020-10-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=500, null=True)),
                ('event_description', models.CharField(max_length=500, null=True)),
                ('event_pub_date', models.DateTimeField(null=True, verbose_name='published date')),
                ('event_end_date', models.DateTimeField(null=True, verbose_name='ending date')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=100, null=True)),
                ('host_email', models.EmailField(max_length=200, null=True)),
                ('host_phone_num', models.CharField(max_length=100, null=True)),
                ('host_password', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_name', models.CharField(max_length=150, null=True)),
                ('visitor_phone_num', models.CharField(max_length=100, null=True)),
                ('visitor_email', models.EmailField(max_length=100, null=True)),
                ('visitor_password', models.CharField(max_length=50, null=True)),
                ('event', models.ManyToManyField(to='eve_holder.Event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_host',
            field=models.ManyToManyField(to='eve_holder.Host'),
        ),
    ]
