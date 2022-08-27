# Generated by Django 4.0.6 on 2022-07-24 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='frushgahmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('family', models.CharField(max_length=50)),
                ('gender', models.IntegerField(choices=[('man', 'مرد'), ('woman', 'زن')])),
            ],
        ),
    ]
