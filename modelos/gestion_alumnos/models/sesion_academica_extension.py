from odoo import models, fields, api


class SesionAcademicaExtension(models.Model):
    """Extension of sesion.academica to add matricula_ids field"""
    _inherit = 'sesion.academica'

    matricula_ids = fields.One2many(
        comodel_name='sesion.alumno',
        inverse_name='sesion_id',
        string='Matrículas'
    )

    numero_alumnos = fields.Integer(
        string='Número de Alumnos',
        compute='_compute_numero_alumnos',
        store=True
    )

    @api.depends('matricula_ids')
    def _compute_numero_alumnos(self):
        """Calcula el número de alumnos inscritos en la sesión"""
        for sesion in self:
            sesion.numero_alumnos = len(sesion.matricula_ids or [])
