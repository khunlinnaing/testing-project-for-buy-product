from project.models import *
from django.db.models import Max
from django.db import transaction
def generate_unique_sale_no(name, model_name, field_name):

    with transaction.atomic():
        last_number_of_generate = (
            model_name.objects.aggregate(max_no=Max(field_name))['max_no']
        )

        if last_number_of_generate:
            try:
                last_number = int(last_number_of_generate.split('_')[-1])
            except (IndexError, ValueError):
                last_number = 0
        else:
            last_number = 0
        new_number = last_number + 1
        number_of_generate = f"{name}_{new_number:06d}"
        while model_name.objects.filter(**{field_name: number_of_generate}).exists():
            new_number += 1
            number_of_generate = f"{name}_{new_number:06d}"

        return number_of_generate