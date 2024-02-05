# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    pnt_raw_percent = fields.Float('Percent')

    @api.depends('bom_id.pnt_raw_type')
    def _get_percent_hide(self):
        hide = True
        if self.bom_id.pnt_raw_type: hide = False
        self.pnt_percent_hide = hide
    pnt_percent_hide = fields.Boolean('Hide percent', compute='_get_percent_hide')