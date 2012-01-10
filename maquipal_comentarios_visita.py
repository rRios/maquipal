# -*- coding: utf-8 -*-

from osv import osv, fields
import time

class maquipal_comentarios_visita(osv.osv):
    _name = 'maquipal.comentarios.visita'
    _description = "Comentarios de la visita"
    _columns = {
        'fecha_creacion': fields.date('Fecha', readonly=True, select=True),
        'texto': fields.text('Comentarios'),
        'partner_id': fields.many2one('res.partner', 'Cliente', readonly=True),
    }
    _defaults = {
        'fecha_creacion': lambda *a: time.strftime("%d/%m/%Y"),
    }

maquipal_comentarios_visita()
