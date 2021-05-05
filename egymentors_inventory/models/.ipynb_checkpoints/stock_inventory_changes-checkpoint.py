# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning
# Ahmed Salama Code Start ---->


class StockInventoryInherit(models.Model):
	_inherit = 'stock.inventory'
	
	ref = fields.Char("Code")
	
	def action_validate(self):
		self.ref = self.env['ir.sequence'].next_by_code('stock.inventory.code') or _('New')
		return super(StockInventoryInherit, self).action_validate()

# Ahmed Salama Code End.
