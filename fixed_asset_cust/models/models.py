# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools import format_date
from datetime import datetime

MAX_NAME_LENGTH = 50


class AccountMove(models.Model):
    _inherit = 'account.move'

    from_custom_asset = fields.Boolean(string='From Custom Asset', copy=False)
    asset_ref_id = fields.Many2one('account.asset', string='From Custom Asset', copy=False)


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    acc_nineteen = fields.Float(string='Accumulated', readonly=False)
#    hide_custom_button = fields.Boolean(string='Hide GL - 2019 Button', default=False, copy=False)

#    def open_asset_custom_entries(self):
#        return {
#            'name': _('Journal Entries'),
#            'view_mode': 'tree,form',
#            'res_model': 'account.move',
#            'views': [(self.env.ref('account.view_move_tree').id, 'tree'), (False, 'form')],
#            'type': 'ir.actions.act_window',
#            'domain': [('from_custom_asset', '=', True), ('asset_ref_id', '=', self.id)],
#            'context': dict(self._context, create=False),
#        }

#    def create_custom_asset_entry(self):
#        for asset in self:
#            asset.compute_custom_depreciation_board()
#            asset.write({'hide_custom_button': True})

    def compute_custom_depreciation_board(self):
        self.ensure_one()
        depreciation_number = 1
        starting_sequence = 0
        amount_to_depreciate = self.acc_nineteen
        configs = self.env['res.config.settings'].search([])
        for conf in configs:
            depreciation_date = conf['assets_date']
        commands = []
        newlines = self._recompute_board(depreciation_number, starting_sequence, amount_to_depreciate,
                                         depreciation_date, already_depreciated_amount=0, amount_change_ids=False)
        newline_vals_list = []
        for newline_vals in newlines:
            # no need of amount field, as it is computed and we don't want to trigger its inverse function
            del (newline_vals['amount_total'])
            newline_vals_list.append(newline_vals)
        new_moves = self.env['account.move'].create(newline_vals_list)
        for move in new_moves:
            move.write({'ref': self.name, 'asset_ref_id': self.id, 'asset_id': False, 'from_custom_asset': True})

            
    def _set_value(self):
        for record in self:
            record.acquisition_date = min(record.original_move_line_ids.mapped('date') + [
                record.prorata_date or record.first_depreciation_date or fields.Date.today()])
            record.first_depreciation_date = record._get_first_depreciation_date()
            record.value_residual = record.original_value - record.salvage_value - record.acc_nineteen
            record.name = record.name or (
                    record.original_move_line_ids and record.original_move_line_ids[0].name or '')
            if not record.asset_type and 'asset_type' in self.env.context:
                record.asset_type = self.env.context['asset_type']
            if not record.asset_type and record.original_move_line_ids:
                account = record.original_move_line_ids.account_id
                record.asset_type = account.asset_type
            record._onchange_depreciation_account()
            

                
    @api.onchange('salvage_value')
    def _onchange_salvage_value(self):
        # When we are configuring the asset we dont want the book value to change
        # when we change the salvage value because of _compute_book_value
        # we need to reduce value_residual to do that
        self.value_residual = self.original_value - self.salvage_value - self.acc_nineteen
        
    @api.onchange('acc_nineteen')
    def _onchange_acc(self):
        # When we are configuring the asset we dont want the book value to change
        # when we change the salvage value because of _compute_book_value
        # we need to reduce value_residual to do that
        self.value_residual = self.original_value - self.acc_nineteen - self.salvage_value
        
    @api.depends('value_residual', 'salvage_value', 'children_ids.book_value')                
    def _compute_book_value(self):
        for record in self:
            record.book_value = record.value_residual + record.salvage_value + sum(record.children_ids.mapped('book_value'))
            record.gross_increase_value = sum(record.children_ids.mapped('original_value'))


    @api.onchange('original_value')
    def _onchange_value(self):
        self._set_value()
        

