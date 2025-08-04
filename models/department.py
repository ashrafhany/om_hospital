from odoo import api, models, fields

class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active', default=True)
    note = fields.Text(string='Note')
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors')
