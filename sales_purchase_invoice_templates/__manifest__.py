# -*- coding: utf-8 -*-
{
    'name': "Sales Purchase Invoice Templates",

    'summary': """
        Different Templates Per Order""",

    'description': """
        Field to assign different templates per Sale order, Purchase Order, or Invoice.
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','purchase','account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view_changes.xml',
        'views/sale_order_view_changes.xml',
        'views/invoice_view_changes.xml',
        'views/custom_template_view.xml',
    ],
}