class assets_report(models.AbstractModel):
    _inherit = 'account.assets.report'

    def _get_lines(self, options, line_id=None):
        options['self'] = self
        lines = []
        total = [0] * 9
        asset_lines = self._get_assets_lines(options)
        parent_lines = []
        children_lines = defaultdict(list)
        for al in asset_lines:
            if al['parent_id']:
                children_lines[al['parent_id']] += [al]
            else:
                parent_lines += [al]
        for al in parent_lines:
            if al['asset_method'] == 'linear' and al[
                'asset_method_number']:  # some assets might have 0 depreciations because they dont lose value
                asset_depreciation_rate = ('{:.2f} %').format(
                    (100.0 / al['asset_method_number']) * (12 / int(al['asset_method_period'])))
            elif al['asset_method'] == 'linear':
                asset_depreciation_rate = ('{:.2f} %').format(0.0)
            else:
                asset_depreciation_rate = ('{:.2f} %').format(float(al['asset_method_progress_factor']) * 100)

            asset_object = self.env['account.asset'].browse(int(al['asset_id']))
            depreciation_opening = al['depreciated_start'] - al['depreciation']
            depreciation_closing = (al['depreciated_end']) + (asset_object.acc_nineteen if asset_object else 0)
            depreciation_minus = 0.0

            asset_opening = al['asset_original_value'] if al['max_date_before'] else 0.0
    
            print("al", asset_object)
            asset_add = 0.0 if al['max_date_before'] else al['asset_original_value']
            asset_minus = 0.0

            for child in children_lines[al['asset_id']]:
                depreciation_opening += child['depreciated_start'] - child['depreciation']
                depreciation_closing += child['depreciated_end']

                asset_opening += child['asset_original_value'] if child['max_date_before'] else 0.0
                asset_add += 0.0 if child['max_date_before'] else child['asset_original_value']

            depreciation_add = depreciation_closing - depreciation_opening
            asset_closing = asset_opening + asset_add

            if al['asset_state'] == 'close' and al['asset_disposal_date'] and al[
                'asset_disposal_date'] < fields.Date.to_date(options['date']['date_to']):
                depreciation_minus = depreciation_closing
                depreciation_closing = 0.0
                asset_minus = asset_closing
                asset_closing = 0.0

            asset_gross = asset_closing - depreciation_closing

            total = [x + y for x, y in zip(total,
                                           [asset_opening, asset_add, asset_minus, asset_closing, depreciation_opening,
                                            depreciation_add, depreciation_minus, depreciation_closing, asset_gross])]

            id = "_".join([self._get_account_group(al['account_code'])[0], str(al['asset_id'])])
            name = str(al['asset_name'])
            line = {
                'id': id,
                'level': 1,
                'name': name if len(name) < MAX_NAME_LENGTH else name[:MAX_NAME_LENGTH - 2] + '...',
                'columns': [
                    {'name': al['asset_acquisition_date'] and format_date(self.env, al['asset_acquisition_date']) or '',
                     'no_format_name': ''},  # Caracteristics
                    {'name': al['asset_date'] and format_date(self.env, al['asset_date']) or '', 'no_format_name': ''},
                    {'name': (al['asset_method'] == 'linear' and _('Linear')) or (
                            al['asset_method'] == 'degressive' and _('Degressive')) or _('Accelerated'),
                     'no_format_name': ''},
                    {'name': asset_depreciation_rate, 'no_format_name': ''},
                    {'name': self.format_value(asset_opening), 'no_format_name': asset_opening},  # Assets
                    {'name': self.format_value(asset_add), 'no_format_name': asset_add},
                    {'name': self.format_value(asset_minus), 'no_format_name': asset_minus},
                    {'name': self.format_value(asset_closing), 'no_format_name': asset_closing},
                    {'name': self.format_value(depreciation_opening), 'no_format_name': depreciation_opening},
                    # Depreciation
                    {'name': self.format_value(depreciation_add), 'no_format_name': depreciation_add},
                    {'name': self.format_value(depreciation_minus), 'no_format_name': depreciation_minus},
                    {'name': self.format_value(depreciation_closing), 'no_format_name': depreciation_closing},
                    {'name': self.format_value(asset_gross), 'no_format_name': asset_gross},  # Gross
                ],
                'unfoldable': False,
                'unfolded': False,
                'caret_options': 'account.asset.line',
                'account_id': al['account_id']
            }
            if len(name) >= MAX_NAME_LENGTH:
                line.update({'title_hover': name})
            lines.append(line)
        lines.append({
            'id': 'total',
            'level': 0,
            'name': _('Total'),
            'columns': [
                {'name': ''},  # Caracteristics
                {'name': ''},
                {'name': ''},
                {'name': ''},
                {'name': self.format_value(total[0])},  # Assets
                {'name': self.format_value(total[1])},
                {'name': self.format_value(total[2])},
                {'name': self.format_value(total[3])},
                {'name': self.format_value(total[4])},  # Depreciation
                {'name': self.format_value(total[5])},
                {'name': self.format_value(total[6])},
                {'name': self.format_value(total[7])},
                {'name': self.format_value(total[8])},  # Gross
            ],
            'unfoldable': False,
            'unfolded': False,
        })
        return lines
