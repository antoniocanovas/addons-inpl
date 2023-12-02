# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    pnt_mrp_tool_categ = fields.Many2one('maintenance.equipment.category', string='Tools category',
                                         store=True, help="Injections or pressure Molds")
    pnt_mrp_accesory_categ = fields.Many2one('maintenance.equipment.category', string='Accesories category',
                                             store=True, help="Accesories for molds")
