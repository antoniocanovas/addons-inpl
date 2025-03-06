from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_open_box_label(self):
        self.ensure_one()
        return {
            'name': 'Box Label',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'box.label.wizard',
            'target': 'new',
            'context': {
                'default_production_id': self.id,
            }
        }