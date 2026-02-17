from odoo import models, fields, api


class AlumnoAcademico(models.Model):
    _name = 'alumno.academico'
    _description = 'Alumno Académico'
    _rec_name = 'name'

    name = fields.Char(string='Nombre Completo', compute='_compute_name')

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    email = fields.Char(string='Email', required=True)
    
    # Relaciones
    matricula_ids = fields.One2many(
        comodel_name='sesion.alumno',
        inverse_name='alumno_id',
        string='Matrículas'
    )
    factura_ids = fields.One2many(
        comodel_name='factura.academica',
        inverse_name='alumno_id',
        string='Facturas'
    )
    
    @api.depends('nombre', 'apellidos')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.nombre} {record.apellidos}"


class SesionAlumno(models.Model):
    _name = 'sesion.alumno'
    _description = 'Matrícula de Alumno en Sesión'
    _rec_name = 'name'

    name = fields.Char(string='Referencia', compute='_compute_name')

    sesion_id = fields.Many2one(
        comodel_name='sesion.academica',
        string='Sesión',
        required=True,
        ondelete='cascade'
    )
    alumno_id = fields.Many2one(
        comodel_name='alumno.academico',
        string='Alumno',
        required=True,
        ondelete='cascade'
    )
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('pagada', 'Pagada'),
    ], string='Estado', default='borrador', required=True)
    fecha_inscripcion = fields.Date(
        string='Fecha de Inscripción',
        default=fields.Date.today
    )
    
    _sql_constraints = [
        ('unique_matricula', 'UNIQUE(sesion_id, alumno_id)',
         'El alumno ya está matriculado en esta sesión')
    ]
    
    def confirmar_matricula(self):
        """Cambiar estado a Confirmada"""
        self.estado = 'confirmada'
    
    def pagar_matricula(self):
        """Cambiar estado a Pagada"""
        self.estado = 'pagada'
        
    @api.depends('alumno_id.name', 'sesion_id.name')
    def _compute_name(self):
        for record in self:
            alumno = record.alumno_id.name if record.alumno_id else 'Borrador'
            sesion = record.sesion_id.name if record.sesion_id else ''
            record.name = f"Matrícula: {alumno}"


class FacturaAcademica(models.Model):
    _name = 'factura.academica'
    _description = 'Factura Académica'

    cantidad = fields.Float(string='Cantidad', required=True)
    fecha_pago = fields.Date(string='Fecha de Pago')
    concepto = fields.Text(string='Concepto')
    
    # Relación con estudiante
    alumno_id = fields.Many2one(
        comodel_name='alumno.academico',
        string='Alumno',
        required=True,
        ondelete='cascade'
    )
