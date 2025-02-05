from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    pnt_goods_state_table = fields.Binary("Tabla verificacion albaran")
    pnt_logo_cert_uno = fields.Binary("Logo albaran cabecera uno")
    pnt_logo_cert_dos = fields.Binary("Logo albaran cabecera dos")
    pnt_logo_cert_tres = fields.Binary("Logo COAs cabecera")

