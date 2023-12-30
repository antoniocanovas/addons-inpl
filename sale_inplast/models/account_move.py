from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    pnt_move_plastic_tax_id = fields.Many2one('account.move', store=True, string='Plastic tax entry')

    @api.depends('state', 'pnt_move_plastic_tax_id', 'write_date')
    def _get_show_button_plastic_tax(self):
        show_button = False
        if (self.state not in ['cancel']) and (self.move_type in ['in_invoice','in_refund','out_invoice','out_refund']) and not (self.pnt_move_plastic_tax_id.id):
            for li in self.invoice_line_ids:
                # Con esta condición verificamos que es plástico:
                if (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                    # Operaciones de compra fuera de España:
                    if (self.partner_id.country_id.code != 'ES') and (self.move_type in ['in_invoice','in_refund']):
                        show_button = True
                    # Operaciones de venta fuera de España, sólo recuperamos si es comercio (no fabricados):
                    if (self.partner_id.country_id.code != 'ES') and (self.move_type in ['out_invoice','out_refund']) and (li.product_id.pnt_is_manufactured == False):
                        show_button = True
                    # Si vendemos o compramos plástico en España, el impuesto va en PVP o ya lo pagó el proveedor.
                    # Si vendemos en España plástico PRODUCIDO aquí, hemos de pagar (si venta en el extranjero, no):
                    if (self.partner_id.country_id.code == 'ES') and (self.move_type in ['out_invoice','out_refund']) and (li.product_id.pnt_is_manufactured):
                        show_button = True
        self.plastic_tax = show_button
    plastic_tax = fields.Boolean('Plastic tax', store=False, compute='_get_show_button_plastic_tax')



    # Caso 1.- Compramos plástico fuera de España => Impuesto (contemplado)
    # Caso 2.- Compramos plástico dentro de España => Ese plástico ya pagó impuesto (contemplado)
    # Caso 3.- Vendemos en España algo comprado fuera y pagó impuesto => Cobrar al cliente en pvp (contemplado)
    # Caso 4.- Vendemos fuera algo comprado fuera de España => Reclamar impuesto ya pagado (contemplado)
    # Caso 5.- Vendemos fuera algo fabricando por nosotros => No paga impuestos (contemplado en tarifa + constrains)
    @api.constrains('state')
    def _check_plastic_tax_required(self):
        for record in self:
            if (record.move_type in ['in_invoice', 'in_refund']) and (record.state in ['posted']):
                if (not record.partner_id.country_id.id):
                    raise UserError('Pon el país al proveedor para poder controlar el impuesto al plástico.')
                elif (record.partner_id.country_id.code != 'ES') and not (record.pnt_move_plastic_tax_id.id):
                    plastic_tax_required = False
                    for li in record.invoice_line_ids:
                        if li.product_id.pnt_plastic_weight != 0:
                            message = "El producto " + li.product_id.name + " requiere impuesto al plástico, crea o asigna el apunte correspondiente en esta factura"
                            raise UserError(message)

            if (record.move_type in ['out_invoice', 'out_refund']) and (record.state in ['posted']):
                if (not record.partner_id.country_id.id):
                    raise UserError('Pon el país al cliente para poder controlar el impuesto al plástico.')
                elif (record.partner_id.country_id.code != 'ES') and not (record.pnt_move_plastic_tax_id.id):
                    for li in record.invoice_line_ids:
                        if (li.product_id.pnt_plastic_weight != 0) and (li.product_id.categ_id.pnt_is_manufactured == False):
                            message = "El producto " + li.product_id.name + " es susceptible de recuperar el impuesto al plástico, crea o asigna el apunte correspondiente en esta factura"
                            raise UserError(message)
