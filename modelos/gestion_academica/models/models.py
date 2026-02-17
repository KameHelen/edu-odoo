from odoo import models, fields, api
from datetime import timedelta


class CursoAcademico(models.Model):
    _name = 'curso.academico'
    _description = 'Curso Académico'
    _rec_name = 'titulo'

    titulo = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción')
    nivel = fields.Selection([
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('c1', 'C1'),
        ('c2', 'C2'),
    ], string='Nivel', required=True)
    precio = fields.Float(string='Precio', required=True)
    
    # Campos computados
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        compute='_compute_fecha_inicio',
        store=True
    )
    
    # Relaciones
    sesion_ids = fields.One2many(
        comodel_name='sesion.academica',
        inverse_name='curso_id',
        string='Sesiones'
    )
    
    @api.depends('sesion_ids.fecha_inicio')
    def _compute_fecha_inicio(self):
        """Calcula la fecha de inicio como la fecha de la primera sesión"""
        for curso in self:
            if curso.sesion_ids:
                curso.fecha_inicio = min(sesion.fecha_inicio for sesion in curso.sesion_ids)
            else:
                curso.fecha_inicio = False


class SesionAcademica(models.Model):
    _name = 'sesion.academica'
    _description = 'Sesión Académica'

    name = fields.Char(string='Nombre Sesión', compute='_compute_name', store=True)

    fecha_inicio = fields.Datetime(string='Fecha y Hora de Inicio', required=True)
    duracion = fields.Integer(string='Duración (minutos)', required=True)
    numero_asientos = fields.Integer(string='Número de Asientos', required=True)
    
    fecha_fin = fields.Datetime(
        string='Fecha Final',
        compute='_compute_fecha_fin',
        store=True
    )
    
    @api.depends('fecha_inicio', 'duracion')
    def _compute_fecha_fin(self):
        """Calcula la fecha de fin basada en inicio + duración"""
        for record in self:
            if record.fecha_inicio and record.duracion:
                record.fecha_fin = record.fecha_inicio + timedelta(minutes=record.duracion)
            else:
                record.fecha_fin = False
    
    # Relaciones
    curso_id = fields.Many2one(
        comodel_name='curso.academico',
        string='Curso',
        required=True,
        ondelete='cascade'
    )
    
    # Campos computados - solo los que no dependen de matricula_ids
    numero_alumnos = fields.Integer(
        string='Alumnos Inscritos',
        default=0
    )
    porcentaje_ocupacion = fields.Float(
        string='% Ocupación',
        compute='_compute_porcentaje_ocupacion',
        store=True
    )
    estado_ocupacion = fields.Selection([
        ('vacio', 'Vacío'),
        ('parcial', 'Parcial'),
        ('lleno', 'Lleno'),
    ], string='Estado Ocupación',
        compute='_compute_estado_ocupacion',
        store=True
    )
    color_ocupacion = fields.Integer(
        string='Color Ocupación',
        compute='_compute_color_ocupacion',
        store=True
    )
    

    @api.depends('numero_alumnos', 'numero_asientos')
    def _compute_porcentaje_ocupacion(self):
        """Calcula el porcentaje de ocupación"""
        for sesion in self:
            if sesion.numero_asientos > 0:
                sesion.porcentaje_ocupacion = (sesion.numero_alumnos / sesion.numero_asientos) * 100
            else:
                sesion.porcentaje_ocupacion = 0.0
    
    @api.depends('porcentaje_ocupacion')
    def _compute_estado_ocupacion(self):
        """Calcula el estado (vacío, parcial, lleno)"""
        for sesion in self:
            if sesion.porcentaje_ocupacion == 0:
                sesion.estado_ocupacion = 'vacio'
            elif sesion.porcentaje_ocupacion < 100:
                sesion.estado_ocupacion = 'parcial'
            else:
                sesion.estado_ocupacion = 'lleno'
    
    @api.depends('porcentaje_ocupacion')
    def _compute_color_ocupacion(self):
        """Asigna color basado en ocupación: 10=verde (<50%), 2=naranja (>=50%), 1=rojo (100%)"""
        for sesion in self:
            if sesion.porcentaje_ocupacion < 50:
                sesion.color_ocupacion = 10  # Verde
            elif sesion.porcentaje_ocupacion < 100:
                sesion.color_ocupacion = 2   # Naranja
            else:
                sesion.color_ocupacion = 1   # Rojo
    
    @api.constrains('numero_alumnos', 'numero_asientos')
    def _check_numero_alumnos(self):
        """Validación: no permitir más alumnos que asientos"""
        for sesion in self:
            if sesion.numero_alumnos > sesion.numero_asientos:
                from odoo.exceptions import ValidationError
                raise ValidationError(
                    f"No se pueden inscribir más alumnos ({sesion.numero_alumnos}) "
                    f"que asientos disponibles ({sesion.numero_asientos})"
                )

    @api.depends('curso_id.titulo', 'fecha_inicio')
    def _compute_name(self):
        for sesion in self:
            fecha = sesion.fecha_inicio.strftime('%d/%m/%Y %H:%M') if sesion.fecha_inicio else ''
            sesion.name = f"{sesion.curso_id.titulo} - {fecha}" if sesion.curso_id else f"Sesión {fecha}"
