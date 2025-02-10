# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Cuentas Analíticas',
        compute='_compute_analytic_account_ids',
        store=True
    )

    @api.depends('analytic_distribution')
    def _compute_analytic_account_ids(self):
        for line in self:
            analytic_ids = []
            if line.analytic_distribution:
                # Como analytic_distribution es un campo JSON,
                # se espera que line.analytic_distribution sea un diccionario
                # cuyas claves son cadenas con IDs separados por comas.
                for key in line.analytic_distribution.keys():
                    # Separamos la cadena por comas y convertimos cada parte en entero
                    ids = [int(x.strip()) for x in key.split(',') if x.strip().isdigit()]
                    analytic_ids.extend(ids)
            # Eliminamos duplicados y asignamos el Many2many
            line.analytic_account_ids = [(6, 0, list(set(analytic_ids)))]


# PARA BORRAR, SE USARÁ CON CUENTAS ANALÍTICAS DE PLANES ESPECÍFICOS:
# Las ventas se asignan por defecto a Producción, asignación del valor parametrizado desde res.company:
@api.depends('move_type')
def _get_analytic_distribution_account(self):
    for record in self:
        analytic_account = False
        default_analytic_account = self.env.company.default_sale_analytic_distribution_account_id
        if record.move_id.move_type in ['out_invoice','out_refund']:
            analytic_account = default_analytic_account.id
        record['analytic_distribution_account_id'] = analytic_account
analytic_distribution_account_id = fields.Many2one('account.analytic.account', string='Department',
                                                   readonly=False, store=True,
                                                   compute='_get_analytic_distribution_account',
                                                   help='Analytic distribution account',
                                                   )
@api.depends('name')
def _get_analytic_distribution_plan(self):
    self.analytic_distribution_plan_id = self.env.company.analytic_distribution_plan_id.id
analytic_distribution_plan_id = fields.Many2one('account.analytic.plan', string='Distribution plan',
                                                compute='_get_analytic_distribution_plan')
