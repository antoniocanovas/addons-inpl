# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    analytic_product_plan = fields.Many2one('account.analytic.plan', string='Product analytic plan')
    analytic_categ_plan = fields.Many2one('account.analytic.plan', string='Category analytic plan')
    analytic_department_plan = fields.Many2one('account.analytic.plan', string='Department analytic plan')
