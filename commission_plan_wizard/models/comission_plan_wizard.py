from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ComissionPlanWizard(models.TransientModel):
    _name = "commission.plan.wizard"
    _description = "Comission Plan Edit Wizard"

    name = fields.Char("Name")
    commission_plan_id = fields.Many2one(
        "commission.plan", string="Commission Plan"
    )
    product_category_ids = fields.Many2many("product.category", string="Product category")
    rate = fields.Float(string="Rate")

    def process(self):
        commission_plan = self.env["commission.plan"].search(
            [("id", "=", self.commission_plan_id.id)]
        )
        commission_plan.commission_rule_ids.unlink()
        for category in self.product_category_ids:
            self.env["commission.rule"].create(
                {
                    "plan_id": self.commission_plan_id.id,
                    "category_id": category.id,
                    "rate": self.rate,
                }
            )
