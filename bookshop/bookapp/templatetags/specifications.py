from django import template
from django.utils.safestring import mark_safe

from bookapp.models import OfficeSupply

register = template.Library()


TABLE_HEAD = """
                <table class="table">
                    <tbody>
             """

TABLE_BOTTOM = """
                    </tbody>
                </table>
               """

TABLE_CONTENT = """
                <tr>
                    <td>{name}</td>
                    <td>{value}</td>
                </tr>
                """

PRODUCT_SPEC = {
    'book': {
        'Автор': 'author',
        'Издатель': 'publisher',
        'Год издания': 'publication_date',
        'Кол-во страниц': 'pages_number',
        'Формат': 'format',
        'Вес, г': 'wt',
        'Возрастные ограничения': 'age_limit'
    },
    'officesupply': {
        'Формат': 'format',
        'Вес, г': 'wt',
        'Наличие производителя': 'manufacturer',
        'Производитель': 'manufacturer_name'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, OfficeSupply):
        if not product.manufacturer:
            PRODUCT_SPEC['officesupply'].pop('Наличие производителя')
            PRODUCT_SPEC['officesupply'].pop('Производитель')
        else:
            PRODUCT_SPEC['officesupply']['Производитель'] = 'manufacturer_name'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_BOTTOM)


