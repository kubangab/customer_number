from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Add the new column if it doesn't exist
    cr.execute("ALTER TABLE res_partner ADD COLUMN IF NOT EXISTS effective_customer_number VARCHAR")
    
    # Update all effective customer numbers
    env['res.partner']._update_all_effective_customer_numbers()
