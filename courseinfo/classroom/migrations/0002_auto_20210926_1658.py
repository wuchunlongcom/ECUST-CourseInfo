# Generated by Django 2.2.6 on 2021-09-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='id',
            field=models.CharField(blank=True, max_length=128, primary_key=True, serialize=False, verbose_name='教室ID'),
        ),
        migrations.AlterField(
            model_name='course',
            name='courseid',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='课程ID'),
        ),
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
