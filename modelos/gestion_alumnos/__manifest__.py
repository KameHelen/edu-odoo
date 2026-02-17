{
    'name': 'Gestión de Alumnos',
    'version': '19.0.1.0',
    'category': 'Education',
    'summary': 'Módulo de gestión de alumnos y matrículas',
    'author': 'EduOdoo',
    'license': 'LGPL-3',
    'depends': ['gestion_academica'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/alumno_academico_views.xml',
        'views/sesion_alumno_views.xml',
        'views/factura_academica_views.xml',
        'views/sesion_academica_extensions.xml',
        'demo/demo.xml',
    ],
    'installable': True,
}
