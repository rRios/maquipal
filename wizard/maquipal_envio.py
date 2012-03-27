# -*- coding: utf-8 -*-

from osv import osv, fields

class maquipal_envio(osv.osv_memory):
    """ Envio de nota a otro usuario """
    _name = 'maquipal.envio'
    _description = 'Envio de nota a otro usuario'
    _columns = {
        'usuario_destino': fields.many2one('res.users', 'Enviar a'),
    }

    def action_maquipal_envio(self, cr, uid, ids, context=None):
        pass

maquipal_envio()