from django.db import migrations
from image_upload.models import Tier

def create_default_tiers(apps, schema_editor):
    Tier.objects.create(name='Basic', thumbnail_sizes="200")
    Tier.objects.create(name='Premium', thumbnail_sizes="200,400", link_to_original=True)
    Tier.objects.create(name='Enterprise', thumbnail_sizes="200,400", link_to_original=True, expiring_link=True)

class Migration(migrations.Migration):

    dependencies = [
        ('image_upload', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_tiers),
    ]
