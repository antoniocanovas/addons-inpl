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
    income_debit = fields.Monetary('Income debit')
    income_credit = fields.Monetary('Income credit')
    expense_debit = fields.Monetary('Expense debit')
    expense_credit = fields.Monetary('Expense credit')
    currency_id = fields.Many2one('res.currency', default=lambda self:self.env.company.currency_id)
