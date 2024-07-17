{
    "name": "Informes personalizados",
    "summary": "Modificaciones de informes, nuevos informes, mejoras y añadidos",
    "version": "17.0.1.0.1",
    "category": "Customizations",
    "website": "https://www.puntsistemes.es",
    "author": "Punt Sistemes",
    "maintainers": [
        "PuntSistemes S.L.U"
    ],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_management",
        "account",
        "stock",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/templates.xml",
        "reports/pnt_report_delivery.xml",
        "views/res_company_views.xml",
        "reports/external_layout.xml",
        "reports/coa_product_document.xml",
        "views/picking_report_views.xml",
    ],
}
