from django.core.management.base import BaseCommand
from matchapp.models import JobCategory


class Command(BaseCommand):
    help = 'Creates default job categories for househelp positions'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'General Househelp',
                'description': 'General household cleaning, cooking, and other domestic duties',
                'icon': 'fas fa-home'
            },
            {
                'name': 'Cleaning & Housekeeping',
                'description': 'Specialized in house cleaning, laundry, and organization',
                'icon': 'fas fa-broom'
            },
            {
                'name': 'Cooking & Kitchen',
                'description': 'Food preparation, meal planning, and kitchen management',
                'icon': 'fas fa-utensils'
            },
            {
                'name': 'Childcare',
                'description': 'Care for children, babysitting, and childcare services',
                'icon': 'fas fa-child'
            },
            {
                'name': 'Elderly Care',
                'description': 'Care for senior citizens and elderly family members',
                'icon': 'fas fa-heart'
            },
            {
                'name': 'Pet Care',
                'description': 'Pet sitting, dog walking, and pet care services',
                'icon': 'fas fa-paw'
            },
            {
                'name': 'Gardening & Landscaping',
                'description': 'Garden maintenance, landscaping, and outdoor work',
                'icon': 'fas fa-leaf'
            },
            {
                'name': 'Laundry & Ironing',
                'description': 'Laundry services, ironing, and clothes care',
                'icon': 'fas fa-spray-can'
            },
            {
                'name': 'Babysitting',
                'description': 'Temporary childcare and babysitting services',
                'icon': 'fas fa-baby'
            },
            {
                'name': 'Personal Assistant',
                'description': 'Administrative tasks, errands, and personal assistance',
                'icon': 'fas fa-tasks'
            },
        ]

        created_count = 0
        for category_data in categories:
            category, created = JobCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Category already exists: {category.name}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Successfully created {created_count} new categories")
        )
