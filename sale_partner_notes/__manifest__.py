{
    "name": "sale_partner_notes",
    "summary": "Adds a button in the sales order to consult the partner's notes and their related company.",
    "version": "17.0.1.0.0",
    "category": "sale",
    "author": "Punt Sistemes",
    "website": "https://www.puntsistemes.es",
    "Maintainers": [
        "Punt Sistemes",
    ],
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        'security/ir.model.access.csv',
        'wizards/client_notes_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
    "installable": True,
}
