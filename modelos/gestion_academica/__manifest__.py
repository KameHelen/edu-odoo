{
    'name': 'Gestión Académica',
    'version': '19.0.1.0',
    'category': 'Education',
    'summary': 'Sistema integral de gestión académica - Módulo base',
    'author': 'EduOdoo',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/curso_academico_views.xml',
        'views/sesion_academica_views.xml',
        'demo/demo.xml',
    ],
    'installable': True,
}
