# Generated by Django 4.2 on 2023-05-24 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeriaWorks', '0005_pizza_isalive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeriaWorks.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeriaWorks.order')),
                ('pizza_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeriaWorks.pizza')),
            ],
        ),
    ]