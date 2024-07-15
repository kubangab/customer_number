{
    'name': 'Customer Number',
    'version': '17.0.1.0.4',
    'category': 'Sales',
    'summary': 'Add Customer Number field to partners',
    'description': """
        This module adds a Customer Number field to partners and displays it on invoices.
    """,
    'author': 'Lasse Larsson, Kubang AB',
    'website': 'https://www.kubang.eu',
    'depends': ['base', 'account','sale','contacts'],
    'data': [
        'security/customer_number_security.xml',
        'security/ir.model.access.csv',
	'wizards/manage_customer_number_view.xml',
        'views/res_partner_views.xml',
	'views/res_config_settings_views.xml',
        'reports/invoice_report_templates.xml',
	'wizards/update_customer_numbers_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
