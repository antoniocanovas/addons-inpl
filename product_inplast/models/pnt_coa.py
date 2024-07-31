

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

TYPE = [
    ('normal', 'estandar'),
    ('asas', 'asa'),
    ('nmp', 'NMP'),
    ('buxton', 'Buxton'),
]

class PntCoa(models.Model):
    _name = "pnt.coa"
    _description = "COA fields"

    name = fields.Char(
        string="Name"
    )
    type = fields.Selection(selection=TYPE)
    print_multicolor = fields.Boolean("Multicolor print")
    body_multicolor = fields.Html("Multicolor table")
    print_quality_meassure = fields.Boolean("Quality meassures")
    print_components = fields.Boolean("Components print")
    body_components = fields.Html("Components table")
    pnt_coa_body = fields.Html(
        string="Body"
    )

    material_number = fields.Char("Material Number")
    specification_number = fields.Char("Specifitacion Number")
    vendor_site_number = fields.Char("Vendor Site Number")