# -*- coding: utf-8 -*-
{
    'name': "Note Order",

    'summary': """
        Adding the Note Order stage to Sales Order""",

    'description': """
        Branch companies now have an additional Note Order stage in the Sales Order
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_management','purchase','sale_quotation_number'],

    # always loaded
    'data': [
#         'security/ir.model.access.csv',
        'data/irsequence.xml',
        'views/views.xml',
#         'views/templates.xml',
    ],

}
