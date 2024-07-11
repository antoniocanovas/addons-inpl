# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    def action_confirm(self):
        res = super().action_confirm()
        for record in self:
            if (record.product_id.tracking == 'lot') and (not record.lot_producing_id.id):
                if (self.company_id.pnt_mrp_lot_name == 'mo'):
                    name = record.name.split("/")[0] + record.name.split("/")[1] + record.name.split("/")[2]
                    newlot = record.env['stock.lot'].create({'name': name, 'product_id': record.product_id.id})
                    record.lot_producing_id = newlot.id
                # ... put here other "else" options to naming lot ...
            return True
