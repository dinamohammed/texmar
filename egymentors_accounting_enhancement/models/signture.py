from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from odoo.exceptions import ValidationError
from datetime import timedelta

class customer(models.Model):
    _inherit = 'account.move'
    
    name_sig = fields.Boolean('Name Signture',default=True)
    id_sig = fields.Boolean('ID Signture',default=True)
    signture_sig = fields.Boolean('Signture',default=True)
    accounting_sig = fields.Boolean('Accounting Signture',default=True)
    ledger_sig = fields.Boolean('Genral Ledger Signture',default=True)
    