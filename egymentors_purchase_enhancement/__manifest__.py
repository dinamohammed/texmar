# -*- coding: utf-8 -*-
{
    'name': "EgyMentors Purchase Enhancement",
    'author': 'EgyMentors, Dalia Atef',
    'category': 'Purchase',
    'summary': """Purchase Enhancement""",
    'website': 'http://www.egymentors.com',
    'license': 'AGPL-3',
    'description': """
""",
    'version': '10.0',
    'depends': ['egymentors_purchase_fx'],
    'data': [
        'security/ir.model.access.csv',

        'reports/report.xml',
        'reports/purchase_report_changes.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
