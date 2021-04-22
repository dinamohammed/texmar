# -*- coding: utf-8 -*-
{
    'name': "Sales Compare Report",

    'summary': """
        Sales Compare Report according to client's Needs.""",

    'description': """
        
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Reporting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','sale','purchase','report_xlsx','branch','sale_commission'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/sale_compare_report.xml',
        'reports/reports.xml',
        'wizard/products_wizard_view.xml',
        'views/product_purchase_report.xml',
    ],
}
