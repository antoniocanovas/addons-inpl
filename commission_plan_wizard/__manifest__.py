{
    'name': 'Logistic Inplast',
    'version': '17.0.1.0.0',
    'category': '',
    'description': u"""
Commision wizard to add several categs with the same commission.
""",
    'author': 'Punt Sistemes SL',
    'depends': [
        'crm',
        'partner_commission',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/commission_plan_wizard_views.xml',
    ],
    'installable': True,
}
