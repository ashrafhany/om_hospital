from odoo import api, models, fields

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Doctor'
    
    name = fields.Char(string='Name', required=True, tracking=True)
    image = fields.Binary(string='Doctor Image')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    specialization = fields.Selection([
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('surgery', 'Surgery'),
        ('urology', 'Urology'),
        ('other', 'Other')
    ], string='Specialization', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    address = fields.Text(string='Address')
    note = fields.Text(string='Note')
    appointment_ids = fields.One2many('hospital.appointment', 'doctor_id', string='Appointments')
    active = fields.Boolean(string='Active', default=True)
    # Only uncomment this if you have the HR module installed
    # employee_id = fields.Many2one('hr.employee', string='Related Employee')
    consultation_fee = fields.Float(string='Consultation Fee')
    years_of_experience = fields.Integer(string='Years of Experience')
    license_number = fields.Char(string='License Number')
    available_days = fields.Char(string='Available Days')
    department_id = fields.Many2one('hospital.department', string='Department')
