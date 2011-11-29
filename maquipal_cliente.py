# -*- coding: utf-8 -*-

from osv import fields, osv

class res_partner(osv.osv):
    _name = 'res.partner'
    _description = 'Cliente'
    _inherit = 'res.partner'
    _columns = {
        'actividad': fields.char('Actividad', size=64),
        'riesgo': fields.char('Riesgo', size=64),
        'comentarios': fields.one2many('maquipal.comentarios.visita','partner_id','Comentarios'),
    } 
    
res_partner()
