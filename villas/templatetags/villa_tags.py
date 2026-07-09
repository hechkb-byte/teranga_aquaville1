from django import template

register = template.Library()


@register.filter
def format_prix(value):
    """Formate un entier en prix FCFA : 175000000 → 175 000 000"""
    try:
        return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return value
