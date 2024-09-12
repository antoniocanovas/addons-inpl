# Copyright Puntsistemes - 2024
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "SSCC code Generator",
    "summary": "Generation of SSCC codes based on customer prefix",
    "version": "17.0.1.0.1",
    "category": "stock",
    "author": "Pedro Guirao Puntsistemes, Adrian Muñoz Puntsistemes",
    "website": "https://www.puntsistemes.es",
    "license": "AGPL-3",
    "depends": [],
    "data": [
        "views/pnt_menu.xml",
        "data/ir_sequence_data.xml",
        "views/pnt_ir_sequence_view.xml",
    ],
    "external_dependencies": {
        "python": [
            "gtin",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
