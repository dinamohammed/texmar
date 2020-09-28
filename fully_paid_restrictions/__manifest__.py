# -*- coding: utf-8 -*-
{
    'name': "Fuly Paid Restrictions",

    'summary': """
        In Sales Invoice Screen:
         Can’t Print This Invoice if Status is not Fully Paid
         Can’t Create Invoice if Sales Order is not Fully Paid     
       """,

    'description': """
        Sales Invoice Screen:
        Can’t Print This Invoice if Status is not Fully Paid
         Can’t Create Invoice if Sales Order is not Fully Paid
    """,

    'author': "Egymentors",
    'website': "https://www.egymentors.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock', 'sale', 'account_accountant','so_po_advance_payment_app','egymentors_purchase_fx'],

    # always loaded
    'data': [
       'views/view_account_invoice_print.xml',
    ],
    'installable':True,
    'auto_install':False,
    'application':True,

}