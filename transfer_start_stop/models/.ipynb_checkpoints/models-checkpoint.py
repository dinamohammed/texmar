# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    cutting_state = fields.Selection([
        ('not', 'Not Cutten Yet'),
        ('cutting', 'Cutting'),
        ('finished', 'Finished Cutting')],
        'Cutting Status', default='not', readonly=True, tracking=True)
    
    
    def button_start_cutting(self):
        for line in self:
            line.write({'cutting_state':'cutting'})
            
    def button_resume_cutting(self):
        for line in self:
            line.write({'cutting_state':'cutting'})
            
    def button_stop_cutting(self):
        for line in self:
            line.write({'cutting_state':'finished'})
