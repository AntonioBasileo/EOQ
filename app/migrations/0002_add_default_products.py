from django.db import migrations

def create_default_products(apps, schema_editor):
    product = apps.get_model('app', 'Product')

    default_products = [
        {"code": "P001", "name": "Prodotto 1", "price": 10.0, "stock": 100},
        {"code": "P002", "name": "Prodotto 2", "price": 20.0, "stock": 50},
        {"code": "P003", "name": "Prodotto 3", "price": 15.5, "stock": 75},
    ]

    for prod in default_products:
        product.objects.get_or_create(code=prod["code"], defaults=prod)

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_products),
    ]
