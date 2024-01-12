# Copyright Puntsistemes SL


from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import re

_digits_re = re.compile(r'^[0-9]+$')
ir_sequence = 'ir.sequence'

class IrSequence(models.Model):
    _inherit = ir_sequence

    pnt_ean14_prefix = fields.Char(string="EAN-14 prefix", size=1)

    def action_open_ean_sequence(self):

        res_id = self.search([('code', '=', "pnt.product.ean.code")], limit=1)
        print(res_id)
        return {
            'name': _("EAN Sequence"),
            'type': 'ir.actions.act_window',
            'res_model': ir_sequence,
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('pnt_product_ean_barcode.pnt_sequence_view').id,
            'res_id': res_id.id,
            'target': 'new',
        }

    def action_open_internal_ean_sequence(self):

        res_id = self.search([('code', '=', "pnt.product.internal.ean.code")],
                                              limit=1)
        print(res_id)
        return {
            'name': _("Internal EAN Sequence"),
            'type': 'ir.actions.act_window',
            'res_model': ir_sequence,
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('pnt_product_ean_barcode.pnt_sequence_view').id,
            'res_id': res_id.id,
            'target': 'new',
        }

    def isdigits(self, number):
        try:
            return bool(_digits_re.match(number))
        except ValidationError:
            return False

    @api.onchange('prefix','pnt_ean14_prefix')
    def validate(self):
        if self.code == 'pnt.product.ean.code' or self.code == 'pnt.product.internal.ean.code':
            if self.prefix and not self.isdigits(self.prefix):
                    raise ValidationError(
                        _(
                            "EAN prefix must be only numbers "
                        )
                    )
            if self.pnt_ean14_prefix and not self.isdigits(self.pnt_ean14_prefix):
                    raise ValidationError(
                        _(
                            "EAN-14 prefix must be only numbers "
                        )
                    )
