# -*- coding: utf-8 -*-
{
    'name': "Stock Move Filter Report",

    'summary': """
        Create Stock move report filter by product""",

    'description': """
        in Inventory we need to modify "Filter Pickings with Product"
        to collect per line and group by other criteria lik Branch,Date, order note
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Reporting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['branch','egymentors_purchase_fx','stock'],

    # always loaded
    'data': [
#         'security/ir.model.access.csv',
        'views/views.xml',
        'reports/stock_move_filtered_view.xml',
    ],
}
