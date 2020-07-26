# -*- coding: utf-8 -*-
{
    'name': "Reports Texmar",

    'summary': """
        Edit in Multiple reports and print outs""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant','account','account_check'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/account_payment_reports.xml',
        'views/account_check_reports.xml',
    ],
}
