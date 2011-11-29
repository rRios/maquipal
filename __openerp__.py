{
    'name': 'Gestion de Ordenes de Trabajo',
    'version': '1.0',
    'category': 'Gestion',
    'description': 'Gestion de ordenes de trabajo para Maquipal',
    'author': 'Raul Rios',
    'website': 'http://dinan.es',
    'depends': [
        'base',
        'base_action_rule',
        'process',
        'mail_gateway',
        'base_calendar',
        'resource',
    ],
    'init_xml': [],
    'update_xml': [
        'view/maquipal_partner_view.xml',
        'view/maquipal_comentarios_visita_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}

