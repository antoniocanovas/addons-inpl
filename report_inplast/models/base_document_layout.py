from odoo import models, fields, api

class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    pnt_goods_state_table = fields.Binary(related='company_id.pnt_goods_state_table', readonly=True)
    pnt_logo_cert_uno = fields.Binary(related='company_id.pnt_logo_cert_uno', readonly=True)
    pnt_logo_cert_dos = fields.Binary(related='company_id.pnt_logo_cert_dos', readonly=True)
    pnt_logo_cert_tres = fields.Binary(related='company_id.pnt_logo_cert_tres', readonly=True)