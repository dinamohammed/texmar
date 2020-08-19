# -*- coding: utf-8 -*-
{
    'name': "Note Order",

    'summary': """
        Create a new phase of Sale order called Note order""",

    'description': """
        Create a new phase of Sale order called Note order accordeing to client requirements
        to fulfil needs in POS, for casheir and customer.
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/note_order_view.xml',
        'views/note_order_line_view.xml',
    ],
}
