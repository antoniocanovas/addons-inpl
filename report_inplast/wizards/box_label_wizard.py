from odoo import api, fields, models


class BoxLabelWizard(models.TransientModel):
    _name = 'box.label.wizard'
    _description = 'Box Label Wizard'

    # Core fields
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', required=True)
    machine_id = fields.Many2one('mrp.workcenter', string='Machine')

    # Related product fields
    product_id = fields.Many2one('product.product', string='Product',
                                 related='production_id.product_id', readonly=True)
    product_base_id = fields.Many2one('product.template', string='Base Product',
                                      compute='_compute_product_base_id', readonly=True)
    tool_id = fields.Many2one('mrp.product.tool', string='Tool',
                              related='production_id.mrp_tool_id', readonly=True)

    # Label numbering and quantity fields
    base_qty = fields.Integer(string='Units per Box', help='Number of caps per pallet / number of boxes',
                              compute='_compute_base_qty', store=True)
    last_printed_label = fields.Integer(string='Last Printed Label', default=0)
    from_label = fields.Integer(string='Start From', default=0)
    color = fields.Char(string='Color', compute='_compute_color', readonly=True)
    quantity = fields.Integer(string='Number of Labels to Print', default=1)

    @api.depends('product_id')
    def _compute_product_base_id(self):
        """Compute the base product id safely"""
        for wizard in self:
            wizard.product_base_id = False
            if wizard.product_id and hasattr(wizard.product_id, 'pnt_parent_id'):
                wizard.product_base_id = wizard.product_id.pnt_parent_id

    @api.depends('product_id', 'product_base_id')
    def _compute_base_qty(self):
        """Compute the base quantity based on the product's parent product"""
        for wizard in self:
            wizard.base_qty = 0
            if wizard.product_id and hasattr(wizard.product_id, 'pnt_parent_qty') and \
                    hasattr(wizard.product_id, 'pnt_box_qty') and \
                    wizard.product_id.pnt_box_qty and wizard.product_id.pnt_box_qty > 0:
                wizard.base_qty = int(wizard.product_id.pnt_parent_qty / wizard.product_id.pnt_box_qty)

    @api.depends('product_id')
    def _compute_color(self):
        """Safely compute the color"""
        for wizard in self:
            wizard.color = False
            if wizard.product_id and hasattr(wizard.product_id, 'product_base_dye'):
                wizard.color = wizard.product_id.product_base_dye

    @api.onchange('production_id')
    def _onchange_production_id(self):
        """Initialize the last_printed_label and from_label when the production changes"""
        for wizard in self:
            last_label = 0
            if wizard.production_id and wizard.production_id.lot_producing_id:
                last_label = wizard.production_id.lot_producing_id.last_printed_label or 0

            wizard.last_printed_label = last_label
            wizard.from_label = last_label

    def action_print_box_label(self):
        """Print the box label report multiple times and update the lot"""
        self.ensure_one()

        # First, update the lot's last_printed_label field with the new value
        if self.production_id.lot_producing_id:
            # Update the last printed label on the lot (last used + quantity)
            new_last_label = self.from_label + self.quantity
            self.production_id.lot_producing_id.last_printed_label = new_last_label

        # Generate duplicate production records for the number of copies
        duplicate_productions = self.env['mrp.production']
        start_label = self.from_label

        for i in range(self.quantity):
            # Add context for the current label number for this copy
            duplicate_productions = duplicate_productions.with_context(
                current_label_number=start_label + i
            )
            duplicate_productions += self.production_id

        # Call the report with the new recordset containing duplicates
        # and pass the wizard values as context
        return self.env.ref('report_inplast.action_report_box_label').with_context({
            'machine_id': self.machine_id.id if self.machine_id else False,
            'base_qty': self.base_qty,
            'from_label': self.from_label,
            'color': self.color,
        }).report_action(duplicate_productions)