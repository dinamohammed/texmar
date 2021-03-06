# -*- coding: utf-8 -*-
{
    'name': "Asset Location",

    'summary': """
        Create and Select Asset Locations""",

    'description': """
        Create and Select Asset Locations
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_accountant', 'account_asset'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/location.xml',
        'views/asset_view.xml',
    ],

}
