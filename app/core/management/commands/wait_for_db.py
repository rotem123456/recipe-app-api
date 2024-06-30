"""
Django command for the database to be available.
"""

from typing import Any
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args: Any, **options: Any):
        pass