{
    "name": "MRP Inplast",
    "summary": "MRP Inplast",
    "version": "17.0.1.0.0",
    'category': 'MRP',
    "author": "Punt Sistemes",
    "website": "https://www.puntsistemes.es",
    "Maintainers":[
        "Punt Sistemes",
    ],
    "license": "LGPL-3",
    "depends": [
        "product",
        "stock",
        "mrp",
        "maintenance",
        "mrp_maintenance",
        "custom_inplast",
        "product_inplast",
    ],
    "data": [
        "views/res_company_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/product_template_views.xml",
        "views/mrp_bom_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
}
