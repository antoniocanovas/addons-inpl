from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_client_notes(self):
        """Open the client notes wizard"""
        return {
            'name': 'Client Notes',
            'type': 'ir.actions.act_window',
            'res_model': 'client.notes.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_id': self.id,
            },
        }