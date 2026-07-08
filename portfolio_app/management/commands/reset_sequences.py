from django.apps import apps
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection


class Command(BaseCommand):
    help = (
        "Resetea las secuencias de autoincremento de la base de datos. "
        "Útil tras un `loaddata` en PostgreSQL (evita errores de 'duplicate key' "
        "en el próximo INSERT). En SQLite es un no-op seguro."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'app_labels',
            nargs='*',
            help="Apps a resetear. Por defecto: portfolio_app.",
        )

    def handle(self, *args, **options):
        app_labels = options['app_labels'] or ['portfolio_app']

        with connection.cursor() as cursor:
            for app_label in app_labels:
                models = list(apps.get_app_config(app_label).get_models())
                statements = connection.ops.sequence_reset_sql(no_style(), models)
                for sql in statements:
                    cursor.execute(sql)
                self.stdout.write(self.style.SUCCESS(
                    f"Secuencias reseteadas para '{app_label}': "
                    f"{len(models)} modelos, {len(statements)} sentencias "
                    f"(motor: {connection.vendor})."
                ))
