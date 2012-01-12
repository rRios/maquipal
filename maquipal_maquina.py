# -*- coding: utf-8 -*-

from osv import fields, osv

class product_product(osv.osv):
    _name = 'product.product'
    _description = 'Maquina'
    _inherit = 'product.product'
    _columns = {
        'modelo': fields.char('Modelo', size=64, required=True),
        'serie': fields.char('Serie', size=64, required=True),
        'cliente_id': fields.many2one('res.partner', 'Cliente', required=True),
        'mod_motor': fields.char('Mod. Motor', size=64),
        'serie_motor': fields.char('Serie Motor', size=64),
        'mod_convertidor': fields.char('Mod. Convertidor', size=64),
        'serie_convertidor': fields.char('Serie Convertidor', size=64),
        'f_combustible': fields.char('F. Combustible', size=64),
        'f_aceite': fields.char('F. Aceite', size=64),
        'f_aire_ext': fields.char('F. Aire Ext', size=64),
        'f_aire_int': fields.char('F. Aire Int', size=64),
        'f_hidraulico': fields.char('F. Hidraulico', size=64),
        'f_convertidor': fields.char('F. Convertidor', size=64),
        't_dientes': fields.char('T. Dientes', size=64),
        'correa_alter': fields.char('Correa Alternador', size=64),
        'correa_venti': fields.char('Correa Ventilador', size=64),
        'alternador': fields.char('Alternador', size=64),
        'm_arranque': fields.char('M. Arranque', size=64),
        'ruedas': fields.char('Ruedas', size=64),
        'mastil': fields.char('Mastil', size=64),
        'bateria': fields.char('Bateria', size=64),
        'comentarios': fields.text('Comentarios'),
    }

product_product()

