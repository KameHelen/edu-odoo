from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProfesorAcademico(models.Model):
    _name = 'profesor.academico'
    _description = 'Profesor Académico'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    titulacion = fields.Char(string='Titulación', required=True)
    
    # Relaciones
    curso_ids = fields.Many2many(
        comodel_name='curso.academico',
        relation='curso_profesor_rel',
        column1='profesor_id',
        column2='curso_id',
        string='Cursos'
    )
    grupo_clase_ids = fields.One2many(
        comodel_name='grupo.clase',
        inverse_name='profesor_id',
        string='Grupos de Clase'
    )


class GrupoClase(models.Model):
    _name = 'grupo.clase'
    _description = 'Grupo de Clase'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    horario = fields.Selection([
        ('08:00', '08:00 - 09:00'),
        ('09:00', '09:00 - 10:00'),
        ('10:00', '10:00 - 11:00'),
        ('11:00', '11:00 - 12:00'),
        ('12:00', '12:00 - 13:00'),
        ('13:00', '13:00 - 14:00'),
        ('14:00', '14:00 - 15:00'),
        ('15:00', '15:00 - 16:00'),
        ('16:00', '16:00 - 17:00'),
        ('17:00', '17:00 - 18:00'),
        ('18:00', '18:00 - 19:00'),
        ('19:00', '19:00 - 20:00'),
        ('20:00', '20:00 - 21:00'),
    ], string='Horario', required=True)
    
    # Relaciones
    profesor_id = fields.Many2one(
        comodel_name='profesor.academico',
        string='Profesor',
        required=True,
        ondelete='cascade'
    )
    sesion_id = fields.Many2one(
        comodel_name='sesion.academica',
        string='Sesión',
        required=True,
        ondelete='cascade'
    )
    
    @api.constrains('profesor_id', 'horario')
    def _check_profesor_schedule(self):
        """Validación: profesor no puede tener 2 clases a la misma hora"""
        for grupo in self:
            if grupo.profesor_id and grupo.horario:
                conflictos = self.search([
                    ('profesor_id', '=', grupo.profesor_id.id),
                    ('horario', '=', grupo.horario),
                    ('id', '!=', grupo.id)
                ])
                if conflictos:
                    raise ValidationError(
                        f"El profesor {grupo.profesor_id.nombre} ya tiene una clase "
                        f"a la hora {grupo.horario}"
                    )
