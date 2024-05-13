from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    pnt_goods_state_table = fields.Binary("State Table verification")
    pnt_logo_cert_uno = fields.Binary("logo cert uno")
    pnt_logo_cert_dos = fields.Binary("logo cert dos")
    pnt_logo_cert_tres = fields.Binary("logo cert tres")

