from django.core.management.base import BaseCommand
from core.models import MqttLog

class Command(BaseCommand):
    help = "Migrate MqttLog data from SQLite to PostgreSQL"

    def handle(self, *args, **options):
        source_qs = MqttLog.objects.using("sqlite").all()
        total = source_qs.count()

        self.stdout.write(f"Found {total} records in SQLite")

        created = 0
        for row in source_qs.iterator():
            MqttLog.objects.using("default").create(
                topic=row.topic,
                payload=row.payload,
                timestamp=row.timestamp
            )
            created += 1

            if created % 100 == 0:
                self.stdout.write(f"Migrated {created}/{total}")

        self.stdout.write(self.style.SUCCESS(
            f"Migration complete: {created} records copied"
        ))
