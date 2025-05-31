from odoo import models, fields, api

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'
    _order = 'create_date desc'
    
    description = fields.Text(string='Description')
    patient_id = fields.Many2one('hms.patient', string='Patient')
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)
    create_date = fields.Datetime(string='Created Date', readonly=True)