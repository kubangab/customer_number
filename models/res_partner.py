from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_number = fields.Char(
        string=_('Customer Number'),
        copy=False,
        readonly=True,
        help=_("A unique identifier for this customer. This number will appear on invoices and is automatically generated for new customers.")
    )

    _sql_constraints = [
        ('customer_number_unique', 'unique(customer_number)', _('The customer number must be unique!'))
    ]

    @api.model_create_multi
    def create(self, vals):
        if vals.get('is_company', False) and not vals.get('customer_number'):
            vals['customer_number'] = self._get_next_customer_number()
        return super(ResPartner, self).create(vals)

    @api.model
    def _get_next_customer_number(self):
        company = self.env.company
        digits = company.customer_number_digits
        start = company.customer_number_start
        padding = company.customer_number_padding

        last_customer = self.search([('customer_number', '!=', False)], order='customer_number desc', limit=1)
        if last_customer:
            try:
                last_number = int(last_customer.customer_number)
                next_number = max(last_number + 1, start)
            except ValueError:
                next_number = start
        else:
            next_number = start

        if padding:
            return str(next_number).zfill(digits)
        else:
            return str(next_number)

    @api.constrains('customer_number', 'is_company')
    def _check_customer_number(self):
        for partner in self:
            if partner.is_company and not partner.customer_number:
                partner.customer_number = self._get_next_customer_number()
            if partner.customer_number:
                if self.search_count([('customer_number', '=', partner.customer_number), ('id', '!=', partner.id)]) > 0:
                    raise ValidationError(_('The customer number must be unique!'))

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('customer_number', operator, name)] + args
        return super(ResPartner, self).name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def _update_existing_customer_numbers(self):
        partners = self.search([('customer_number', '!=', False), ('is_company', '=', True)])
        for partner in partners:
            if partner.company_id.customer_number_padding:
                partner.customer_number = partner.customer_number.zfill(partner.company_id.customer_number_digits)
