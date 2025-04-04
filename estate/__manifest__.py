# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,

    'author': "Kevin",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/property_type/estate_property_type_list.xml',
        'views/property_type/estate_property_type_form.xml',
        'views/property_tag/estate_property_tag_form.xml',
        'views/estate_property_list.xml',
        'views/estate_property_form.xml',
        'views/estate_property_search.xml',
        'views/property_tag/estate_property_tag_views.xml',
        'views/property_type/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}

