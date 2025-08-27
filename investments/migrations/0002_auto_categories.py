from django.db import migrations

def create_investment_categories(apps, schema_editor):
    Category = apps.get_model("records", "Category")
    Subcategory = apps.get_model("records", "Subcategory")

    expense_cat, _ = Category.objects.get_or_create(
        category_name="Investments",
        category_type="expense",
    )
    Subcategory.objects.get_or_create(
        category=expense_cat,
        subcategory_name="Investments",
    )

    income_cat, _ = Category.objects.get_or_create(
        category_name="Investment income",
        category_type="income",
    )
    Subcategory.objects.get_or_create(
        category=income_cat,
        subcategory_name="Return on investment",
    )
    Subcategory.objects.get_or_create(
        category=income_cat,
        subcategory_name="Investment interests",
    )


def reverse_investment_categories(apps, schema_editor):
    Category = apps.get_model("records", "Category")
    Subcategory = apps.get_model("records", "Subcategory")

    try:
        Subcategory.objects.filter(
            subcategory_name__in=["Investments", "Return on investment", "Investment interests"]
        ).delete()

        Category.objects.filter(
            category_name__in=["Investments", "Investment income"]
        ).delete()
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("records", "0001_initial"), 
        ("investments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_investment_categories, reverse_investment_categories),
    ]
