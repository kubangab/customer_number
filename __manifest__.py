{
    'name': 'Customer Number',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add Customer Number field to partners',
    'description': """
        This module adds a Customer Number field to partners and displays it on invoices.
    """,
    'depends': ['base', 'account'],
    'data': [
        'views/res_partner_views.xml',
        'reports/invoice_report_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
