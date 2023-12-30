from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    pnt_move_plastic_tax_id = fields.Many2one('account.move', store=True, string='Plastic tax entry')


    plastic_tax = fields.Boolean('Plastic tax', store=False)



    # Caso 1.- Compramos plástico fuera de España => Impuesto (contemplado)
    # Caso 2.- Compramos plástico dentro de España => Ese plástico ya pagó impuesto (contemplado)
    # Caso 3.- Vendemos en España algo comprado fuera y pagó impuesto => Cobrar al cliente en pvp (contemplado)
    # Caso 4.- Vendemos fuera algo comprado fuera de España => Reclamar impuesto ya pagado (contemplado)
    # Caso 5.- Vendemos fuera algo fabricando por nosotros => No paga impuestos (contemplado en tarifa + constrains)
