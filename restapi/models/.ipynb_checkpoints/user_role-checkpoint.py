from odoo import models, fields, api


class restapi(models.Model):
    _inherit = 'res.users'
    
    user_role = fields.Selection([
        ('sales', 'Sales'),
        ('dicoration_engineer', 'Dicoration Engineer')],string='User Role')
    