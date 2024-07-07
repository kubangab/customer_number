from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_number_digits = fields.Integer(related='company_id.customer_number_digits', readonly=False)
    customer_number_start = fields.Integer(related='company_id.customer_number_start', readonly=False)
    customer_number_padding = fields.Boolean(related='company_id.customer_number_padding', readonly=False)

class ResCompany(models.Model):
    _inherit = 'res.company'

    customer_number_digits = fields.Integer(string='Customer Number Digits', default=5)
    customer_number_start = fields.Integer(string='Starting Customer Number', default=1000)
    customer_number_padding = fields.Boolean(string='Use Leading Zeros', default=True)
