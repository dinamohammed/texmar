# -*- coding: utf-8 -*-
{
    'name': "Texmar Task3",

    'summary': """
        Shift Validation button is sale Order""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','stock'],
    
    'data': [
        'views/sale_order_view.xml',

    ],
}
