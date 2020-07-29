# -*- coding: utf-8 -*-
{
    'name': "Sale Stock Manfacturing",

    'summary': """ Adds the Size of Pieces fields in the Produce & Transfer Screens
        """,

    'description': """
        Adds the Size of Pieces fields in the Manufacturing Produce, Manufacturing Order & Sales Order/Purchase Order Transfer Screens
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'sale_management', 'stock_picking_batch', 'sale_stock', 'purchase', 'purchase_stock'],

    # always loaded
    'data': [
        'views/stock_picking_inherit_view.xml',
        'views/mrp_product_produce_inherit_view.xml',
        
        'wizard/mrp_product_produce_inherit_view.xml',
    ],

}
