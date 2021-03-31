# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    parent_agent = fields.Many2one('res.partner', string='TL Agent', domain=[("agent", "=", True)])
    
    is_team_leader = fields.Boolean('Is Team Leader', 
                                    compute = 'on_change_parent_agent', 
                                    domain=[("agent", "=", True)], store = True)
    
    @api.depends('parent_agent')
    def on_change_parent_agent(self):
        for record in self:
            if record.parent_agent and not record.agent_ids:
                record.is_team_leader = False
            elif not record.parent_agent and record.agent_ids:
                record.is_team_leader = True
    

class SaleCommissionMixin(models.AbstractModel):
    _inherit = "sale.commission.mixin"
    
    ######## OverRide Function to add settlements to Parent Agents #########
    
    def _prepare_agents_vals_partner(self, partner):
        """Utility method for getting agents creation dictionary of a partner."""
        vals = []
        for agent in partner.agent_ids:
            if agent.parent_agent:
                vals.append((0, 0, self._prepare_agent_vals(agent.parent_agent)))
            vals.append((0, 0, self._prepare_agent_vals(agent)))
        return vals
    
    
class SaleOrderLineAgent(models.Model):
    _inherit = "sale.order.line.agent"
    
    temp_commission_id = fields.Many2one(
        comodel_name="sale.commission",
        ondelete="restrict",
        readonly=False,
        copy=True,
    )
    
    @api.depends(
        "object_id.price_subtotal", "object_id.product_id", "object_id.product_uom_qty"
    )
    def _compute_amount(self):
    ################## Change the calculation of commission
    ################## If agent has a TL Agent (parent_agent)
    ################## If agent got commission 5%
    ################## Then TL agent gets 15 % (20% - 5%)
        team_leader_id = self.agent_id.mapped('parent_agent')
        temp_commission_id = team_leader_id.commission_id
        for line in self:
            if line.agent_id.parent_agent.id == team_leader_id.id:
                if line.agent_id.commission_id.commission_type == "fixed":
                    temp_commission_id.not_fix_qty = \
                            temp_commission_id.fix_qty - line.agent_id.commission_id.fix_qty

        for line in self:
            order_line = line.object_id
            line.amount = line._get_commission_amount(
                line.commission_id,
                order_line.price_subtotal,
                order_line.product_id,
                order_line.product_uom_qty,
            )
            line.commission_id.not_fix_qty = 0
    
class AccountInvoiceLineAgent(models.Model):
    _inherit = "account.invoice.line.agent"
    
    temp_commission_id = fields.Many2one(
        comodel_name="sale.commission",
        ondelete="restrict",
        readonly=False,
        copy=True,
    )
    
    
    @api.depends("object_id.price_subtotal", "object_id.product_id.commission_free")
    def _compute_amount(self):
        
        team_leader_id = self.agent_id.mapped('parent_agent')
        temp_commission_id = team_leader_id.commission_id
        for line in self:
            if line.agent_id.parent_agent.id == team_leader_id.id:
                if line.agent_id.commission_id.commission_type == "fixed":
                    temp_commission_id.not_fix_qty = \
                            temp_commission_id.fix_qty - line.agent_id.commission_id.fix_qty
        for line in self:
            inv_line = line.object_id
            line.amount = line._get_commission_amount(
                line.commission_id,
                inv_line.price_subtotal,
                inv_line.product_id,
                inv_line.quantity,
            )
            line.commission_id.not_fix_qty = 0
            # Refunds commissions are negative
            if line.invoice_id.type and "refund" in line.invoice_id.type:
                line.amount = -line.amount
        