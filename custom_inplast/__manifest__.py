{
    "name": "Custom Inplast",
    "summary": "Customs Inplast",
    "version": "17.0.1.0.0",
    'category': 'Product, Picking',
    "author": "Punt Sistemes",
    "website": "https://www.puntsistemes.es",
    "Maintainers":[
        "Equipo rojo",
    ],
    "license": "LGPL-3",
    "depends": [
        "stock",
        "account",
        "l10n_es_partner",
        "partner_phone_secondary",
        "partner_commission",
    ],
    "data": [
        "views/stock_location_views.xml",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
        "views/res_partner_views.xml",
        "views/mig_views.xml",
        "security/ir.model.access.csv",
        "views/menu_views.xml",
    ],
    "installable": True,
}
