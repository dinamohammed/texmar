# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

{
    'name': "EgyMentors Inventory Enhancement[ercac]",
    'author': 'EgyMentors, Ahmed Salama',
    'category': 'Inventory',
    'summary': """Inventory Enhancement""",
    'website': 'http://www.egymentors.com',
    'license': 'AGPL-3',
    'description': """
""",
    'version': '10.0',
    'depends': ['base', 'stock', 'purchase', 'report_xlsx', 'purchase_discount', 'egymentors_product_code', 'sales_custome'],
    'data': [
        'reports/reports.xml',
        'reports/delivery_slip_report.xml',
        
        'views/quantity_in_words.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
