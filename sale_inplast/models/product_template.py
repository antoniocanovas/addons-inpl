from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pnt_pricelist_weight = fields.Float('Pricelist weight', store=True, copy=True)

    # Primer incremento porcentual sobre el precio ya modificado por variación de precio en MP + defectuoso:
    pnt_i1 = fields.Float('Inc. 1 (%)', store=True, copy=False)
    # Segundo incremento en tanto por mil, sobre el precio ya modificado por variación de precio en MP + defectuoso:
    pnt_i2 = fields.Float('Inc. 2 (tanto/1000)', store=True, copy=False)
    # Tercer incremento en valor absoluto sobre los incrementos anteriores:
    pnt_i3 = fields.Float('Inc. 3 (€)', store=True, copy=False)
