# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class WizardTrialBalance(models.TransientModel):
    _name = 'wizard.general.balance.ecosoft'

    choose_period = fields.Boolean('A un Periodo')
    period_id = fields.Many2one('account.period', 'Periodo', required=False)
    level = fields.Selection([(1, '1.- Mayor'),(2, '2.- Sub-cta'),(3, '3.- Auxiliar')], string='Nivel',
      required=True, copy=False, default=1,)
    display_account = fields.Selection([('all','All'), ('movement','With movements'), 
                                        ('not_zero','With balance is not equal to 0'),], 
                                        string='Display Accounts', required=True, default='movement')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='all')
    
    def print_report(self, data):
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','period_id','level','display_account','target_move'])[0])
        #records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].get_action(False, 'account.report_generalbalance_ecosoft', data=data)
