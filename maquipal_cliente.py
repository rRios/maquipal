# -*- coding: utf-8 -*-

from osv import fields, osv
import time
import pdb
import crm

class res_partner(osv.osv):
    # def get_fecha_ultima_visita(self, cr, uid, ids, field_name, arg, context):
    #     res = {}
        
    #     for id in ids:
    #         comentarios = self.pool.get('maquipal.comentarios.visita').search(cr, uid, [('partner_id', '=', id)])
    #         if len(comentarios)>0:
    #             ultimo = self.pool.get('maquipal.comentarios.visita').browse(cr, uid, comentarios[-1])
    #             campo =  ultimo.fecha_creacion
    #             c = time.strptime(campo,"%Y-%m-%d")
    #             res[id] = time.strftime("%d/%m/%Y",c)

    #     return res

    # def get_fecha_ultima_visita2(self, cr, uid, ids, field_name, arg, context):
    #     res = {}
    #     for id in ids:
    #         comentarios = self.pool.get('crm.meeting').search(cr, uid, [('partner_id', '=', id)])
    #         if len(comentarios)>0:
    #             ultimo
    
    _name = 'res.partner'
    _description = 'Cliente'
    _inherit = 'res.partner'
    _columns = {
        'actividad': fields.char('Actividad', size=64),
        'riesgo': fields.char('Riesgo', size=64),
        'address': fields.one2many('res.partner.address', 'partner_id', 'Contacts'),
        'calle': fields.related('address', 'street', type='char', string='Calle'),
        'elcontacto': fields.related('address', 'name', type='char', string='Contacto'),
        #'comentarios': fields.one2many('maquipal.comentarios.visita','partner_id','Comentarios'),
        'maquinas': fields.one2many('product.product', 'cliente_id', 'Maquinas'),
        'visitas': fields.one2many('crm.meeting', 'partner_id', 'Visitas'),
        'aviso': fields.char('Aviso', size=140),
        'notas': fields.one2many('maquipal.nota', 'cliente_id', 'Notas Asociadas'),
    } 
    _defaults = {

    }


    def crear_nota_desde_cliente(self, cr, uid, ids, context=None):
        """
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        """

        value = {}
        data = context and context.get('active_ids', []) or []
        nota_obj = self.pool.get('maquipal.nota')
        cliente_obj = self.pool.get('res.partner')

        data_obj = self.pool.get('ir.model.data')
        
        #select the view
        id2 = data_obj._get_id(cr, uid, 'maquipal', 'view_nota_form')
        id3 = data_obj._get_id(cr, uid, 'maquipal', 'view_nota_tree')    
        if id2:
            id2 = data_obj.browse(cr, uid, id2, context=context).res_id
        if id3:
            id3 = data_obj.browse(cr, uid, id3, context=context).res_id 

        #pdb.set_trace()

        for this in self.browse(cr, uid, ids, context=context):
            #pdb.set_trace()
            if this.riesgo == False:
                campo_riesgo = ''
            else:
                campo_riesgo = this.riesgo
            if this.comment == False:
                campo_comment = ''
            else:
                campo_comment = this.comment

            campo_comentarios = 'Riesgo: '+campo_riesgo+'\n\n'+campo_comment

            new_nota = nota_obj.create(cr, uid, {
                    'cliente_id': this.id,
                    'phone': this.phone,
                    'mobile': this.mobile,
                    'contacto': this.address[0].name,
                    'comentarios': campo_comentarios,
                    'aviso': this.aviso,
            }, context=context)


            # #############################################
            # warning = {}
            # cliente = self.pool.get('res.partner').browse(cr, uid, this.id)
            # if cliente.aviso:
            #     title = "Aviso"
            #     message = cliente.aviso
            #     warning = {
            #         'title': title,
            #         'message': message,
            #     }
            # result = super(res_partner,self).crear_nota_desde_cliente(cr, uid, ids, context) 
            # if result.get('warning',False):
            #     warning['title'] = title and title +' & '+ result['warning']['title'] or result['warning']['title']
            #     warning['message'] = message and message + ' ' + result['warning']['message'] or result['warning']['message']
            # #############################################

            value = {
                'name': 'Nueva Nota',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'maquipal.nota',
                'res_id' : new_nota,
                'views': [(id2, 'form'), (id3, 'tree'), (False, 'calendar')],
                'target': 'current',
                'type': 'ir.actions.act_window',
            }

        return value
        #return {'warning':{'title':'warning','message':'Negative margin on this line'}}


res_partner()


# class maquipal_comentarios_visita(osv.osv):
#     _name = 'maquipal.comentarios.visita'
#     _description = "Comentarios de la visita"
#     _columns = {
#         'fecha_creacion': fields.date('Fecha', readonly=True, select=True),
#         'texto': fields.text('Comentarios'),
#         'partner_id': fields.many2one('res.partner', 'Cliente', readonly=True),
#     }
#     _defaults = {
#         'fecha_creacion': lambda *a: time.strftime("%d/%m/%Y"),
#     }

# maquipal_comentarios_visita()



class maquipal_calendario(osv.osv):
    _name = "crm.meeting"
    _description = "calendario"
    _inherit = "crm.meeting"
    _columns = {
        #'ultima_visita': fields.function(get_fecha_ultima_visita, type='char', size=64, method=True),
        #'proxima_visita': fields.function(get_fecha_ultima_visita, type='char', size=64, method=True),
        #'visitas': fields.one2many('crm.meeting', 'partner_id', 'Visitas'),
        #'tipo': fields.selection([('visita', 'Visita'), ('llamada', 'Llamada')], 'Tipo'),
        'cliente': fields.char('Cliente', size=64),
        'contacto': fields.char('Contacto', size=64),
        'phone': fields.char('Telefono', size=64),
        'mobile': fields.char('Movil', size=64),
        'nota': fields.char('Nota', size=64),
        'fecha_inicio': fields.date('Fecha inicio'),
        'datos': fields.text('Datos'),
        'estado': fields.selection([
                ('pendiente', 'Pendiente'),
                ('hecho', 'Hecho')], 'Estado', select=True),
        }
    _order = "date desc"
    _defaults = {
        'estado': 'pendiente',
    }

maquipal_calendario()

