# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from docutils.nodes import container
from odoo import fields, models, api


class AnalyticDistribution(models.Model):
    _inherit = 'analytic.distribution'


    # =========================================================================
    # 1) PICKINGS: HANDLES (Asas)
    # =========================================================================
    picking_in_handles_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_handles_rel',  # tabla rel única
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de Asas",
        compute="_compute_picking_in_handles_ids",
    )
    picking_in_handles_qty = fields.Float(
        string="Cantidad de Albaranes de Asas",
        compute="_compute_picking_in_handles_qty",
        store=True,
    )
    picking_in_pallet_handles_qty = fields.Float(
        string="Cantidad de Asas (suma de UoM)",
        compute="_compute_picking_in_handles",
        store=True,
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_handles_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', '=', 'handle'),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_handles_ids = pickings

    @api.depends('picking_in_handles_ids')
    def _compute_picking_in_handles_qty(self):
        for rec in self:
            rec.picking_in_handles_qty = len(rec.picking_in_handles_ids)

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_handles(self):
        """Suma el campo 'product_uom_qty' de las líneas de movimientos con productos 'handle'."""
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', '=', 'handle'),
                ('picking_type_code', '=', 'incoming'),
            ])
            total_qty = 0.0
            for picking in pickings:
                lines = picking.move_ids_without_package.filtered(
                    lambda l: l.product_id.categ_id.type == 'handle'
                )
                total_qty += sum(lines.mapped('product_uom_qty'))
            rec.picking_in_pallet_handles_qty = total_qty

    # =========================================================================
    # 2) PICKINGS: CAPS (Tapones)
    # =========================================================================
    picking_in_caps_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_caps_rel',  # tabla rel única
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de Tapones",
        compute="_compute_picking_in_caps_ids",
    )
    picking_in_caps_qty = fields.Float(
        string="Cantidad de Albaranes de Tapones",
        compute="_compute_picking_in_caps_qty",
        store=True,
    )
    picking_in_pallet_caps_qty = fields.Float(
        string="Cantidad de Tapones (suma de UoM)",
        compute="_compute_picking_in_caps",
        store=True,
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_caps_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['cap_mrp', 'cap_distribution']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_caps_ids = pickings

    @api.depends('picking_in_caps_ids')
    def _compute_picking_in_caps_qty(self):
        for rec in self:
            rec.picking_in_caps_qty = len(rec.picking_in_caps_ids)

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_caps(self):
        """Suma el campo 'product_uom_qty' de las líneas de movimientos con productos de tapones."""
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['cap_mrp', 'cap_distribution']),
                ('picking_type_code', '=', 'incoming'),
            ])
            total_qty = 0.0
            for picking in pickings:
                lines = picking.move_ids_without_package.filtered(
                    lambda l: l.product_id.categ_id.type in ['cap_mrp', 'cap_distribution']
                )
                total_qty += sum(lines.mapped('product_uom_qty'))
            rec.picking_in_pallet_caps_qty = total_qty

    # =========================================================================
    # 3) SALE ORDERS: CAPS (Tapones)
    # =========================================================================
    sale_caps_order_ids = fields.Many2many(
        'sale.order',
        relation='analytic_distribution_sale_caps_order_rel',  # relación rel única
        column1='analytic_distribution_id',
        column2='sale_order_id',
        string="Sale Orders de Tapones",
        compute="_compute_sale_caps_order_ids",
    )
    sale_caps_order_count = fields.Integer(
        string="Número de Sale Orders de Tapones",
        compute="_compute_sale_caps_order_count",
    )
    sale_caps_order_qty = fields.Float(
        string="Cantidad de Tapones (Sale Orders)",
        compute="_compute_sale_caps_order_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_sale_caps_order_ids(self):
        """Obtiene los sale orders del período y filtra aquellos que contengan líneas
        con productos de categoría 'cap_mrp' o 'cap_distribution'."""
        for rec in self:
            sale_orders = self.env['sale.order'].search([
                ('date_order', '>=', rec.date_from),
                ('date_order', '<=', rec.date_to),
            ])
            caps_orders = sale_orders.filtered(
                lambda o: any(line.product_id.categ_id.type in ['cap_mrp', 'cap_distribution'] for line in o.order_line)
            )
            rec.sale_caps_order_ids = caps_orders

    @api.depends('sale_caps_order_ids')
    def _compute_sale_caps_order_count(self):
        for rec in self:
            rec.sale_caps_order_count = len(rec.sale_caps_order_ids)

    @api.depends('sale_caps_order_ids')
    def _compute_sale_caps_order_qty(self):
        """Suma el 'product_uom_qty' de las líneas de sale order que tengan
        productos de categoría 'cap_mrp' o 'cap_distribution'."""
        for rec in self:
            total_qty = 0.0
            for so in rec.sale_caps_order_ids:
                lines = so.order_line.filtered(
                    lambda l: l.product_id.categ_id.type in ['cap_mrp', 'cap_distribution']
                )
                total_qty += sum(lines.mapped('product_uom_qty'))
            rec.sale_caps_order_qty = total_qty

    # =========================================================================
    # 4) SALE ORDERS: HANDLES (Asas)
    # =========================================================================
    sale_handles_order_ids = fields.Many2many(
        'sale.order',
        relation='analytic_distribution_sale_handles_order_rel',  # relación rel única
        column1='analytic_distribution_id',
        column2='sale_order_id',
        string="Sale Orders de Asas",
        compute="_compute_sale_handles_order_ids",
    )
    sale_handles_order_count = fields.Integer(
        string="Número de Sale Orders de Asas",
        compute="_compute_sale_handles_order_count",
    )
    sale_handles_order_qty = fields.Float(
        string="Cantidad de Asas (Sale Orders)",
        compute="_compute_sale_handles_order_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_sale_handles_order_ids(self):
        """Obtiene los sale orders del período y filtra aquellos que contengan líneas
        con productos de categoría 'handle'."""
        for rec in self:
            sale_orders = self.env['sale.order'].search([
                ('date_order', '>=', rec.date_from),
                ('date_order', '<=', rec.date_to),
            ])
            handles_orders = sale_orders.filtered(
                lambda o: any(line.product_id.categ_id.type == 'handle' for line in o.order_line)
            )
            rec.sale_handles_order_ids = handles_orders

    @api.depends('sale_handles_order_ids')
    def _compute_sale_handles_order_count(self):
        for rec in self:
            rec.sale_handles_order_count = len(rec.sale_handles_order_ids)

    @api.depends('sale_handles_order_ids')
    def _compute_sale_handles_order_qty(self):
        """Suma el 'product_uom_qty' de las líneas de sale order que tengan
        productos de categoría 'handle'."""
        for rec in self:
            total_qty = 0.0
            for so in rec.sale_handles_order_ids:
                lines = so.order_line.filtered(
                    lambda l: l.product_id.categ_id.type == 'handle'
                )
                total_qty += sum(lines.mapped('product_uom_qty'))
            rec.sale_handles_order_qty = total_qty

    # =========================================================================
    # 5) PICKINGS: CISTERNAS
    # =========================================================================
    picking_in_cistern_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_cistern_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de cisternas",
        compute="_compute_picking_in_cistern_ids",
    )
    picking_in_cistern_qty = fields.Float(
        string="Cantidad de cisternas",
        compute="_compute_picking_in_cistern_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_cistern_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['raw_cistern']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_cistern_ids = pickings

    @api.depends('picking_in_cistern_ids')
    def _compute_picking_in_cistern_qty(self):
        for rec in self:
            rec.picking_in_cistern_qty = len(rec.picking_in_cistern_ids)

    # =========================================================================
    # 6) PICKINGS: SACOS
    # =========================================================================
    picking_in_sack_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_sack_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de sacos",
        compute="_compute_picking_in_sack_ids",
    )
    picking_in_sack_qty = fields.Float(
        string="Cantidad de sacos",
        compute="_compute_picking_in_sack_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_sack_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['raw_sack']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_sack_ids = pickings

    @api.depends('picking_in_sack_ids')
    def _compute_picking_in_sack_qty(self):
        for rec in self:
            rec.picking_in_sack_qty = len(rec.picking_in_sack_ids)

    # =========================================================================
    # 7) PICKINGS: COLOR
    # =========================================================================
    picking_in_color_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_color_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de color",
        compute="_compute_picking_in_color_ids",
    )
    picking_in_color_qty = fields.Float(
        string="Cantidad de color",
        compute="_compute_picking_in_color_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_color_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['raw_color']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_color_ids = pickings

    @api.depends('picking_in_color_ids')
    def _compute_picking_in_color_qty(self):
        for rec in self:
            rec.picking_in_color_qty = len(rec.picking_in_color_ids)

    # =========================================================================
    # 8) PICKINGS: CARTÓN
    # =========================================================================
    picking_in_cardboard_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_cardboard_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de cartón",
        compute="_compute_picking_in_cardboard_ids",
    )
    picking_in_cardboard_qty = fields.Float(
        string="Cantidad de cartón",
        compute="_compute_picking_in_cardboard_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_cardboard_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['raw_cardboard']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_cardboard_ids = pickings

    @api.depends('picking_in_cardboard_ids')
    def _compute_picking_in_cardboard_qty(self):
        for rec in self:
            rec.picking_in_cardboard_qty = len(rec.picking_in_cardboard_ids)

    # =========================================================================
    # 9) PICKINGS: BOLSAS
    # =========================================================================
    picking_in_bag_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_bag_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de bolsas",
        compute="_compute_picking_in_bag_ids",
    )
    picking_in_bag_qty = fields.Float(
        string="Cantidad de bolsas",
        compute="_compute_picking_in_bag_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_bag_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['raw_bag']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_bag_ids = pickings

    @api.depends('picking_in_bag_ids')
    def _compute_picking_in_bag_qty(self):
        for rec in self:
            rec.picking_in_bag_qty = len(rec.picking_in_bag_ids)

    # =========================================================================
    # 10) PICKINGS: pallets
    # =========================================================================

    picking_in_pallet_ids = fields.Many2many(
        'stock.picking',
        relation='analytic_distribution_inplast_bag_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Albaranes de bolsas",
        compute="_compute_picking_in_pallet_ids",
    )
    picking_in_pallet_qty = fields.Float(
        string="Cantidad de bolsas",
        compute="_compute_picking_in_pallet_qty",
    )

    @api.depends('date_from', 'date_to')
    def _compute_picking_in_pallet_ids(self):
        for rec in self:
            pickings = self.env['stock.picking'].search([
                ('scheduled_date', '>=', rec.date_from),
                ('scheduled_date', '<=', rec.date_to),
                ('move_ids_without_package.product_id.categ_id.type', 'in', ['raw_pallet']),
                ('picking_type_code', '=', 'incoming'),
            ])
            rec.picking_in_bag_ids = pickings

    @api.depends('picking_in_pallet_ids')
    def _compute_picking_in_pallet_qty(self):
        for rec in self:
            rec.picking_in_pallet_qty = len(rec.picking_in_pallet_ids)

    # =========================================================================
    # 11) sale: container
    # =========================================================================

    sale_container_ids = fields.Many2many('sale.order.line',compute='_compute_sale_container_ids',string='Sale Container')
    sale_container_qty = fields.Integer(string='Cantidad de Container',compute='_compute_sale_container_qty')

    @api.depends('date_from', 'date_to')
    def _compute_sale_container_ids(self):
        for rec in self:
            sales = self.env['sale.order.line'].search([
                ('order_id.date_order', '>=', rec.date_from),
                ('order_id.date_order', '<=', rec.date_to),
                ('state', 'in', ['sale']),
                ('bom_template_type', 'in', ['box','box_nonnrp' ]),
            ])
            parameters = self.env.ref('analytic_distribution_inplast.analytic_distribution_inplast_parameter')
            container_box_qty = parameters.container_box_qty
            sale_line_container = []
            for line in sales:
                if container_box_qty != 0 and (line.product_uom_qty % container_box_qty) == 0:
                    sale_line_container.append(line.id)

            rec.sale_container_ids = [(6,0,sale_line_container)]
    @api.depends('date_from', 'date_to')
    def _compute_sale_container_qty(self):
        for record in self:
            containers = 0
            parameters = self.env.ref('analytic_distribution_inplast.analytic_distribution_inplast_parameter')
            container_box_qty = parameters.container_box_qty
            for li  in record.sale_container_ids:
                containers += li.product_uom_qty/container_box_qty
            record.sale_container_qty = containers


    # =========================================================================
    # 12) consolidados almacen
    # =========================================================================

    picking_hour_qty = fields.Float(string='Cantidad de consolidados por hora',compute='_compute_picking_hour_qty')
    picking_balance = fields.Float(string='Balance de consolidados',compute='_compute_picking_balance')

    @api.depends('date_from', 'date_to')
    def _compute_picking_hour_qty(self):
        for rec in self:
            picking_hour_qty = 0
            parameters = self.env.ref('analytic_distribution_inplast.analytic_distribution_inplast_parameter')
            cistern_unload= parameters.raw_cistern_unload * rec.picking_in_cistern_qty
            sack_unload = parameters.raw_sack_unload * rec.picking_in_sack_qty
            color_unload = parameters.raw_color_unload * rec.picking_in_color_qty
            cardboard_unload = parameters.raw_cardboard_unload * rec.picking_in_cardboard_qty
            bag_unload = parameters.raw_bag_unload * rec.picking_in_bag_qty
            pallet_unload = parameters.raw_pallet_unload * rec.picking_in_pallet_qty
            internal_pickings = rec.days * (parameters.raw_color_relocation_daily + parameters.raw_cardboard_relocation_daily + parameters.raw_bag_relocation_daily + parameters.raw_pallet_relocation_daily)
            container_load = rec.sale_container_qty * parameters.container_load

            rec.picking_hour_qty = cistern_unload + sack_unload + color_unload + cardboard_unload + bag_unload + pallet_unload + internal_pickings + container_load



