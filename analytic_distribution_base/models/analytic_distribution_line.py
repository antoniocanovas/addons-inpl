# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError

class AnalyticDistributionLine(models.Model):
    _name = 'analytic.distribution.line'
    _description = 'Analytic distribution line'


    template_id = fields.Many2one('analytic.distribution.template', string='Template', required=True)
    name = fields.Char(related='template_id.name')
    distribution_id = fields.Many2one('analytic.distribution', string='Distribution')
    date_from = fields.Date(related='distribution_id.date_from')
    date_to = fields.Date(related='distribution_id.date_to')
    income = fields.Monetary('Income', compute='_get_income')
    expense = fields.Monetary('Expense', compute='_get_expense')

    @api.depends('date_from','date_to','template_id')
    def _get_income(self):
        for rec in self:
            rec.income = 1

    @api.depends('date_from','date_to','template_id')
    def _get_expense(self):
        for rec in self:
            rec.expense = 2