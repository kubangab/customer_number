from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_number = fields.Char(string=_('Customer Number'), copy=False)

    _sql_constraints = [
        ('customer_number_unique', 'unique(customer_number)', _('The customer number must be unique!'))
    ]

    @api.constrains('customer_number')
    def _check_customer_number(self):
        for partner in self:
            if partner.customer_number:
                if self.search_count([('customer_number', '=', partner.customer_number), ('id', '!=', partner.id)]) > 0:
                    raise ValidationError(_('The customer number must be unique!'))
