from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    pnt_move_plastic_tax_id = fields.Many2one('account.move', store=True, string='Plastic tax entry',
                                 help='El impuesto al plástico graba la introducción o fabricación del mismo en España.'
                                      '- - - '
                                      'Es obligatorio el pago de tasa:'
                                      '- En caso de importar plástico.'
                                      '- En caso de fabricar plastico en España.'
                                      '- La tasa de compra se paga adicionalmente al precio del proveedor extranjero, en aduana.'
                                      '- La repercusión de la tasa al cliente se hace en el PVP, no es compensable y lleva IVA.'
                                      '- - - '
                                      'Podemos solicitar la devolución de estas tasas en los siguientes casos:'
                                      '- Venta de plástico adquirido fuera de España, pagó tasas y ha sido exportado.'
                                      '- Abono de facturas de compra fuera de España con devolución de material.'
                                      '- - - '
                                      'Otros casos:'
                                      '- Si compramos plástico en España, el proveedor ya pagó la tasa, no podemos recuperarla.'
                                      '- La compra de materia prima no se considera grabable a que no se conoce su uso final.'
                                      '- - - '
                                      'CONFIGURACIÓN DE LA APLICACIÓN:'
                                      '- Los productos fabricados están definidos en la familia.'
                                      '- El diario y cuenta contable utilizada para el apunte están definidos en la configuración de empresa.'
                                      '- En caso de que la factura no requiera tasa el botón para creación automática no aparece.'
                                      '- Podemos asignar un apunte creado previamente (o nulo) manualmente o crearlo automáticamente.'
                                      '- Se recomienda diario independiente para facilitar la búsqueda y filtros oportunos.'
                                      '(más información en la web oficial AEAT)')

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

    def create_plastic_tax_entry(self):
        # Si es venta o abono de compra: el debe a la 700(producto) y haber a la 475
        # Si es compra o abono de venta: el debe a la 475 y haber a la 600 (depende del producto)
        # Añadir los kg de plástico
        if self.pnt_move_plastic_tax_id.id:
          raise UserError('Esta factura ya tiene un apunte, modifícalo o quita la asociación.')

        plastic_journal = self.env.company.pnt_plastic_journal_id
        plastic_account = self.env.company.pnt_plastic_account_id

        if not (plastic_journal.id) or not (plastic_account.id):
            raise UserError('Asigna el diario y cuenta para el impuesto al plástico en la compañía.')

        tax_entry = self.env['account.move'].create(
            {'journal_id': plastic_journal.id, 'move_type': 'entry', 'name': "Plastic tax: " + self.partner_id.name,
             'partner_id': self.partner_id.id, 'invoice_origin': self.invoice_origin})
        self.pnt_move_plastic_tax_id = tax_entry

        control = 0
        if (self.move_type == 'out_invoice') and (self.partner_id.country_id.code == 'ES'):
            self.tax_entry_out_invoice_spain()
        if (self.move_type == 'out_invoice') and (self.partner_id.country_id.code != 'ES'):
            self.tax_entry_out_invoice_no_spain()

        if (self.move_type == 'out_refund') and (self.partner_id.country_id.code == 'ES'):
            self.tax_entry_out_refund_spain()
        if (self.move_type == 'out_refund') and (self.partner_id.country_id.code != 'ES'):
            self.tax_entry_out_refund_no_spain()

        if (self.move_type == 'in_invoice') and (self.partner_id.country_id.code != 'ES'):
            self.tax_entry_in_invoice()
        if (self.move_type == 'in_refund') and (self.partner_id.country_id.code != 'ES'):
            self.tax_entry_in_refund()

    def tax_entry_out_invoice_spain(self):
        for li in self.invoice_line_ids:
            if (li.product_id.id) and (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                # En la venta pagamos impuesto por plástico FABRICADO aquí y vendido aquí:
                if (li.product_id.pnt_is_manufactured):
                    accountpurchase = li.product_id.property_account_expense_id
                    if not accountpurchase.id: accountpurchase = li.product_id.categ_id.property_account_expense_categ_id
                    accountsale = li.product_id.property_account_income_id
                    if not accountsale.id: accountsale = li.product_id.categ_id.property_account_income_categ_id

                    tax_entry = self.pnt_move_plastic_tax_id
                    tax_entry['line_ids'] = [(0, 0, {
                        'product_id': li.product_id.id,
                        'display_type': li.display_type,
                        'name': li.product_id.name,
                        'price_unit': abs(li.pnt_plastic_tax / li.quantity),
                        'debit': abs(li.pnt_plastic_tax),
                        'account_id': accountsale.id,
                        'analytic_distribution': li.analytic_distribution,
                        'partner_id': self.partner_id.id,
                        'quantity': li.quantity,
                    }), (0, 0, {
                        'name': self.name or '/',
                        'credit': abs(li.pnt_plastic_tax),
                        'account_id': self.env.company.pnt_plastic_account_id.id,
                        'partner_id': self.partner_id.id,
                    })]

    def tax_entry_out_invoice_no_spain(self):
        # En la venta reclamamos abono de impuesto pagado si vendemos fabricados IMPORTADOS (que pagamos en aduana anteriormente la tasa):
        for li in self.invoice_line_ids:
            if (li.product_id.id) and (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                if not (li.product_id.pnt_is_manufactured):
                    accountpurchase = li.product_id.property_account_expense_id
                    if not accountpurchase.id: accountpurchase = li.product_id.categ_id.property_account_expense_categ_id
                    accountsale = li.product_id.property_account_income_id
                    if not accountsale.id: accountsale = li.product_id.categ_id.property_account_income_categ_id

                    tax_entry = self.pnt_move_plastic_tax_id
                    tax_entry['line_ids'] = [(0, 0, {
                        'product_id': li.product_id.id,
                        'display_type': li.display_type,
                        'name': li.product_id.name,
                        'price_unit': abs(li.pnt_plastic_tax / li.quantity),
                        'credit': abs(li.pnt_plastic_tax),
                        'account_id': accountsale.id,
                        'analytic_distribution': li.analytic_distribution,
                        'partner_id': self.partner_id.id,
                        'quantity': li.quantity,
                    }), (0, 0, {
                        'name': self.name or '/',
                        'debit': abs(li.pnt_plastic_tax),
                        'account_id': self.env.company.pnt_plastic_account_id.id,
                        'partner_id': self.partner_id.id,
                    })]



    def tax_entry_out_refund_spain(self):
        for li in self.invoice_line_ids:
            if (li.product_id.id) and (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                # Para venta pagamos impuesto por plástico FABRICADO aquí y vendido aquí, pero no si vuelve a STOCK:
                if (li.product_id.pnt_is_manufactured):
                    accountpurchase = li.product_id.property_account_expense_id
                    if not accountpurchase.id: accountpurchase = li.product_id.categ_id.property_account_expense_categ_id
                    accountsale = li.product_id.property_account_income_id
                    if not accountsale.id: accountsale = li.product_id.categ_id.property_account_income_categ_id

                    tax_entry = self.pnt_move_plastic_tax_id
                    tax_entry['line_ids'] = [(0, 0, {
                        'product_id': li.product_id.id,
                        'display_type': li.display_type,
                        'name': li.product_id.name,
                        'price_unit': abs(li.pnt_plastic_tax / li.quantity),
                        'debit': abs(li.pnt_plastic_tax),
                        'account_id': self.env.company.pnt_plastic_account_id.id,
                        'analytic_distribution': li.analytic_distribution,
                        'partner_id': self.partner_id.id,
                        'quantity': li.quantity,
                    }), (0, 0, {
                        'name': self.name or '/',
                        'credit': abs(li.pnt_plastic_tax),
                        'account_id': accountsale.id,
                        'partner_id': self.partner_id.id,
                    })]

    def tax_entry_out_refund_no_spain(self):
        # En venta si nos han devuelto el impuesto (porque pagamos "no fabricado"
        # hemos de volver a pagarlo ya que introducimos plático en España:
        for li in self.invoice_line_ids:
            if (li.product_id.id) and (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                if not (li.product_id.pnt_is_manufactured):
                    accountpurchase = li.product_id.property_account_expense_id
                    if not accountpurchase.id: accountpurchase = li.product_id.categ_id.property_account_expense_categ_id
                    accountsale = li.product_id.property_account_income_id
                    if not accountsale.id: accountsale = li.product_id.categ_id.property_account_income_categ_id

                    tax_entry = self.pnt_move_plastic_tax_id
                    tax_entry['line_ids'] = [(0, 0, {
                        'product_id': li.product_id.id,
                        'display_type': li.display_type,
                        'name': li.product_id.name,
                        'price_unit': abs(li.pnt_plastic_tax / li.quantity),
                        'credit': abs(li.pnt_plastic_tax),
                        'account_id': self.env.company.pnt_plastic_account_id.id,
                        'analytic_distribution': li.analytic_distribution,
                        'partner_id': self.partner_id.id,
                        'quantity': li.quantity,
                    }), (0, 0, {
                        'name': self.name or '/',
                        'debit': abs(li.pnt_plastic_tax),
                        'account_id': accountsale.id,
                        'partner_id': self.partner_id.id,
                    })]

    def tax_entry_in_invoice(self):
                # Pagamos impuesto en aduana por Compra de plástico en el extranjero (la materia prima no paga, para
                # esto en los productos de materia prima "pnt_plastic_weight" == 0):
                for li in self.invoice_line_ids:
                    if (li.product_id.id) and (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                        if not (li.product_id.pnt_is_manufactured):
                            accountpurchase = li.product_id.property_account_expense_id
                            if not accountpurchase.id: accountpurchase = li.product_id.categ_id.property_account_expense_categ_id
                            accountsale = li.product_id.property_account_income_id
                            if not accountsale.id: accountsale = li.product_id.categ_id.property_account_income_categ_id

                            tax_entry = self.pnt_move_plastic_tax_id
                            tax_entry['line_ids'] = [(0, 0, {
                                'product_id': li.product_id.id,
                                'display_type': li.display_type,
                                'name': li.product_id.name,
                                'price_unit': abs(li.pnt_plastic_tax / li.quantity),
                                'debit': abs(li.pnt_plastic_tax),
                                'account_id': accountpurchase.id,
                                'analytic_distribution': li.analytic_distribution,
                                'partner_id': self.partner_id.id,
                                'quantity': li.quantity,
                            }), (0, 0, {
                                'name': self.name or '/',
                                'credit': abs(li.pnt_plastic_tax),
                                'account_id': self.env.company.pnt_plastic_account_id.id,
                                'partner_id': self.partner_id.id,
                            })]

    def tax_entry_in_refund(self):
                # Abono del anterior:
                # Solicitud de devolución de impuesto en aduana por Compra de plástico en el extranjero,
                # en el caso de devolución:
                for li in self.invoice_line_ids:
                    if (li.product_id.id) and (li.product_id.pnt_plastic_weight != 0) and (li.quantity != 0):
                        if not (li.product_id.pnt_is_manufactured):
                            accountpurchase = li.product_id.property_account_expense_id
                            if not accountpurchase.id: accountpurchase = li.product_id.categ_id.property_account_expense_categ_id
                            accountsale = li.product_id.property_account_income_id
                            if not accountsale.id: accountsale = li.product_id.categ_id.property_account_income_categ_id

                            tax_entry = self.pnt_move_plastic_tax_id
                            tax_entry['line_ids'] = [(0, 0, {
                                'product_id': li.product_id.id,
                                'display_type': li.display_type,
                                'name': li.product_id.name,
                                'price_unit': abs(li.pnt_plastic_tax / li.quantity),
                                'debit': abs(li.pnt_plastic_tax),
                                'account_id': self.env.company.pnt_plastic_account_id.id,
                                'analytic_distribution': li.analytic_distribution,
                                'partner_id': self.partner_id.id,
                                'quantity': li.quantity,
                            }), (0, 0, {
                                'name': self.name or '/',
                                'credit': abs(li.pnt_plastic_tax),
                                'account_id': accountpurchase.id,
                                'partner_id': self.partner_id.id,
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
