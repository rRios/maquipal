# -*- coding: utf-8 -*-

from osv import osv, fields
from datetime import datetime

class maquipal_comentarios_visita(osv.osv):
    _name = 'maquipal.comentarios.visita'
    _description = "Comentarios de la visita"
    _columns = {
        'fecha_creacion': fields.datetime('Fecha', readonly=True),
        'texto': fields.text('Comentarios'),
        'partner_id': fields.many2one('res.partner', 'Cliente'),
    }

maquipal_comentarios_visita()
