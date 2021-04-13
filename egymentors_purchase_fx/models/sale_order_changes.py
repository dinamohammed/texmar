# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.osv import expression
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


# Ahmed Salama Code Start ---->

# class SaleOrderType(models.Model):
#     _name = 'sale.order.type'
#     _description = "PO Type"

#     name = fields.Char(required=1)



class SaleOrderInherit(models.Model):
	_inherit = 'sale.order'
    
	order_status = fields.Selection([('open', 'Open'),
	                                 ('closed', 'Closed')], "Order Status", default='open')
	purchase_delivered = fields.Boolean("PO Qty Delivered",
	                                    help="Flag to show if there is related purchase order and if it's delivered")
	has_mto = fields.Boolean(compute='_check_lines_mto')
	hide_cancel = fields.Boolean("Hide Cancel?")
	stop_cancel_at = fields.Datetime("Stop Cancel")
# 	compute='compute_stop_cancel_at'
	
	display_name = fields.Char("Order", compute='get_display_name')
	po_type_id = fields.Many2one('purchase.order.type', "PO Type")
	fx_num_id = fields.Many2one('fx.number', "Fx/Production No.")
	
	@api.onchange('name', 'client_order_ref')
	def get_display_name(self):
		for order in self:
			display_name = ''
			if order.name:
				display_name = order.name
			if order.client_order_ref:
				display_name += '/' + order.client_order_ref
			order.display_name = display_name
	
# 	@api.onchange('date_order')
# 	def compute_stop_cancel_at(self):
# 		for order in self:
# 			order.stop_cancel_at = (order.date_order +
# 			                        relativedelta(days=1)).replace(hour=7, minute=0, second=0)
	
	@api.model
	def cron_stop_cancel_sale_order(self):
		orders = self.env['sale.order'].search([]). \
			filtered(lambda o: o.stop_cancel_at.date() == fields.Date.today())
		for order_id in orders:
			order_id.write({'hide_cancel': True})
	
	@api.onchange('order_line')
	def _check_lines_mto(self):
		for order in self:
			mto = self.env.ref('stock.route_warehouse0_mto')
			routes = order.order_line.mapped('product_id.route_ids.id')
			has_mto = False
			if mto.id in routes:
				has_mto = True
			order.has_mto = has_mto
	
	def action_view_delivered(self):
		action = self.env.ref('purchase.purchase_rfq').read()[0]
		action['domain'] = [('id', '=', self.purchase_delivered_id.id)]
		return action
	
	purchase_delivered_id = fields.Many2one('purchase.order', "PO Qty Delivered")
	
	def action_print(self):
		return self.env.ref('sale.action_report_saleorder').report_action(self)
	
	@api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('name', operator, name), ('client_order_ref', operator, name)]
		purchase_order_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
		return models.lazy_name_get(self.browse(purchase_order_ids).with_user(name_get_uid))
	
	@api.depends('name', 'client_order_ref')
	def name_get(self):
		result = []
		for so in self:
			name = so.name
			if so.client_order_ref:
				# origin = '#' in so.origin and so.origin.replace('#', '')
				name += '/' + so.client_order_ref
			
			result.append((so.id, name))
		return result
	
	def action_confirm(self):
		res = super(SaleOrderInherit, self).action_confirm()
		for rec in self:
			rec.picking_ids.write({'fx_pick_num_id': rec.fx_num_id.id})
			rec.picking_ids.move_ids_without_package.write({'fx_num_id': rec.fx_num_id.id})
		return res
	
class SaleOrderLineInherit(models.Model):
	_inherit = 'sale.order.line'
	
	line_status = fields.Selection([('open', 'Open'),
	                                ('closed', 'Closed')], "Status", default='open')
	is_cut = fields.Boolean("Cut", help="Flag to product lines which is cut")
	sample_date = fields.Date("Sample Date")
	line_delivery_date = fields.Date("Delivery Date")
	approval_status = fields.Selection([('approved', 'Approved'),
	                                    ('refused', 'Refused')], "Approval Status")
	
	branch_id = fields.Many2one(related = 'order_id.branch_id')
	
	def write(self, vals):
		"""
		Change Status Of SO
		:param vals:
		:return:
		"""
		super(SaleOrderLineInherit, self).write(vals)
		if vals.get('line_status'):
			# Check Other Lines:
			for line in self:
				if line.order_id:
					if all(line_status == 'closed' for line_status
					       in line.order_id.order_line.mapped('line_status')):
						status = 'closed'
					else:
						status = 'open'
					line.order_id.write({'order_status': status})
		return True
	
	def cut_lines(self):
		for line in self:
			line.is_cut = True
	
	def un_cut_lines(self):
		for line in self:
			line.is_cut = False
	
	def _prepare_procurement_group_vals(self):
		vals = super(SaleOrderLineInherit, self)._prepare_procurement_group_vals()
		name = self.order_id.name
		if self.order_id.client_order_ref:
			name += '/' + self.order_id.client_order_ref
		vals['name'] = name
		return vals
	
	def _prepare_procurement_values(self, group_id=False):
		values = super(SaleOrderLineInherit, self)._prepare_procurement_values(group_id)
		if self.line_delivery_date:
			values['date_planned'] = self.line_delivery_date
