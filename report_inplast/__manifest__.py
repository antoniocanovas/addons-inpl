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
        "views/res_partner_views.xml",
        "views/templates.xml",
        "views/pnt_report_delivery.xml",
        "views/res_company_views.xml",
    ],
}
