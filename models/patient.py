from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError, UserError

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer()
    
    # New fields
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined', tracking=True)
    
    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', readonly=True)
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Logs')
    
    # Constraints
    @api.constrains('department_id')
    def _check_department_is_opened(self):
        for patient in self:
            if patient.department_id and not patient.department_id.is_opened:
                raise ValidationError(_('Cannot assign patient to a closed department.'))
    
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise ValidationError(_('CR Ratio is required when PCR is checked.'))
    
    # Onchange methods
    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            # Enable doctors selection when department is selected
            return {'readonly': {'doctor_ids': False}}
    
    @api.onchange('age')
    def _onchange_age(self):
        # Hide history if age < 50
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': _('PCR Checked'),
                    'message': _('PCR has been automatically checked because age is less than 30.')
                }
            }
    
    # Create and write overrides for logging
    def create(self, vals):
        patient = super(Patient, self).create(vals)
        self.env['hms.patient.log'].create({
            'description': 'Patient created',
            'patient_id': patient.id,
        })
        return patient
    
    def write(self, vals):
        # Check if state has changed
        if 'state' in vals:
            old_state = self.state
            new_state = vals['state']
            if old_state != new_state:
                self.env['hms.patient.log'].create({
                    'description': f'State changed to {dict(self._fields["state"].selection).get(new_state)}',
                    'patient_id': self.id,
                })
        return super(Patient, self).write(vals)