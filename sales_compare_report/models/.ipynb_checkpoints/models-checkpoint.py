# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    product_reference = fields.Char(related = "product_id.default_code", store = True)
    product_name = fields.Char(related = "product_id.name", store = True)
    product_qty_on_hand = fields.Float(related = "product_id.qty_available", store = True)
    remaining_qty = fields.Char("Remaining Qty", compute = "_return_remaining_qty", store = True)
    product_color = fields.Char("Color", compute = "_return_product_color", store = True)
    
    approve_date = fields.Datetime(related = "order_id.date_approve")
    product_market = fields.Integer("Market")
    product_gallery = fields.Integer("Gallery")
    product_dealer = fields.Integer("Dealer")
    
    @api.depends('product_qty','qty_received')
    def _return_remaining_qty(self):
        for line in self:
            line.remaining_qty = line.product_qty - line.qty_received
    
    @api.depends('product_id')
    def _return_product_color(self):
        for line in self:
            product = line.product_id
            color_attr = self.env.ref('product.product_attribute_2')
            for attribute in product.product_template_attribute_value_ids:
                if attribute.attribute_id == color_attr \
                            and attribute.product_attribute_value_id:
                    line.product_color = attribute.product_attribute_value_id.name.split('-')[1]
                    
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    product_color = fields.Char("Color", compute = "_return_product_color", store = True)
    
    total_market = fields.Integer('Current Year Market', compute = '_get_total_values_current_year', store = True)
    total_gallery = fields.Integer('Current Year Gallery', compute = '_get_total_values_current_year', store = True)
    total_dealer = fields.Integer('Current Year Dealer', compute = '_get_total_values_current_year', store = True)
    
    last_total_market = fields.Integer('Last Year Market', compute = '_get_total_values_last_year', store = True)
    last_total_gallery = fields.Integer('Last Year Gallery', compute = '_get_total_values_last_year', store = True)
    last_total_dealer = fields.Integer('Last Year Dealer', compute = '_get_total_values_last_year', store = True)
    
#     @api.depends('')
    def _get_total_values_current_year(self):
        from_date = datetime. strptime('01/01/%s'%datetime.today().year, '%d/%m/%Y')
        to_date = datetime. strptime('31/12/%s'%datetime.today().year, '%d/%m/%Y')
        for product in self:
            total_m = total_g = total_d = 0
            sale_order_lines = self.env['sale.order.line'].search([('product_id','=',product.id),
                                                                   ('create_date','>=',from_date),
                                                                  ('create_date','<=',to_date)])
            for sol in sale_order_lines:
                if sol.is_market:
                    total_m += 1
                elif sol.is_gallery:
                    total_g += 1
                elif sol.is_dealer:
                    total_d += 1
            product.total_market = total_m
            product.total_gallery = total_g
            product.total_dealer = total_d
    
    def _get_total_values_last_year(self):
        from_date = datetime. strptime('01/01/%s'%(datetime.today().year-1), '%d/%m/%Y')
        to_date = datetime. strptime('31/12/%s'%(datetime.today().year-1), '%d/%m/%Y')
        for product in self:
            total_m = total_g = total_d = 0
            sale_order_lines = self.env['sale.order.line'].search([('product_id','=',product.id),
                                                                   ('create_date','>=',from_date),
                                                                  ('create_date','<=',to_date)])
            for sol in sale_order_lines:
                if sol.is_market:
                    total_m += 1
                elif sol.is_gallery:
                    total_g += 1
                elif sol.is_dealer:
                    total_d += 1
            product.last_total_market = total_m
            product.last_total_gallery = total_g
            product.last_total_dealer = total_d
            
        
    
    
    @api.depends('product_template_attribute_value_ids')
    def _return_product_color(self):
        for line in self:
            color_attr = self.env.ref('product.product_attribute_2')
            for attribute in line.product_template_attribute_value_ids:
                if attribute.attribute_id == color_attr \
                            and attribute.product_attribute_value_id:
                    line.product_color = attribute.product_attribute_value_id.name.split('-')[1]
                                        

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    is_market = fields.Boolean('Market', compute = '_get_bool_values', store = True)
    is_gallery = fields.Boolean('Gallery', compute = '_get_bool_values', store = True)
    is_dealer = fields.Boolean('Dealer', compute = '_get_bool_values', store = True)
    
    @api.depends('order_id.branch_id','salesman_id')
    def _get_bool_values(self):
        for line in self:
            if line.order_id.branch_id:
                line.is_gallery = True
            else:
                line.is_market = True
            if line.salesman_id:
                line.is_dealer = True
                
                
        