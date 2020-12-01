# -*- coding: utf-8 -*-
{
    'name': "Discount Sale Purchase",

    'summary': """
        Adding Discount""",

    'description': """
        Adding Discount Per Line + Global Discount to Sale order and purchase order 
    """,

    'author': "Egmentors",
    'website': "http://www.egmentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
    ],
}
