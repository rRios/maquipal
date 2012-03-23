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
        'base_calendar',
        'resource',
        'product',
        'crm',
    ],
    'init_xml': [],
    'update_xml': [
        'view/maquipal_partner_view.xml',
        'view/maquipal_maquina_view.xml',
        'view/maquipal_nota_view.xml',
        'workflow/maquipal_workflow.xml',
    ],
    'demo_xml': [],
    'test': [
            'test/test_maquipal_cliente.yml',
            'test/test_maquipal_maquina.yml',
            'test/test_maquipal_nota.yml',
            ],
    'installable': True,
    'auto_install': False,
}

