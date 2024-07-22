from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'delivery.carrier'

    pnt_agency_or_carrier = fields.Char(string='Agency or Carrier')
    pnt_address = fields.Char(string='Address')
    pnt_cif = fields.Char(string='CIF')

    pnt_driver_name = fields.Char(string='Driver Name')
    pnt_driver_id = fields.Char(string='Driver ID')
    pnt_license_plate = fields.Char(string='License Plate')
    pnt_trailer_container = fields.Char(string='Trailer / Container')

    pnt_print_picking_list = fields.Boolean("Print picking list")



