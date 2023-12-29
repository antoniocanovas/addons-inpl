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
        # Si vendemos o compramos en España, el impuesto va en PVP o ya lo pagó el proveedor:
        if (self.partner_id.country_id.code != 'ES') and (self.state not in ['cancel']) and (self.move_type in ['in_invoice','in_refund','out_invoice','out_refund']) and not (self.pnt_move_plastic_tax_id.id):
            for li in self.invoice_line_ids:
                if (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                    show_button = True
        self.plastic_tax = show_button
    plastic_tax = fields.Boolean('Plastic tax', store=False, compute='_get_show_button_plastic_tax')

    def create_plastic_tax_entry(self):
        # Si es venta o abono de compra: el debe a la 700(producto) y haber a la 475
        # Si es compra o abono de venta: el debe a la 475 y haber a la 600 (depende del producto)
        # Añadir los kg de plástico
        if self.pnt_move_plastic_tax_id.id:
          raise UserError('Esta factura ya tiene un apunte, modifícalo o quita la asociación.')

        plastic_journal_id = self.env.company.pnt_plastic_journal_id
        account430 = env['account.account'].search([('code', '=', '430000')])
        accountsup = self.partner_id.property_account_payable_id
        if not plastic_journal_id:
            raise UserError('Asigna el diario para el impuesto al plástico en la compañía.')

        tax_entry = env['account.move'].create(
            {'journal_id': plastic_journal_id.id, 'move_type': 'entry', 'name': "Impuesto al plástico " + record.name,
             'partner_id': record.partner_id.id, 'invoice_origin': record.invoice_origin})
        record['pnt_move_plastic_tax_id'] = tax_entry

        for li in record.invoice_line_ids:
            if li.product_id.id:
                # Voy por aquí:


                #        account = li.product_id.property_account_expense_id
                #        if not account.id: account = li.product_id.categ_id.property_account_expense_categ_id
                apunte['line_ids'] = [(0, 0, {
                    'product_id': li.product_id.id,
                    'display_type': li.display_type,
                    'name': li.product_id.name,
                    'price_unit': abs(li.price_subtotal),
                    'debit': li.price_subtotal,
                    'account_id': account430.id,
                    'analytic_distribution': li.analytic_distribution,
                    'partner_id': record.partner_id.id
                }), (0, 0, {
                    'name': record.name or '/',
                    'credit': li.price_subtotal,
                    'account_id': 233,
                    'partner_id': record.partner_id.id,
                })]

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
