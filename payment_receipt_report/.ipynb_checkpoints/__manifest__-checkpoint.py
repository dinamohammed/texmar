# -*- coding: utf-8 -*-
{
    'name': "Payment Receipt Report",

    'summary': """
        A customized report for payment receipts""",

    'description': """
        A customized report for payment receipts
    """,

    'author': "Egymentors@MuhammedAshraf9244",
    'website': "https://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/payment_receipt_report.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
