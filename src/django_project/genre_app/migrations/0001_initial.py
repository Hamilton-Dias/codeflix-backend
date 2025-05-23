import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('category_app', '0002_alter_category_description_alter_category_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(related_name='genres', to='category_app.category')),
            ],
            options={
                'db_table': 'genres',
            },
        ),
    ]
