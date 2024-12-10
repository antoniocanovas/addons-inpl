# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api, _


class CommissionPlan(models.Model):
    _inherit = "commission.plan"

    def action_open_commission_wizard(self):
        self.ensure_one()

        return {
            "name": _("Comission Plan Categories Wizard"),
            "view_mode": "form",
            "view_id": self.env.ref("commission_plan_wizard.commission_plan_wizard_views").id,
            "view_type": "form",
            "res_model": "commission.plan.wizard",
            "type": "ir.actions.act_window",
            "target": "new",
            "context": {
                "default_commission_plan_id": self.id,
            },
        }
