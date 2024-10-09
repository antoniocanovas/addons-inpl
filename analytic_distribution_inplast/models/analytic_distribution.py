from odoo import fields, models, api
from odoo.exceptions import UserError


class AnalyticDistribution(models.Model):
    _inherit = "analytic.distribution"

    compute_mode = fields.Selection(
        [
            ("demo", "demo INPLAST"),
            ("r13", "R13.- Electricidad"),
            ("r14", "Reparto 14"),
        ]
    )

    workcenter_ids = fields.Many2many("mrp.workcenter", string="Workcenters")

    def compute_distribution(self):
        """Extend this function with custom Inplast analytic compute modes"""
        super().compute_distribution()
        self.env["account.analytic.line"].search(
            [("analytic_distribution_id", "=", self.id)]
        ).unlink()
        self.inplast_computed_modes()

    def inplast_computed_modes(self):
        if self.compute_mode == "demo":
            raise UserError("ok")
        elif self.compute_mode == "r13":
            self.compute_r13()
        elif self.compute_mode == "r14":
            self.compute_r14()

    def compute_r13(self):
        datefrom = self.date_from
        dateto = self.date_to
        total_kwh = 0  # Total de kWh consumidos por todas las máquinas
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

        # Crear o actualizar entradas analíticas para cada producto
        for i in range(len(mrpproducts)):
            product = mrpproducts[i]
            product_kwh = product_total_kwh[i]

            machine_percentage = (product_kwh / total_kwh) * 100
            machine_cost = (amount * machine_percentage) / 100

            existing_line = self.env["account.analytic.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("date", ">=", datefrom),
                    ("date", "<=", dateto),
                ],
                limit=1,
            )

            self.env["account.analytic.line"].create(
                {
                    "name": f"Consumo {product.name}",
                    "amount": -machine_cost,
                    "product_id": product.id,
                    "date": fields.Date.today(),
                    "analytic_distribution_id": self.id,
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

        # Crear o actualizar entradas analíticas para cada producto
        for i in range(len(mrpproducts)):
            product = mrpproducts[i]
            product_kwh = product_total_duration[i]

            machine_percentage = (product_kwh / total_duration) * 100
            machine_cost = (amount * machine_percentage) / 100

            existing_line = self.env["account.analytic.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("date", ">=", datefrom),
                    ("date", "<=", dateto),
                ],
                limit=1,
            )

            self.env["account.analytic.line"].create(
                {
                    "name": f"Consumo {product.name}",
                    "amount": -machine_cost,
                    "product_id": product.id,
                    "date": fields.Date.today(),
                    "analytic_distribution_id": self.id,
                }
            )

        return True
