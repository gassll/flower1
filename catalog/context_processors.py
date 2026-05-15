from catalog.models import Category


def categories_processor(request):
    footer_category_slugs = [
        'avtorskie-bukety',
        'vazy',
        'mono-duo-i-trio-bukety',
        'korziny-tsvetov',
        'cveti-v-korobke'
    ]

    footer_categories = Category.objects.filter(
        slug__in=footer_category_slugs
    )

    return {
        'footer_categories': footer_categories
    }