# 		if self.order_id.fx_num_id:
# 			values['fx_pick_num_id'] = self.order_id.fx_num_id.id
		return values
	
	def _action_launch_stock_rule(self, previous_product_uom_qty=False):
		"""
		Launch procurement group run method with required/custom fields genrated by a
		sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
		depending on the sale order line product rule.
		"""
		precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
		procurements = []
		for line in self:
			if line.state != 'sale' or not line.product_id.type in ('consu','product'):
				continue
			qty = line._get_qty_procurement(previous_product_uom_qty)
			if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
				continue
			
			group_id = line._get_procurement_group()
			if not group_id:
				group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
				line.order_id.procurement_group_id = group_id
			else:
				# In case the procurement group is already created and the order was
				# cancelled, we need to update certain values of the group.
				updated_vals = {}
				if group_id.partner_id != line.order_id.partner_shipping_id:
					updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
				if group_id.move_type != line.order_id.picking_policy:
					updated_vals.update({'move_type': line.order_id.picking_policy})
				if updated_vals:
					group_id.write(updated_vals)
			
			values = line._prepare_procurement_values(group_id=group_id)
			product_qty = line.product_uom_qty - qty
			
			line_uom = line.product_uom
			quant_uom = line.product_id.uom_id
			origin = line.order_id.name
			if line.order_id.client_order_ref:
				# origin = '#' in so.origin and so.origin.replace('#', '')
				origin += '/' + line.order_id.client_order_ref
			product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
			procurements.append(self.env['procurement.group'].Procurement(
				line.product_id, product_qty, procurement_uom,
				line.order_id.partner_shipping_id.property_stock_customer,
				line.name, origin, line.order_id.company_id, values))
		if procurements:
			self.env['procurement.group'].run(procurements)
		return True
	
	def _purchase_service_prepare_order_values(self, supplierinfo):
		""" Returns the values to create the purchase order from the current SO line.
		:param supplierinfo: record of product.supplierinfo
		:rtype: dict
		"""
		self.ensure_one()
		partner_supplier = supplierinfo.name
		fiscal_position_id = self.env['account.fiscal.position'].sudo().with_contex_prepare_procurement_valuest(company_id=self.company_id.id).get_fiscal_position(partner_supplier.id)
		date_order = self._purchase_get_date_order(supplierinfo)
# 		raise ValidationError('PO Type %s' %self.order_id.po_type_id.id)
		return {
			'partner_id': partner_supplier.id,
			'partner_ref': partner_supplier.ref,
			'company_id': self.company_id.id,
			'currency_id': partner_supplier.property_purchase_currency_id.id or self.env.company.currency_id.id,
			'dest_address_id': self.order_id.partner_shipping_id.id,
			'origin': self.order_id.name,
			'payment_term_id': partner_supplier.property_supplier_payment_term_id.id,
			'date_order': date_order,
			'fiscal_position_id': fiscal_position_id,
			'po_type_id': self.order_id.po_type_id.id,
			'fx_num_id': self.order_id.fx_num_id.id,
		}
	def _prepare_invoice_line(self):
		"""
		Prepare the dict of values to create the new invoice line for a sales order line.
		:param qty: float quantity to invoice
		"""
		self.ensure_one()
		return {
			'display_type': self.display_type,
			'sequence': self.sequence,
			'name': self.name,
			'product_id': self.product_id.id,
			'fx_num_id': self.order_id.fx_num_id.id,
			'product_uom_id': self.product_uom.id,
			'quantity': self.qty_to_invoice,
			'discount': self.discount,
			'price_unit': self.price_unit,
			'tax_ids': [(6, 0, self.tax_id.ids)],
			'analytic_account_id': self.order_id.analytic_account_id.id,
			'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
			'sale_line_ids': [(4, self.id)],
		}



# Ahmed Salama Code End.
