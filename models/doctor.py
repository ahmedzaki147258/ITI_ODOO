from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Image(string='Image')
    
    # For display name purposes
    @api.depends('first_name', 'last_name')
    def name_get(self):
        result = []
        for doctor in self:
            name = f"{doctor.first_name} {doctor.last_name}"
            result.append((doctor.id, name))
        return result