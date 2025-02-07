# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class AnalyticDistribution(models.Model):
    _inherit = 'analytic.distribution'

    picking_in_handles_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_handles_rel',  # nombre único para la tabla rel
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de Asas",
        compute="_compute_picking_in_handles_ids",

    )
    picking_in_pallet_handles_qty = fields.Float(
        string="Cantidad de Asas",
        compute="_compute_picking_in_handles",
        store=True
    )

    picking_in_handles_qty = fields.Float(
        string="Cantidad de Asas",
        compute="_compute_picking_in_handles_qty",
        store=True
    )
    picking_in_caps_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_caps_rel',  # nombre único para la tabla rel
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de tapones",
        compute="_compute_picking_in_caps_ids",

    )
    picking_in_pallet_caps_qty = fields.Float(
        string="pallets de Tapones",
        compute="_compute_picking_in_caps_qty",
        store=True
    )

    picking_in_caps_qty = fields.Float(
        string="albaranes de Tapones",
        compute="_compute_picking_in_caps",
        store=True
    )



    sale_pallet_cap_ids = fields.Many2many(
        'sale.order.line',
        string="Líneas de Palets de Tapones",
        compute="_compute_sale_pallet_cap_ids",
    )
    sale_pallet_cap_qty = fields.Float(
        string="Cantidad de Palets de Tapones",
        compute="_compute_sale_pallet_cap_qty",
    )
    sale_pallet_handles_ids = fields.Many2many(
        'sale.order.line',
        string="Líneas de Palets de Tapones",
        compute="_compute_sale_pallet_cap_ids",
    )
    sale_pallet_handles_qty = fields.Float(
        string="Cantidad de Palets de Tapones",
        compute="_compute_sale_pallet_cap_qty",
    )



    @api.depends('date_from', 'date_to')
    def _compute_sale_pallet_handles_qty(self):
        self.sale_pallet_handles_qty = len(self.sale_pallet_handles_ids)

    @api.depends('date_from', 'date_to')
    def _compute_sale_pallet_cap_qty(self):
        self.sale_pallet_cap_qty = len(self.sale_pallet_cap_ids)

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_handles_qty(self):
        self.picking_in_handles_qty=len(self.picking_in_handles_ids)

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_caps_qty(self):
        self.picking_in_caps_qty = len(self.picking_in_caps_ids)

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_caps_ids(self):
        """Calcula los pickings del periodo en que al menos una línea tenga
        product_id.categ_id.type == '['cap_mrp', 'cap_distribution']' y suma la cantidad de esas líneas."""
        for rec in self:
            # Ajusta el dominio según tus campos de fecha y la relación con los pickings
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['cap_mrp', 'cap_distribution']),
            ])
            rec.picking_in_caps_ids = pickings


    @api.depends('date_from', 'date_to')
    def _compute_picking_in_caps(self):
        """Calcula los pickings del periodo en que al menos una línea tenga
        product_id.categ_id.type == '['cap_mrp', 'cap_distribution']' y suma la cantidad de esas líneas."""
        for rec in self:
            # Ajusta el dominio según tus campos de fecha y la relación con los pickings
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type',  'in', ['cap_mrp', 'cap_distribution']),
            ])

            total_qty = 0.0
            for picking in pickings:
                # Filtramos las líneas con productos del tipo 'handle'
                lines = picking.move_ids_without_package.filtered(
                    lambda l: l.product_id.categ_id.type in ['cap_mrp', 'cap_distribution']
                )
                total_qty += sum(lines.mapped('product_uom_qty'))
            rec.picking_in_pallet_caps_qty = total_qty

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_handles_ids(self):
        """Calcula los pickings del periodo en que al menos una línea tenga
        product_id.categ_id.type == 'handle' y suma la cantidad de esas líneas."""
        for rec in self:
            # Ajusta el dominio según tus campos de fecha y la relación con los pickings
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', '=', 'handle'),
            ])
            rec.picking_in_handles_ids = pickings

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_handles(self):
        """Calcula los pickings del periodo en que al menos una línea tenga
        product_id.categ_id.type == 'handle' y suma la cantidad de esas líneas."""
        for rec in self:
            # Ajusta el dominio según tus campos de fecha y la relación con los pickings
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', '=', 'handle'),
            ])

            total_qty = 0.0
            for picking in pickings:
                # Filtramos las líneas con productos del tipo 'handle'
                lines = picking.move_ids_without_package.filtered(
                    lambda l: l.product_id.categ_id.type == 'handle'
                )
                total_qty += sum(lines.mapped('product_uom_qty'))
            rec.picking_in_pallet_handles_qty = total_qty

    @api.depends('date_from', 'date_to')
    def _compute_sale_pallet_cap_ids(self):
        """Calcula las líneas de venta del periodo que tengan productos de
        familia de tapones (por ejemplo, 'cap_mrp' y 'cap_distribution') y suma
        la cantidad vendida."""
        for rec in self:
            sale_lines = self.env['sale.order.line'].search([
                ('order_id.date_order', '>=', rec.date_from),
                ('order_id.date_order', '<=', rec.date_to),
                ('product_id.categ_id.type', 'in', ['cap_mrp', 'cap_distribution']),
            ])
            rec.sale_pallet_cap_ids = sale_lines

    @api.depends('date_from', 'date_to')
    def _compute_sale_pallet_cap(self):
        """Calcula las líneas de venta del periodo que tengan productos de
        familia de tapones (por ejemplo, 'cap_mrp' y 'cap_distribution') y suma
        la cantidad vendida."""
        for rec in self:
            sale_lines = self.env['sale.order.line'].search([
                ('order_id.date_order', '>=', rec.date_from),
                ('order_id.date_order', '<=', rec.date_to),
                ('product_id.categ_id.type', 'in', ['cap_mrp', 'cap_distribution']),
            ])
            rec.sale_pallet_cap_qty = (sum(sale_lines.mapped('product_uom_qty')))

    @api.depends('date_from', 'date_to')
    def _compute_sale_pallet_handles_ids(self):
        """Calcula las líneas de venta del periodo que tengan productos de
        familia de tapones (por ejemplo, 'cap_mrp' y 'cap_distribution') y suma
        la cantidad vendida."""
        for rec in self:
            sale_lines = self.env['sale.order.line'].search([
                ('order_id.date_order', '>=', rec.date_from),
                ('order_id.date_order', '<=', rec.date_to),
                ('product_id.categ_id.type', '=', 'handle'),
            ])
            rec.sale_pallet_cap_ids = sale_lines

    @api.depends('date_from', 'date_to')
    def _compute_sale_pallet_handles(self):
        """Calcula las líneas de venta del periodo que tengan productos de
        familia de tapones (por ejemplo, 'cap_mrp' y 'cap_distribution') y suma
        la cantidad vendida."""
        for rec in self:
            sale_lines = self.env['sale.order.line'].search([
                ('order_id.date_order', '>=', rec.date_from),
                ('order_id.date_order', '<=', rec.date_to),
                ('product_id.categ_id.type', '=', 'handle'),
            ])

            rec.sale_pallet_cap_qty = sum(sale_lines.mapped('product_uom_qty'))
