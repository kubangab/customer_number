from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestCustomerNumber(TransactionCase):

    def setUp(self):
        super(TestCustomerNumber, self).setUp()
        self.Partner = self.env['res.partner']
        self.company = self.env.company

        # Set up configuration parameters
        self.env['ir.config_parameter'].sudo().set_param('customer_number.generation', 'auto')
        self.env['ir.config_parameter'].sudo().set_param('customer_number.digits', '5')
        self.env['ir.config_parameter'].sudo().set_param('customer_number.start', '1000')
        self.env['ir.config_parameter'].sudo().set_param('customer_number.padding', 'True')

    def test_01_create_company_partner_auto_generation(self):
        partner = self.Partner.create({
            'name': 'Test Company',
            'is_company': True,
        })
        self.assertTrue(partner.customer_number, "Customer number should be automatically generated")
        self.assertEqual(partner.customer_number, '01000', "First customer number should be 01000")

    ''''
    def test_02_create_multiple_company_partners(self):
        partners = self.Partner.create([
            {'name': 'Company 1', 'is_company': True},
            {'name': 'Company 2', 'is_company': True},
            {'name': 'Company 3', 'is_company': True},
        ])
        self.assertEqual(partners[0].customer_number, '01000')
        self.assertEqual(partners[1].customer_number, '01001')
        self.assertEqual(partners[2].customer_number, '01002')
    ''''

    def test_03_create_individual_partner(self):
        partner = self.Partner.create({
            'name': 'John Doe',
            'is_company': False,
        })
        self.assertFalse(partner.customer_number, "Individual partner should not have a customer number")

    def test_04_unique_customer_number(self):
        self.Partner.create({
            'name': 'Test Company 1',
            'is_company': True,
            'customer_number': '12345',
        })
        with self.assertRaises(ValidationError):
            self.Partner.create({
                'name': 'Test Company 2',
                'is_company': True,
                'customer_number': '12345',
            })

    def test_05_manual_customer_number_generation(self):
        # Set generation mode to manual
        self.env['ir.config_parameter'].sudo().set_param('customer_number.generation', 'manual')
        partner = self.Partner.create({
            'name': 'Manual Company',
            'is_company': True,
        })
        self.assertFalse(partner.customer_number, "Customer number should not be generated in manual mode")
        
        # Generate customer number manually
        partner.action_generate_customer_number()
        self.assertTrue(partner.customer_number, "Customer number should be generated after manual action")

    def test_06_padding_configuration(self):
        # Disable padding
        self.env['ir.config_parameter'].sudo().set_param('customer_number.padding', 'False')
        partner = self.Partner.create({
            'name': 'No Padding Company',
            'is_company': True,
        })
        self.assertEqual(partner.customer_number, '1000', "Customer number should not be padded")

        # Re-enable padding
        self.env['ir.config_parameter'].sudo().set_param('customer_number.padding', 'True')
        partner = self.Partner.create({
            'name': 'Padding Company',
            'is_company': True,
        })
        self.assertEqual(partner.customer_number, '01001', "Customer number should be padded")
