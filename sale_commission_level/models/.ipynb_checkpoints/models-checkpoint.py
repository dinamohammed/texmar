# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    parent_agent = fields.Many2one('res.partner',string='TL Agent')
    

class SaleCommissionMixin(models.AbstractModel):
    _inherit = "sale.commission.mixin"
    
    ######## OverRide Function to add settlements to Parent Agents #########
    
    def _prepare_agents_vals_partner(self, partner):
        """Utility method for getting agents creation dictionary of a partner."""
        vals = []
        for agent in partner.agent_ids:
            if agent.parent_agent:
                vals.vals.append((0, 0, self._prepare_agent_vals(agent.parent_agent)))
            vals.append((0, 0, self._prepare_agent_vals(agent)))
        return vals