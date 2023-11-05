from odoo import _, api, fields, models
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def upd_res_partner_lock(self):
        customers = self.env['res.partner'].search([('customer_rank','>',0)])
        now = date.today()
        pricelist_days = self.env.user.company_id.pnt_pricelist_day_lock
        lock_date = now + timedelta(days = pricelist_days)
#        for customer in customers:
#            if customer.property_product_pricelist.pnt_tracking_date
        return True
