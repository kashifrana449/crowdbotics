from django.core.management.base import BaseCommand, CommandError
from apps.models import Plan


class Command(BaseCommand):
    help = 'Add the plans in database'

    def handle(self, *args, **options):
        plans = [
            {
                'name': 'Free',
                'price': 0,
            },
            {
                'name': 'Standard',
                'price': 10,
            },
            {
                'name': 'Pro',
                'price': 25,
            }
        ]
        for plan_item in plans:
            Plan.objects.get_or_create(**plan_item)
        total_plans = Plan.objects.all().count()
        if total_plans <= 3:
            self.stdout.write(self.style.ERROR('%d plans are added in plan table and total plans are 3' % total_plans))
        else:
            self.stdout.write(self.style.SUCCESS('All plans have been inserted in plan table successfully'))