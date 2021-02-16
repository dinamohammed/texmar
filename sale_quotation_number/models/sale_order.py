# © 2010-2012 Andy Lu <andy.lu@elico-corp.com> (Elico Corp)
# © 2013 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2017 valentin vinagre  <valentin.vinagre@qubiq.es> (QubiQ)
# © 2020 Manuel Regidor  <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        company = vals.get("company_id", False)
#         branch = vals.get("branch_id", False)
#         if branch:
#             branch_2 = self.env["res.branch"].browse(branch)
#             vals["name"] = self.env["ir.sequence"].next_by_code(branch_2.sequence_code) or "New"
#             return super(SaleOrder, self).create(vals)
#         else:
        if company:
            company = self.env["res.company"].browse(company)
        else:
            company = self.env.company
        if self.env.user.branch_id or self.env.user.branch_ids:
            vals["name"] = self.env["ir.sequence"].next_by_code("note.order") or "/"
        else:
            if not company.keep_name_so:
                vals["name"] = self.env["ir.sequence"].next_by_code("sale.quotation") or "/"
        return super(SaleOrder, self).create(vals)

#     def copy(self, default=None):
#         self.ensure_one()
#         if default is None:
#             default = {}
#         default["name"] = "/"
#         if self.origin and self.origin != "":
#             default["origin"] = self.origin + ", " + self.name
#         else:
#             default["origin"] = self.name
#         return super(SaleOrder, self).copy(default)

    def action_confirm(self):
        for order in self:
            if order.state in ("draft", "sent") and not order.company_id.keep_name_so:
                if order.origin and order.origin != "":
                    quo = order.origin + ", " + order.name
                else:
                    quo = order.name
                order.sudo().write(
                    {
                        "origin": quo,
                        "name": self.env["ir.sequence"].next_by_code("sale.order"),
                    }
                )
        return super(SaleOrder,self).action_confirm()

    

# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
    
    
#     @api.model
#     def create(self, vals):
#         if self.branch_id:
#             if vals.get('name', 'New') == 'New':
#                 seq_date = None
#                 if 'date_order' in vals:
#                     seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
#                 vals['name'] = self.env['ir.sequence'].next_by_code(self.branch_id.sequence_code, sequence_date=seq_date) or '/'
#             return super(PurchaseOrder, self).create(vals)
#         else:
#             if vals.get('name', 'New') == 'New':
#                 seq_date = None
#                 if 'date_order' in vals:
#                     seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
#                 vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'
#             return super(PurchaseOrder, self).create(vals)

    