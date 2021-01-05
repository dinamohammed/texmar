# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class ResUsers(models.Model):
    _inherit = 'res.users'

    user_product_ids = fields.Many2many(
        'product.category',
        'product_category_user_rel',
        'user_id',
        'product_category_id',
        'Allowed Categories')
    
    category_type = fields.Selection([('fabric', 'Fabric'),
                                      ('yarn', 'Yarn'),
                                      ('other', 'Other'),
                                      ('not', 'Un-Specified')], "Category Type", default='not')
    
    