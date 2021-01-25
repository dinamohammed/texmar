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

    
class ResUsers(models.Model):
    _inherit = 'stock.picking'
    
#     category_type = fields.Selection(related='move_ids_without_package.product_id.categ_id.category_type', 
#                                      string= "Category Type",store=True)
    
    category_type = fields.Selection([('fabric', 'Fabric'),
                                      ('yarn', 'Yarn'),
                                      ('other', 'Other'),
                                      ('not', 'Un-Specified')], "Category Type", default='not', store= True
                                     , compute = 'onchange_category_type')
    
    @api.onchange('move_ids_without_package')
    def onchange_category_type(self):
        for line in self:
            for move in line.move_ids_without_package:
                if move.product_id.categ_id.category_type:
                    line['category_type'] = move.product_id.categ_id.category_type
