from odoo import api, fields, models, _
from datetime import datetime


class settings_config(models.TransientModel):
    _inherit = "res.config.settings"
    assets_date = fields.Date(string='Assets Date')

    @api.model
    def get_values(self):
        res = super(settings_config, self).get_values()
        res['assets_date'] = self.env['ir.config_parameter'].\
                                       get_param('assets_date', default=datetime.today())
        return res

    def set_values(self):
        self.assets_date and self.env['ir.config_parameter'].\
            set_param('assets_date', self.assets_date)
        super(settings_config, self).set_values()
