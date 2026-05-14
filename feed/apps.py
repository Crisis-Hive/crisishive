from django.apps import AppConfig


class FeedConfig(AppConfig):
    name = 'feed'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(load_categories, sender=self)


def load_categories(sender, **kwargs):
    from feed.models import Category
    if Category.objects.exists():
        return  # already loaded, skip

    categories = [
        {'name': 'Flood',                'icon': '🌊', 'color': '#1E90FF'},
        {'name': 'Fire',                 'icon': '🔥', 'color': '#FF4500'},
        {'name': 'Earthquake',           'icon': '🌍', 'color': '#8B4513'},
        {'name': 'Cyclone',              'icon': '🌀', 'color': '#9400D3'},
        {'name': 'Landslide',            'icon': '⛰️', 'color': '#A0522D'},
        {'name': 'Drought',              'icon': '☀️', 'color': '#FFD700'},
        {'name': 'Industrial Accident',  'icon': '🏭', 'color': '#808080'},
        {'name': 'Road Accident',        'icon': '🚗', 'color': '#FF6347'},
        {'name': 'Building Collapse',    'icon': '🏚️', 'color': '#CD853F'},
        {'name': 'Disease Outbreak',     'icon': '🦠', 'color': '#32CD32'},
    ]
    for cat in categories:
        Category.objects.create(**cat)
    print(f"[CrisisHive] Loaded {len(categories)} categories.")