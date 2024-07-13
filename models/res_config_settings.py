from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_number_generation = fields.Selection([
        ('auto', 'Automatic'),
        ('manual', 'Manual with Button')
    ], string='Customer Number Generation', default='manual', config_parameter='customer_number.generation')
    customer_number_digits = fields.Integer(string='Customer Number Digits', default=5, config_parameter='customer_number.digits')
    customer_number_start = fields.Integer(string='Starting Customer Number', default=1000, config_parameter='customer_number.start')
    customer_number_padding = fields.Boolean(string='Use Leading Zeros', default=True, config_parameter='customer_number.padding')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        _logger.info(f"Retrieved config values: {res}")
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        _logger.info(f"Set config values: {self.customer_number_generation}, {self.customer_number_digits}, {self.customer_number_start}, {self.customer_number_padding}")

class ResCompany(models.Model):
    _inherit = 'res.company'

    customer_number_digits = fields.Integer(string='Customer Number Digits', default=5)
    customer_number_start = fields.Integer(string='Starting Customer Number', default=1000)
    customer_number_padding = fields.Boolean(string='Use Leading Zeros', default=True)
