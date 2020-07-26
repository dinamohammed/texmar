# -*- coding: utf-8 -*-
{
    'name': "Available qty & Validation Button",

    'summary': """
        Task 3 Texmar Gap """,

    'description': """
        Create field available quantity , located in Main company only.
        Does computaions , Change colors of field values according to condition.
        Shift Validation button is sale Order
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

    # always loaded
    'data': [
        'views/sale_order_view.xml',
    ],

}
