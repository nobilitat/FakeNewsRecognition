from django.db.models import TextChoices

class Categories(TextChoices):
    false = ("Ложь", "Ложь")
    true = ("Истина", "Истина")