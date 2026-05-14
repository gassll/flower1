from .models import Category


def categories_processor(request):
    """Делает список категорий для подвала доступным во всех шаблонах"""
    # Выбираем только нужные категории в нужном порядке
    footer_category_slugs = [
        'avtorskie-bukety',
        'vazy',
        'mono-duo-i-trio-bukety',
        'korziny-tsvetov',
        'cveti-v-korobke'
    ]

    footer_categories = Category.objects.filter(
        slug__in=footer_category_slugs
    ).order_by('name')

    return {
        'footer_categories': footer_categories
    }