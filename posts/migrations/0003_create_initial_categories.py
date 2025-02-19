from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')  # หาคลาส Category
    categories = [
        {'name': 'พูดคุยทั่วไป', 'slug': 'พูดคุยทั่วไป'},
        {'name': 'นักศึกษาสอบถามอาจารย์', 'slug': 'นักศึกษาสอบถามอาจารย์'},
        {'name': 'แจกชีต', 'slug': 'แจกชีต'},
        {'name': 'แจกแนวข้อสอบ', 'slug': 'แจกแนวข้อสอบ'},
    ]
    for category in categories:
        Category.objects.create(**category)

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_category_alter_post_options_post_slug_post_status_and_more'),  # ใช้หมายเลข migration ก่อนหน้านี้ที่เหมาะสม
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]
