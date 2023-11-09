from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

#    @api.onchange('parent_id')
#    def _get_pricelist_mode(self):
#        if self.parent_id.id:
#            self.pnt_pricelist_mode = self.parent_id.pnt_pricelist_mode
    pnt_pricelist_mode   = fields.Selection([('auto','Automático'),
                                             ('bom', 'Escandallo general'),
                                             ('custom', 'Escandallo personalizado')], readonly=False,
                                            store=True, copy=True, related='parent_id.pnt_pricelist_mode')

    @api.onchange('parent_id')
    def _get_pricelist_update(self):
        if self.parent_id.id:
            self.pnt_pricelist_update = self.parent_id.pnt_pricelist_update
    pnt_pricelist_update = fields.Selection([('1m', 'Monthly'),
                                             ('3m', 'Quarter'),
                                             ('6m', '6 months'),
                                             ('custom', 'Negociación')],
                                            store=True, copy=True, compute='_get_pricelist_update')

#    @api.onchange('parent_id')
#    def _get_pricelist_mode_update(self):
#        if self.parent_id.id:
#            self.write({'pnt_pricelist_mode': self.parent_id.pnt_pricelist_mode,
#                        'pnt_pricelist_update': self.parent_id.pnt_pricelist_update})
