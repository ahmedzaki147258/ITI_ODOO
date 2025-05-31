from odoo import models, fields, api

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer()