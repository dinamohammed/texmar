# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomTemplate(models.Model):
    _name = 'custom.template'
    
    name = fields.Char('Template Name')
    template_id = fields.Char('Template External ID')
    
