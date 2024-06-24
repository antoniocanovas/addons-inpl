# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def get_split_mrp_as_serial(self):

        for li in self.finished_move_line_ids:
            qty = int(li.quantity - 1)
            li.write({'quantity': 1})
            for i in range(qty):
                self.env['stock.move.line'].create(
                    {'product_id': li.product_id.id, 'production_id': self.id,
                     'quantity': 1, 'state': 'confirmed', 'move_id': li.move_id.id})


    def action_confirm(self):
        res = super().action_confirm()
        if self.product_id.pnt_mrp_as_serial:
            self.get_split_mrp_as_serial()
        return True

    def update_lot_as_serial(self):
        seq = self.lot_producing_id.pnt_mrp_serial
        mo_lot = self.lot_producing_id

        for li in self.finished_move_line_ids:
            name = mo_lot.name + "." + str(seq)
            lot = self.env['stock.lot'].search([('product_id', '=', li.product_id.id), ('name', '=', name)])
            if not lot.id:
                lot = self.env['stock.lot'].create({'product_id': li.product_id.id, 'name': name})
            li.write({'lot_id': lot.id})
            seq += 1

        mo_lot.write({'pnt_mrp_serial': seq})

        # Unreserve / Reserve, original lot => New lots:
        pickings, productions = [], []
        sml = self.env['stock.move.line'].search(
            [('product_id', '=', self.product_id.id), ('lot_id', '=', mo_lot.id)])
        for li in sml:
            if (li.picking_id.id) and (li.picking_id not in pickings):
                pickings.append(li.picking_id)
            if (li.production_id.id) and (li.production_id not in productions):
                productions.append(li.production_id)

        for pi in pickings:
            pi.do_unreserve()
            pi.action_assign()

        for mo in productions:
            mo.do_unreserve()
            mo.action_assign()

    def button_mark_done(self):
        res = super().button_mark_done()
        if self.product_id.pnt_mrp_as_serial:
            self.update_lot_as_serial()
        return res