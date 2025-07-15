from odoo import api, models,fields

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital appointment'
    _rec_names_search = ['reference', 'patient_id']
    _rec_name = 'patient_id'
    
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True , ondelete='cascade')
    date_appointment = fields.Date(string='Date', tracking=True)
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string='Appointment Lines')
    total_quantity = fields.Float(string='Total Quantity', compute='_compute_total_quantity', store=True)
    date_of_birth = fields.Date(string='Date of Birth' , related='patient_id.date_of_birth')
    
    @api.model_create_multi
    def create(self, vals_list):
        print("Creating appointment with vals_list:", vals_list)
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        return super(HospitalAppointment, self).create(vals_list)
    
    @api.depends('appointment_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(line.quantity for line in record.appointment_line_ids)
    
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.reference} {record.patient_id.name if record.patient_id else 'Unknown Patient'}"

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            record.message_post(body="Appointment confirmed.")

    def action_ongoing(self):
        for record in self:
            record.state = 'ongoing'
            record.message_post(body="Appointment is now ongoing.")

    def action_done(self):
        for record in self:
            record.state = 'done'
            record.message_post(body="Appointment is done.")

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
            record.message_post(body="Appointment has been cancelled.")

class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'
    
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product' , required=True)
    quantity = fields.Float(string='Quantity', default=1.0)