from odoo import api, fields, models


class ClientNotesWizard(models.TransientModel):
    _name = 'client.notes.wizard'
    _description = 'Client Notes Wizard'

    sale_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    partner_id = fields.Many2one(related='sale_id.partner_id', string='Customer', readonly=True)
    commercial_partner_id = fields.Many2one(related='partner_id.commercial_partner_id', string='Commercial Partner',
                                            readonly=True)

    # El campo comment es de tipo HTML
    partner_note = fields.Html(related='partner_id.comment', string='Partner Note', readonly=True)
    commercial_partner_note = fields.Html(related='commercial_partner_id.comment', string='Commercial Partner Note',
                                          readonly=True)

    partner_sale_warn = fields.Selection(related='partner_id.sale_warn', string='Partner Sale Warning', readonly=True)
    # El campo sale_warn_msg es de tipo Text, no Html
    partner_sale_warn_msg = fields.Text(related='partner_id.sale_warn_msg', string='Partner Sale Warning Message',
                                        readonly=True)
    commercial_partner_sale_warn = fields.Selection(related='commercial_partner_id.sale_warn',
                                                    string='Commercial Partner Sale Warning', readonly=True)
    commercial_partner_sale_warn_msg = fields.Text(related='commercial_partner_id.sale_warn_msg',
                                                   string='Commercial Partner Sale Warning Message', readonly=True)