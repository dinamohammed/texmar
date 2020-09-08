# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools.misc import formatLang




class PurchaseOrderTaxes(models.Model):
	_inherit = 'purchase.order'
    
    
	def purchase_taxes(self):
		tax_obj = self.env['account.tax']
		for order in self:
			taxes_dict = []
			taxes = []
			# Group taxes
			for line in order.order_line:
				if line.taxes_id:
					for tax_id in line.taxes_id.ids:
						if tax_id not in taxes:
							taxes.append(tax_id)
			if taxes:
				for tax_id in taxes:
					tax = tax_obj.browse(tax_id)
					tax_amount = 0
					for line in order.order_line:
						if tax_id in line.taxes_id.ids:
							vals = line._prepare_compute_all_values()
							taxes = tax.compute_all(
								vals['price_unit'],
								vals['currency_id'],
								vals['product_qty'],
								vals['product'],
								vals['partner'])
							tax_amount += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
					taxes_dict.append({
						'tax_name': tax.name,
						'tax_amount': tax_amount,
					})
			return taxes_dict
	
	# TODO: ADD SECTOR FOR TAXES SUCH AS INVOICE
	amount_by_group = fields.Binary(string="Tax amount by group",
	                                compute='compute_purchase_taxes_by_group')
	
	@api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.taxes_id',
	             'amount_tax', 'partner_id', 'currency_id')
	def compute_purchase_taxes_by_group(self):
		''' Helper to get the taxes grouped according their account.tax.group.
        This method is only used when printing the invoice.
        '''
		for order in self:
			lang_env = order.with_context(lang=order.partner_id.lang).env
			tax_lines = order.order_line.filtered(lambda line: line.taxes_id.ids != [])
			res = {}
			# There are as many tax line as there are repartition lines
			done_taxes = set()
			for line in tax_lines:
				for tax_id in line.taxes_id:
					tax_dict = tax_id.compute_all(line.price_unit, line.currency_id,
					                              line.product_qty, line.product_id,
					                              order.partner_id).get('taxes', [])[0]
					print("tax_dict: ", tax_dict)
					if tax_dict:
						price_tax = tax_dict.get('amount')
						res.setdefault(tax_id.tax_group_id, {'base': 0.0, 'amount': 0.0})
						res[tax_id.tax_group_id]['amount'] += price_tax
						tax_key_add_base = tuple(order._get_tax_key_for_group_add_base(line))
						if tax_key_add_base not in done_taxes:
							if line.currency_id != self.company_id.currency_id:
								amount = self.company_id.currency_id._convert(price_tax, line.currency_id,
								                                              self.company_id, fields.Date.today())
							else:
								amount = price_tax
							res[tax_id.tax_group_id]['base'] += amount
							# The base should be added ONCE
							done_taxes.add(tax_key_add_base)
			res = sorted(res.items(), key=lambda l: l[0].sequence)
			order.amount_by_group = [(
				group.name, amounts['amount'],
				amounts['base'],
				formatLang(lang_env, amounts['amount'], currency_obj=order.currency_id),
				formatLang(lang_env, amounts['base'], currency_obj=order.currency_id),
				len(res),
				group.id
			) for group, amounts in res]    
            
	@api.model
	def _get_tax_key_for_group_add_base(self, line):
		"""
        Useful for compute_purchase_taxes_by_group
        must be consistent with _get_tax_grouping_key_from_tax_line
         @return list
        """
		return line.taxes_id.ids