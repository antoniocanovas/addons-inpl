

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class MrpTool(models.Model):
    _name = "pnt.mrp.tool"
    _description = "PNT MRP Tools"

    name = fields.Char(string="Name", store=True)
    pnt_type = fields.Selection([('tool','Tool'),('accesory','Accessory'), string='Type', store=True, copy=True])
    pnt_tool_id = fields.Many2one('pnt.mrp.tool', string='Tool', copy=True, store=True)
    pnt_cycles = fields.Integer('Cycles / Speed', copy=True, store=True)
    pnt_gaps = fields.Integer('Gaps', copy=True, store=True)
    pnt_note = fields.Html(string="Notes")
