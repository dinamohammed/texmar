# -*- coding: utf-8 -*-
{
    'name': "EgyMentors Accounting Enhancement",
    'author': 'EgyMentors, Dalia Atef',
    'category': 'Accounting',
    'summary': """Accounting Enhancement""",
    'website': 'http://www.egymentors.com',
    'license': 'AGPL-3',
    'description': """
""",
    'version': '10.0',
    'depends': ['account', 'sale_discount_total', 'purchase_discount','account'],
    'data': [
        'reports/reports.xml',
        'reports/invoice_report.xml',
        'views/signs.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
