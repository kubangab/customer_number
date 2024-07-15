from odoo import models, fields, api, _

class ManageCustomerNumber(models.TransientModel):
    _name = 'manage.customer.number'
    _description = 'Manage Customer Number'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    current_number = fields.Char(related='partner_id.customer_number', string='Current Number', readonly=True)
    action = fields.Selection([
        ('manual', _('Enter Manually')),
        ('generate', _('Generate New')),
        ('keep', _('Keep Current'))
    ], string='Action', required=True, default='keep')
    new_number = fields.Char(string='New Number')

    @api.onchange('action')
    def _onchange_action(self):
        if self.action == 'generate':
            self.new_number = self.env['res.partner']._get_next_customer_number()
        elif self.action == 'keep':
            self.new_number = False

    def apply_action(self):
        self.ensure_one()
        if self.action == 'manual' and self.new_number:
            padded_number = self._pad_customer_number(self.new_number)
            self.partner_id.customer_number = padded_number
        elif self.action == 'generate':
            self.partner_id.customer_number = self.env['res.partner']._get_next_customer_number()
        return {'type': 'ir.actions.act_window_close'}

    def _pad_customer_number(self, number):
        padding = self.env['ir.config_parameter'].sudo().get_param('customer_number.padding', 'True').lower() == 'true'
        digits = int(self.env['ir.config_parameter'].sudo().get_param('customer_number.digits', '5'))
        
        if padding:
            return number.zfill(digits)
        return number
