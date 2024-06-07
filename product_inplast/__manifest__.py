{
    "name": "recepcion personalizada",
    "summary": "añade un check obligatorio para evitar hacer el check in sin leer antes las politicas de la compañia",
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
        "frontdesk",
        "website"
    ],
    "data": [
        'views/frontdesk_visitor_views.xml'

    ],

    'assets': {
        'frontdesk.assets_frontdesk': [

            'pnt_frontdesk_inplast/static/views/frontdesk_view.xml',
        ],

    },

}
