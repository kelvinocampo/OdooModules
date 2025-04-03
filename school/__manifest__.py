# -*- coding: utf-8 -*-
{
    'name': "Modulo de Administracion de Escuela aa",

    'summary': "Administra puntuciones de alumnos, profesores y materias.",

    'description': """
        Long description of module's purpose
    """,

    'author': "Kevin",
    'website': "",

    'category': 'Education',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
