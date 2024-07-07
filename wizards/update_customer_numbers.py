from odoo import models, fields, api

class UpdateCustomerNumbers(models.TransientModel):
    _name = 'update.customer.numbers'
    _description = 'Update Customer Numbers'

    partner_count = fields.Integer(string='Partners to Update', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(UpdateCustomerNumbers, self).default_get(fields)
        res['partner_count'] = self.env['res.partner'].search_count([('is_company', '=', True), ('customer_number', '!=', False)])
        return res

    def action_update_customer_numbers(self):
        partners = self.env['res.partner'].search([('is_company', '=', True), ('customer_number', '!=', False)])
        for partner in partners:
            current_number = int(partner.customer_number)
            new_number = str(current_number).zfill(self.env.company.customer_number_digits)
            partner.write({'customer_number': new_number})
        return {'type': 'ir.actions.act_window_close'}
