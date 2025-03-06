from odoo import api, models
import datetime


class BoxLabelReport(models.AbstractModel):
    _name = 'report.report_inplast.report_box_label'
    _description = 'Box Label Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        This method prepares data for the report template
        """
        # If docids are not provided, get them from data
        if not docids and data and data.get('ids'):
            docids = data.get('ids')

        # Get the MO record(s)
        docs = self.env['mrp.production'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'mrp.production',
            'docs': docs,
            'data': data,
            'datetime': datetime,  # Make datetime available in the template
        }