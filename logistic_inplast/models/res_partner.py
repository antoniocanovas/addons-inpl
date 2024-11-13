from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    container_type_ids = fields.One2many('container.type', 'partner_id', string="Containers")
