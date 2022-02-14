# -*- coding: utf-8 -*-
{
    'name': 'Gestión de grupos',
    'summary': 'Módulo que pretende facilitar la gestión de grupos musicales',
    'description': 'Módulo que pretende facilitar la gestión de grupos musicales centralizando en una sola app los datos de los grupos, músicos, instrumentos, recintos de concierto, etc...',
    'author': "Adrián Castro Villacañas",
    'website': "https://github.com/Desun92/Gestion-de-grupos.git",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    
    'category': 'Musical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','personas'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}
