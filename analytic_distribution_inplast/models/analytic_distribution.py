# -*- coding: utf-8 -*-
# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from docutils.nodes import container
from odoo import fields, models, api
from odoo.exceptions import UserError

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
        string="Handle pickings",
        compute="_compute_picking_in_handles_ids",
    )
    picking_in_handles_qty = fields.Float(
        string="Handle pickings qty",
        compute="_compute_picking_in_handles_qty",
        store=True,
    )
    picking_in_pallet_handles_qty = fields.Float(
        string="Handle pallets received",
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
        string="Cap pickings",
        compute="_compute_picking_in_caps_ids",
    )
    picking_in_caps_qty = fields.Float(
        string="Cap picking qty",
        compute="_compute_picking_in_caps_qty",
        store=True,
    )
    picking_in_pallet_caps_qty = fields.Float(
        string="Cap pallets received",
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
        string="Cap sale orders",
        compute="_compute_sale_caps_order_ids",
    )
    sale_caps_order_count = fields.Integer(
        string="Cap orders qty",
        compute="_compute_sale_caps_order_count",
    )
    sale_caps_order_qty = fields.Float(
        string="Cap pallet sales",
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
        string="Handle sale orders",
        compute="_compute_sale_handles_order_ids",
    )
    sale_handles_order_count = fields.Integer(
        string="Handle orders qty",
        compute="_compute_sale_handles_order_count",
    )
    sale_handles_order_qty = fields.Float(
        string="Handle pallets sales",
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
        string="Cistern pickings",
        compute="_compute_picking_in_cistern_ids",
    )
    picking_in_cistern_qty = fields.Float(
        string="Cistern qty",
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
        string="Sack pickings",
        compute="_compute_picking_in_sack_ids",
    )
    picking_in_sack_qty = fields.Float(
        string="Sack pikings qty",
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
        string="Color pickings in",
        compute="_compute_picking_in_color_ids",
    )
    picking_in_color_qty = fields.Float(
        string="Color picking in qty",
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
        string="Cardboard pikings",
        compute="_compute_picking_in_cardboard_ids",
    )
    picking_in_cardboard_qty = fields.Float(
        string="Cardboard piking qty",
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
        string="Bag pickings",
        compute="_compute_picking_in_bag_ids",
    )
    picking_in_bag_qty = fields.Float(
        string="Bag pickings qty",
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
        relation='analytic_distribution_inplast_pallet_rel',
        column1='analytic_distribution_id',
        column2='picking_id',
        string="Pallet pickings in",
        compute="_compute_picking_in_pallet_ids",
    )
    picking_in_pallet_qty = fields.Float(
        string="Pallet pickings in qty",
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
            rec.picking_in_pallet_ids = pickings

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
            internal_pickings = rec.days * (parameters.raw_color_reloc_daily + parameters.raw_cardboard_reloc_daily + parameters.raw_bag_reloc_daily + parameters.raw_pallet_reloc_daily)
            container_load = rec.sale_container_qty * parameters.container_load

            rec.picking_hour_qty = cistern_unload + sack_unload + color_unload + cardboard_unload + bag_unload + pallet_unload + internal_pickings + container_load



    # =========================================================================
    # MÉTODOS DE CÁLCULO PARA DISTRIBUCIONES ANALÍTICAS:
    # =========================================================================

    def compute_distribution(self):
        """Extend this function with custom Inplast analytic compute modes"""
        super().compute_distribution()
        self.env["account.analytic.line"].search(
            [("analytic_distribution_id", "=", self.id)]
        ).unlink()
        for li in self.line_ids:
            if li.template_id.compute_method == "demo":
                a=1
                #raise UserError("ok")
            elif li.template_id.compute_method == "r13":
                self.compute_r13(li)
            elif li.template_id.compute_method in ["r14","r15"]:
                self.compute_r14(li)
            elif li.template_id.compute_method == "r22":
                self.compute_r22(li)


    def compute_r13(self, li):
        datefrom = self.date_from
        dateto = self.date_to
        total_kwh = 0  # Total de kWh consumidos por todas las máquinas
        workcenters = li.template_id.workcenter_ids
        balance = li.balance  # El coste a distribuir

        # Wororders entre fechas:
        workorders = self.env["mrp.workorder"].search(
            [
                ("workcenter_id", "in", workcenters.ids),
                ("date_start", ">=", datefrom),
                ("date_start", "<=", dateto),
            ]
        )

        # Inicialización de listas simples
        mrpproducts = []
        product_total_kwh = []

        # Cálculo del total de kWh consumidos
        for wo in workorders:
            product = wo.product_id
            duration = wo.duration
            machine = wo.workcenter_id

            # Identificamos productos únicos y agregamos a la lista si no están
            if product not in mrpproducts:
                mrpproducts.append(product)
                product_total_kwh.append(0)  # Inicializamos su consumo total a 0

            # Calculamos el consumo de kWh
            kwh_consumed = duration * machine.power_kw
            total_kwh += kwh_consumed

            # Actualizamos el consumo total por producto
            product_index = mrpproducts.index(product)
            product_total_kwh[product_index] += kwh_consumed

        # Verificar si hay consumo total de kWh para evitar la división por cero
        if total_kwh == 0:
            raise UserError("No hay consumo de energía registrado.")

        # Crear entradas analíticas para cada producto
        for i in range(len(mrpproducts)):
            product = mrpproducts[i]
            product_kwh = product_total_kwh[i]

            machine_percentage = (product_kwh / total_kwh) * 100
            machine_cost = (balance * machine_percentage) / 100

            # Buscar la cuenta analítica para el producto base tapón, o crearla:
            analytic_product = product
            if product.pnt_product_type == 'packing':
                analytic_product = product.pnt_parent_id

            analytic_account = self.env['account.analytic.account'].search([
                ('product_id','=',analytic_product.id)
            ])
            if not analytic_account.id:
                analytic_account = self.env['account.analytic.account'].create({
                    'product_id': analytic_product.id,
                    'plan_id': self.env.company.analytic_product_plan_id.id,
                    'name': analytic_product.name,
                })

            # Buscar el nombre del campo creado dinámicamente:
            analytic_field_name = self.env['ir.model.fields'].search([
                ('model','=','account.analytic.line'),
                ('ttype','=','many2one'),
                ('field_description','=',analytic_account.plan_id.name),
            ]).name

            self.env["account.analytic.line"].create(
                {
                    "name": f"Consumo {product.name}",
                    "amount": machine_cost,
                    "product_id": product.id,
                    "date": fields.Date.today(),
                    "analytic_distribution_id": self.id,
                    analytic_field_name: analytic_account.id,
                }
            )

        return True

    def compute_r14(self):
        datefrom = self.date_from
        dateto = self.date_to
        total_duration = 0  # Total de kWh consumidos por todas las máquinas
        workcenters = self.workcenter_ids
        amount = self.amount  # El máximo coste a distribuir

        # Órdenes de manufactura consideradas entre fechas:
        workorders = self.env["mrp.workorder"].search(
            [
                ("workcenter_id", "in", workcenters.ids),
                ("date_start", ">=", datefrom),
                ("date_start", "<=", dateto),
            ]
        )

        # Inicialización de listas simples
        mrpproducts = []
        product_total_duration = []

        # Cálculo del total de kWh consumidos
        for wo in workorders:
            product = wo.product_id
            duration = wo.duration
            machine = wo.workcenter_id

            # Identificamos productos únicos y agregamos a la lista si no están
            if product not in mrpproducts:
                mrpproducts.append(product)
                product_total_duration.append(0)  # Inicializamos su consumo total a 0

            total_duration += duration

            # Actualizamos el consumo total por producto
            product_index = mrpproducts.index(product)
            product_total_duration[product_index] += duration

        # Verificar si hay consumo total de kWh para evitar la división por cero
        if total_duration == 0:
            raise UserError("No hay consumo de energía registrado.")

        # Crear entradas analíticas para cada producto
        for i in range(len(mrpproducts)):
            product = mrpproducts[i]
            product_kwh = product_total_duration[i]

            machine_percentage = (product_kwh / total_duration) * 100
            machine_cost = (amount * machine_percentage) / 100

            self.env["account.analytic.line"].create(
                {
                    "name": f"Consumo {product.name}",
                    "amount": machine_cost,
                    "product_id": product.id,
                    "date": fields.Date.today(),
                    "analytic_distribution_id": self.id,
                }
            )

        return True

    def compute_r22(self):
        # El chequeo de región es el siguiente: país = España (ES), o posición fiscal "intracomuntaria" (EU) y otros.
        # La parametrización está hecha:
        analytic_spain = self.env.company.analytic_spain_account_id.id
        analytic_eu= self.env.companyanalytic_eu_account_id.id
        analytic_noneu = self.env.company.analytic_non_eu_account_id.id
        amount = self.amount

        fiscal_position_eu_external_id = "account." + self.company.id + "_" + "fp_intra"
        partner_eu = self.env.ref(fiscal_position_eu_external_id)

        if not analytic_spain.id or not analytic_eu.id or not analytic_noneu.id:
            raise UserError('Go to company => Analytic parametrization and assign region accounts.')

        # Cálculo para España: Todos los account.move.line de las cuentas, cuyo partner.country_id es España.
        #  Es UE si la posición fiscal es partner_eu.id; el resto a "Resto del mundo".

        #  Se hace el porcentaje sobre el total de venta,
        #  Se crea array de familia que ha sido cada venta (por array de venta, familia),
        #  Si existe cuenta analítica para esta familia, se añade apunte contable, en otro caso se crea y después añade.

        # El array podría ser: [ 'region', 'familia' , 'importe']
        # Después calcular en base al array.
        return True