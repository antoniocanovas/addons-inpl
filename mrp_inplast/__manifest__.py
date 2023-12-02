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
        "custom_inplast",
    ],
    "data": [
        "views/res_company_views.xml",
        "views/maintenance_equipment_views.xml",
        "views/product_template_views.xml",
# Versión 1 (para borrar):
#        "security/ir.model.access.csv",
#        "views/mrp_tool_views.xml",
#        "views/menu_views.xml",
    ],
    "installable": True,
}
