from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    pnt_raw_material = fields.Many2one('product.template', store=True, copy=True, string='Raw material', tracking=True,
                                       domain="[('detailed_type','=','product')]",
                                       help='Main component to manufacture these category products.')
    pnt_plastic_weight = fields.Float('Plastic weight', store=True, copy=True, digits='Stock Weight', tracking=True,
                                      help='Unit weight used to pricelist recalculation and plastic taxes.')
    pnt_mrp_fault_percent = fields.Float('Fault (%)', store=True, copy=True, tracking=True,
                                         help='Production percent deficiency')

    # Incremento tanto por mil debido a variaciones del coste de materia prima y energía:
    pnt_i0 = fields.Float('Inc. Raw (tanto/1000)', store=True, copy=False)
    # Primer incremento comercial porcentual sobre el precio ya modificado por variación de precio en MP + defectuoso:
    pnt_i1 = fields.Float('Inc. 1 (%)', store=True, copy=False)
    # Segundo incremento en tanto por mil, sobre el precio ya modificado por variación de precio en MP + defectuoso:
    pnt_i2 = fields.Float('Inc. 2 (tanto/1000)', store=True, copy=False)
    # Tercer incremento en valor absoluto sobre los incrementos anteriores:
    pnt_i3 = fields.Float('Inc. 3 (€)', store=True, copy=False)

    pnt_is_manufactured = fields.Boolean('Manufactured', store=True, copy=True, default=True,
                                         help='Enabled if products are manufactured, disabled when bought.')

    @api.constrains('pnt_plastic_weight')
    def _avoid_change_weight_if_exists_plastic_tax_moves(self):
        account_moves = self.env['account.move.line'].search([('product_id.categ_id','=', self.id),])
        if account_moves.ids:
            raise UserError('You can not change the weight used for previous taxes accounting and sales pricelists,'
                            'create another category and products.')