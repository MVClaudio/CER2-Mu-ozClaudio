# Generated by Django 5.1.1 on 2024-10-20 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_pedido_estado_carrito_carritoproducto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='total',
        ),
    ]
