{
    "name": "Product Inplast",
    "summary": "Products Inplast",
    "version": "17.0.1.0.0",
    "category": "Product, Picking",
    "author": "Punt Sistemes",
    "website": "https://www.puntsistemes.es",
    "Maintainers": [
        "Equipo rojo",
    ],
    "license": "LGPL-3",
    "depends": [
        "product",
        "stock",
        "account",
        "mrp",
        "report_qweb_pdf_watermark",
        "mrp_lot_name",
        "custom_inplast",
        "l10n_es_aeat_mod592",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_company_views.xml",
        "views/product_template_views.xml",
        "views/product_category_views.xml",
        "views/menu_views.xml",
        "data/stock_package_type.xml",
    ],
    "installable": True,
}
