# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class QuantityInWords(models.Model):
    _inherit = 'stock.move'

    quantity_in_words = fields.Char(string="Quantity in Words" , readonly=True)

    @api.depends('product_uom_qty')
    def _onchange_quantity(self):
        res = QuantityInWords, self._onchange_quantity()
        for qty in self:
            amount_text = self.product_uom.with_context({'lang': self.env.user.lang}).amount_to_text(
			qty.product_uom_qty)
            if qty.env.user.lang in ['ar', 'ar_SY', 'ar_001']:
                quantity_in_words = "%s %s" % (amount_text, "فقط")
                quantity_in_words = str(quantity_in_words).replace('Units', 'وحده')
            else:
                quantity_in_words = amount_text + ' only'

            qty.quantity_in_words = quantity_in_words
        return res
    
    def set_quantity_in_words(self):
        for quantity in self:
            quantity.quantity_in_words = quantity.quantity_in_words(quantity.product_uom_qty)