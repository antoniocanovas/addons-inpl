# Copyright Puntsistemes SL


from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import re

_digits_re = re.compile(r"^[0-9]+$")
ir_sequence = "ir.sequence"


class IrSequence(models.Model):
    _inherit = ir_sequence

    pnt_extension_digit = fields.Integer(string="SSCC extension digit", size=1)

    def action_open_sscc_sequence(self):

        res_id = self.search([("code", "=", "pnt.sscc.code")], limit=1)
        return {
            "name": _("SSCC Sequence"),
            "type": "ir.actions.act_window",
            "res_model": ir_sequence,
            "view_mode": "form",
            "view_type": "form",
            "view_id": self.env.ref(
                "pnt_sscc_generator_base.pnt_sscc_sequence_view"
            ).id,
            "res_id": res_id.id,
            "target": "new",
        }

    def isdigits(self, number):
        try:
            return bool(_digits_re.match(number))
        except ValidationError:
            return False

    @api.onchange("prefix")
    def validate(self):
        if self.code == "seq.sscc.code":
            if self.prefix and not self.isdigits(self.prefix):
                raise ValidationError(_("SSCC prefix must be only numbers "))
