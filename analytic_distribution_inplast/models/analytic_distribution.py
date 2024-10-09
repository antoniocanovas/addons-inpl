# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError

class AnalyticDistribution(models.Model):
    _inherit = 'analytic.distribution'

    compute_mode = fields.Selection([
        ('demo','demo INPLAST'),
        ('r13', 'R13.- Electricidad'),
    ])

    workcenter_ids = fields.Many2many('mrp.workcenter', string="Workcenters")


    def compute_distribution(self):
        """ Extend this function with custom Inplast analytic compute modes
        """
        super().compute_distribution()
        self.inplast_computed_modes()

    def inplast_computed_modes(self):
        if self.compute_mode == 'demo':
            raise UserError('ok')
        elif self.compute_mode == 'r13':
            self.compute_r13()

    def compute_r13(self):
        datefrom = self.date_from
        dateto = self.date_to
        total_kw, mrpproducts = 0, []
        # Array de máquinas a considerar:
        workcenters = self.workcenter_ids
        # Manufacturing order consideradas entre fechas:
        workorders = self.env['mpr.workorder'].search(
            [('workcenter_id','in',workcenter.ids),
             ('date_start', '>=', datefrom),
             ('date_start', '<=', dateto)])

        # Cálculo del total de kw en todos los workcenter en base al tiempo trabajado:
        for wo in workorders:
            total_kw += wo.duration * wo.workcenter_id.power_kw
            if wo.product_id not in mainproducts:
                mainproducts.append(wo.product_id)

        # Bucle para recorrer las operaciones de cada producto entre fechas:
        # (consumo teórico por máquina, consumo teórico total, tapones por máquina, tapones total):
        for product in mrpproducts:
            power = 0
            productworkorders = self.env['mrp.workorder'].search(
                [('workcenter_id','in',workcenter.ids),
                 ('date_start', '>=', datefrom),
                 ('date_start', '<=', dateto),
                 ('product_id','=',product.id)])
            for pwo in productworkorders:
                # Consumo:
                power += 1
                # Nº tapones:

                # Búsqueda de cuenta analítica, creación si no existe:

                # Creación de la imputación:

