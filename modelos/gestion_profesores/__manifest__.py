{
    'name': 'Gestión de Profesores',
    'version': '19.0.1.0',
    'category': 'Education',
    'summary': 'Módulo de gestión de profesores y grupos de clase',
    'author': 'EduOdoo',
    'license': 'LGPL-3',
    'depends': ['gestion_academica'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/profesor_academico_views.xml',
        'views/grupo_clase_views.xml',
        'views/sesion_academica_extension.xml',
        'demo/demo.xml',
    ],
    'installable': True,
}
