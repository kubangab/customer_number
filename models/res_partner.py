from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    customer_number = fields.Char(
        string=_('Customer Number'),
        copy=False,
        readonly=False,
        help=_("A unique identifier for this customer. This number will appear on invoices if set.")
    )
    
    _sql_constraints = [
        ('customer_number_company_uniq', 'UNIQUE(customer_number, company_id)',
         _('The customer number must be unique per company!'))
    ]
    
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
                    raise exceptions.ValidationError(_('The customer number must be unique per company!'))
                        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            _logger.info(f"Creating partner with vals: {vals}")
            if vals.get('is_company'):
                _logger.info("Partner is a company")
                if not vals.get('customer_number'):
                    _logger.info("No customer number provided")
                    generation_mode = self.env['ir.config_parameter'].sudo().get_param('customer_number.generation', 'manual')
                    _logger.info(f"Generation mode: {generation_mode}")
                    if generation_mode == 'auto':
                        vals['customer_number'] = self._get_next_customer_number()
                        _logger.info(f"Generated customer number: {vals['customer_number']}")
        return super(ResPartner, self).create(vals_list)
    
    @api.model
    def _get_next_customer_number(self):
        digits = int(self.env['ir.config_parameter'].sudo().get_param('customer_number.digits', '5'))
        start = int(self.env['ir.config_parameter'].sudo().get_param('customer_number.start', '1000'))
        padding = self.env['ir.config_parameter'].sudo().get_param('customer_number.padding', 'True').lower() == 'true'
            
        _logger.info(f"Generating next customer number. Digits: {digits}, Start: {start}, Padding: {padding}")
            
        self.env.cr.execute("""
            SELECT MAX(CAST(customer_number AS INTEGER))
            FROM res_partner
            WHERE customer_number ~ '^[0-9]+$'
        """)
        max_number = self.env.cr.fetchone()[0] or start - 1
        next_number = max(max_number + 1, start)
            
        _logger.info(f"Next number before padding: {next_number}")
            
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