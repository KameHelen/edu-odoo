from odoo import models, fields


class SesionAcademicaExtension(models.Model):
    """Extension of sesion.academica to add grupo_clase_ids field"""
    _inherit = 'sesion.academica'

    grupo_clase_ids = fields.One2many(
        comodel_name='grupo.clase',
        inverse_name='sesion_id',
        string='Grupos de Clase'
    )
