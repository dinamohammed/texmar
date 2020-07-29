from odoo import models, fields, api
from odoo.exceptions import ValidationError

class so_po_sync(models.Model):
    _inherit = 'mrp.production'

    notes = fields.Text(string='Terms and conditions',readonly=True)