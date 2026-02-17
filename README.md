## 🔒 Resolución de Restricciones y Validaciones

A continuación se detalla técnicamente cómo se han implementado las restricciones de negocio para garantizar la integridad de los datos en los módulos de gestión académica.

### 1. Control de Aforo en Sesiones (Capacidad)
**Restricción:** No se permite que el número de alumnos inscritos supere la capacidad máxima (asientos) definidos para una sesión.

*   **Implementación:** [.py](cci:7://file:///c:/odoo-dev/odoo/modelos/gestion_academica/__init__.py:0:0-0:0) (Python Constraint)
*   **Modelo:** `sesion.academica`
*   **Método:** `@api.constrains('numero_alumnos', 'numero_asientos')`
*   **Lógica:** Se compara dinámicamente el campo computado [numero_alumnos](cci:1://file:///c:/odoo-dev/odoo/modelos/gestion_academica/models/models.py:134:4-143:17) con el límite `numero_asientos`. Si el primero es mayor, se lanza una excepción `ValidationError` impidiendo el guardado del registro.

```python
@api.constrains('numero_alumnos', 'numero_asientos')
def _check_numero_alumnos(self):
    for sesion in self:
        if sesion.numero_alumnos > sesion.numero_asientos:
            raise ValidationError(f"No se pueden inscribir más alumnos ({sesion.numero_alumnos}) que asientos disponibles ({sesion.numero_asientos})")
```

### 2. Unicidad de Matrícula (Doble Inscripción)
**Restricción:** Un mismo alumno no puede matricularse más de una vez en la misma sesión académica.

*   **Implementación:** SQL Constraint
*   **Modelo:** `sesion.alumno`
*   **Método:** `@api.constrains('numero_alumnos', 'numero_asientos')`
*   **Lógica:** Se ha definido una restricción única compuesta (composite unique key) en la base de datos PostgreSQL que involucra los campos sesion_id y alumno_id. Esto garantiza la integridad a nivel de base de datos, siendo más rápido y seguro que una comprobación en Python.

```python
_sql_constraints = [
    ('unique_matricula', 'UNIQUE(sesion_id, alumno_id)', 'El alumno ya está matriculado en esta sesión')
]
```
### 3. Gestión de Conflictos de Horario Profesores

**Restricción:** Un profesor no puede impartir clase en dos grupos diferentes que coincidan en el mismo tramo horario.

*   **Implementación:** [.py](cci:7://file:///c:/odoo-dev/odoo/modelos/gestion_academica/__init__.py:0:0-0:0) (Python Constraint)
*   **Modelo:** `grupo.clase`
*   **Método:** `@api.constrains('profesor_id', 'horario')`
*   **Lógica:** Antes de asignar un grupo a un profesor, el sistema realiza una búsqueda (search) en todos los grupos existentes para verificar si ese profesor (profesor_id) ya tiene asignada una clase en el mismo horario (horario), excluyendo el registro actual. Si se encuentra coincidencia, se bloquea la operación.

```python
@api.constrains('profesor_id', 'horario')
def _check_profesor_schedule(self):
    # Búsqueda de solapamientos
    conflictos = self.search([
        ('profesor_id', '=', grupo.profesor_id.id),
        ('horario', '=', grupo.horario),
        ('id', '!=', grupo.id)
    ])
    if conflictos:
        raise ValidationError(...)
```

