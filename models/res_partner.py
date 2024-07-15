from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    customer_number = fields.Char(
        string='Customer Number',
        copy=False,
        readonly=True,
        help="A unique identifier for this customer. This number will appear on invoices if set."
    )
    
    _sql_constraints = [
        ('customer_number_company_uniq', 'UNIQUE(customer_number, company_id)',
         'The customer number must be unique per company!')
    ]

    def init(self):
        # Create a lock table if it doesn't exist
        self.env.cr.execute("""
            CREATE TABLE IF NOT EXISTS customer_number_lock (
                id serial PRIMARY KEY
            )
        """)

    
    @api.constrains('customer_number', 'company_id')
    def _check_unique_customer_number(self):
        for partner in self:
            if partner.customer_number:
                domain = [
                    ('customer_number', '=', partner.customer_number),
                    ('company_id', '=', partner.company_id.id),
                    ('id', '!=', partner.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(_('The customer number must be unique per company!'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_company'):
                if not vals.get('customer_number'):
                    generation_mode = self.env['ir.config_parameter'].sudo().get_param('customer_number.generation', 'manual')
                    if generation_mode == 'auto':
                        vals['customer_number'] = self._get_next_customer_number()
        partners = super(ResPartner, self).create(vals_list)
        return partners

    @api.model
    def _get_next_customer_number(self):
        digits = int(self.env['ir.config_parameter'].sudo().get_param('customer_number.digits', '5'))
        start = int(self.env['ir.config_parameter'].sudo().get_param('customer_number.start', '1000'))
        padding = self.env['ir.config_parameter'].sudo().get_param('customer_number.padding', 'True').lower() == 'true'

        # Lock the table to ensure only one transaction can generate the next number at a time
        self.env.cr.execute("LOCK TABLE customer_number_lock IN ACCESS EXCLUSIVE MODE")

        # Check for the maximum existing customer number
        self.env.cr.execute("""
            SELECT MAX(CAST(customer_number AS INTEGER))
            FROM res_partner
            WHERE customer_number ~ '^[0-9]+$'
        """)
        max_number = self.env.cr.fetchone()[0]

        # Use the start value if no customer numbers exist, otherwise continue from max_number
        if max_number is None:
            next_number = start
        else:
            next_number = max_number + 1

        if padding:
            result = str(next_number).zfill(digits)
        else:
            result = str(next_number)

        _logger.info(f"Generated customer number: {result}")
        return result

    def action_generate_customer_number(self):
        for partner in self:
            if partner.is_company and not partner.customer_number:
                partner.customer_number = self._get_next_customer_number()
                _logger.info(f"Generated customer number for existing partner: {partner.customer_number}")

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
