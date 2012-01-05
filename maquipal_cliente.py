# -*- coding: utf-8 -*-

from osv import fields, osv
import time

class res_partner(osv.osv):
    def get_fecha_ultima_visita(self, cr, uid, ids, field_name, arg, context):
        res = {}
        
        for id in ids:
            comentarios = self.pool.get('maquipal.comentarios.visita').search(cr, uid, [('partner_id', '=', id)])
            if len(comentarios)>0:
                ultimo = self.pool.get('maquipal.comentarios.visita').browse(cr, uid, comentarios[-1])
                campo =  ultimo.fecha_creacion
                c = time.strptime(campo,"%Y-%m-%d")
                res[id] = time.strftime("%d/%m/%Y",c)

        return res
    
    _name = 'res.partner'
    _description = 'Cliente'
    _inherit = 'res.partner'
    _columns = {
        'actividad': fields.char('Actividad', size=64),
        'riesgo': fields.char('Riesgo', size=64),
        'comentarios': fields.one2many('maquipal.comentarios.visita','partner_id','Comentarios'),
        #'ultima_visita': fields.date('Ultima Visita', readonly=True),
        'ultima_visita': fields.function(get_fecha_ultima_visita, type='char', size=64, method=True),
        'pruebas': fields.function(get_fecha_ultima_visita, type='char', size=64,  method=True),
        #'pruebas': fields.char('Pruebas', size=64),
    } 
    _defaults = {
        #'ultima_visita': lambda *a: time.strftime('%d-%m-%Y'),
        #'pruebas': get_fecha_ultima_visita(),
    }
    
res_partner()
