# Generated by Django 4.0.1 on 2022-02-04 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_courseepisode_title'),
        ('cart', '0002_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='final_unit_price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='unit_price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(blank=True, help_text='فقط در لحظه ی نهایی شدن سفارش، قیمت ذخیره میشود', null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='course.course'),
        ),
    ]
