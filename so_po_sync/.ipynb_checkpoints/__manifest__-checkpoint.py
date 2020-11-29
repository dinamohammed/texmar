# -*- coding: utf-8 -*-
{
    'name': "So Po Sync",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'website':'egymentors.com',

    'author': "egy mentors - hatem",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'company':'egy mentors',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','sale','stock','mrp','duplicate_fields','sale_quotation_number'],

    # always loaded
    'data': [
        'views/purchase.xml',
        'views/delivery.xml',
        'views/sales.xml',
        'views/mrp.xml',
        'views/templates.xml',
    ],

}