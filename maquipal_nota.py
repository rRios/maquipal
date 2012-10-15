# -*- coding: utf-8 -*-

from osv import fields, osv
from datetime import datetime
import time
import pdb
import random

AVAILABLE_STATES = [
    ('no_comenzado', 'No Comenzado'),
    ('urgente', 'Urgente'),
    ('pte_proveedor', 'Pte. Proveedor'),
    ('llamar', 'Llamar'),
    ('en_curso', 'En Curso'),
    ('pte_cliente', 'Pte. Cliente'),
    ('pte_stock', 'Pte. Stock'),
    ('ofertado', 'Ofertado'),
    ('retrasado', 'Retrasado'),
    ('incompleto', 'Incompleto'),
    ('avisado', 'Avisado'),
    ('recogen', 'Recogen'),
    ('recepcionado', 'Recepcionado'),
    ('cerrado', 'Cerrado'),
]

AVAILABLE_STATES_SELECCION = [
    ('no_comenzado', 'No Comenzado'),
    ('urgente', 'Urgente'),
    ('pte_proveedor', 'Pte. Proveedor'),
    ('llamar', 'Llamar'),
    ('en_curso', 'En Curso'),
    ('pte_cliente', 'Pte. Cliente'),
    ('pte_stock', 'Pte. Stock'),
    ('ofertado', 'Ofertado'),
    ('retrasado', 'Retrasado'),
    ('incompleto', 'Incompleto'),
    ('avisado', 'Avisado'),
    ('recogen', 'Recogen'),
    ('recepcionado', 'Recepcionado'),
]

class maquipal_nota(osv.osv):
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        """This function returns value of partner address based on partner
        @param self: The object pointer
        @param cr: the current row, from the database cursor
        @param uid: the current user's ID for security checks
        @param ids: List of case IDs
        @param part: Partner's id
        @email: Partner's email ID
        """
        if not part:
            return {'value': {'partner_address_id': False,
                            'email_from': False,
                            'phone': False
                            }}
        addr = self.pool.get('res.partner').address_get(cr, uid, [part], ['contact'])
        #addr = self.pool.get('res.partner').address_get(cr, uid, [part])

        data = self.onchange_partner_address_id(cr, uid, ids, addr['contact'])['value']
        #data = self.onchange_partner_address_id(cr, uid, ids, addr)['value']

        #
        #cliente = self.pool.get('res.partner').browse(cr, uid, part)
        # data['aviso'] = cliente.aviso
        #pdb.set_trace()
        # if cliente.aviso:
        #     raise osv.except_osv(('AVISO'),(cliente.aviso))

        return {'value': data}

    def onchange_partner_address_id(self, cr, uid, ids, add, email=False):
        """This function returns value of partner email based on Partner Address
        @param self: the object pointer
        @param cr: the current row, from the database cursor
        @param uid: the current user's ID for security checks
        @param ids: list of case IDs
        @param add Id of Partner's address
        @email: Partner's email ID
        """
        if not add:
            return {'value': {'email_from': False}}
        address = self.pool.get('res.partner.address').browse(cr, uid, add)

        #pdb.set_trace()
        #return {'value': {'email_from': address.email, 'phone': address.phone, 'contacto': address.name}}
        return {'value': {'phone': address.phone, 'contacto': address.name, 'mobile': address.mobile, 'aviso': address.partner_id.aviso}}

    def onchange_maquina_id(self, cr, uid, ids, maq):
        """This function returns value of modelo and serie based on maquina id
        @param self: the object pointer
        @param cr: the current row, from the database cursor
        @param uid: the current user's ID for security checks
        @param ids: list of case IDs
        @param maq Id of maquina
        """
        if not maq:
            return {'value': {}}
        maquina = self.pool.get('product.product').browse(cr, uid, maq)
        return {'value': {'modelo': maquina.modelo, 'serie': maquina.serie}}


    def _get_default_user(self, cr, uid, context=None):
        """Gives current user id
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        """
        if context and context.get('portal', False):
            return False

        return uid


    def copiar_estado_visto(self, cr, uid, ids, est_visto, context=None):
        """Copia el estado_visto en estado. estado_visto sirve para ocultar el estado cerrado del desplegable
        @param self: the object pointer
        @param cr: the current row, from the database cursor
        @param uid: the current user's ID for security checks
        @param ids: list of case IDs
        @param est_visto: estado_visto (igual que estado, pero sin cerrado)
        """
        if not est_visto:
            return {'value': {}}

        # cliente = self.pool.get('res.partner').browse(cr, uid, part)
        # if cliente.aviso:
        #     raise osv.except_osv(('AVISO'),(cliente.aviso))

        return {'value': {'estado': est_visto}}

    def copiar_estado(self, cr, uid, ids, est, context=None):
        """Copia el estado en estado_visto. por si se vuelve de cerrado
        @param self: the object pointer
        @param cr: the current row, from the database cursor
        @param uid: the current user's ID for security checks
        @param ids: list of case IDs
        @param est: estado
        """
        if not est:
            return {'value': {}}

        # cliente = self.pool.get('res.partner').browse(cr, uid, part)
        # if cliente.aviso:
        #     raise osv.except_osv(('AVISO'),(cliente.aviso))

        return {'value': {'estado_visto': est}}

    # def onchange_datos(self, cr, uid, ids, datos, context=None):
    #     if context is None:
    #         context = {}
    #     context.update({'active_ids': ids})
    #     notas = self.browse(cr, uid, ids)
    #     for nota in notas:
    #         if nota.cliente_id.aviso:
    #             return {'value':{}, 'warning': nota.cliente_id.aviso}
                



    # def write(self, cr, uid, ids, vals, context=None):
    #     if context is None:
    #         context = {}
    #     context.update({'active_ids': ids})
    #     notas = self.browse(cr, uid, ids)
    #     for nota in notas:
    #         if nota.cliente_id.aviso:
    #             raise osv.except_osv(('AVISO'),(nota.cliente_id.aviso))
    #             res = super(nota, self).write(cr, uid, ids, vals, context)
    #         else:
    #             res = super(osv.osv, self).write(cr, uid, ids, vals, context=context)
    #     return res




    _name = 'maquipal.nota'
    _description = 'Nota'
    _rec_name = 'fecha_inicio'
    _columns = {
        'cliente_id': fields.many2one('res.partner', 'Cliente', select=True),
        'phone': fields.char('Telefono', size=64),
        'mobile': fields.char('Movil', size=64),
        'contacto': fields.char('Contacto', size=64),
        'maquina': fields.many2one('product.product', 'Maquina', select=True),
        'modelo': fields.char('Modelo', size=64, select=True),
        'serie': fields.char('Serie', size=64, select=True),
        # 'modelo': fields.many2one('product.product', 'Modelo', select=True),
        # 'serie': fields.many2one('product.product', 'Serie', select=True),
        'fecha_inicio': fields.date('Fecha inicio', readonly=True, select=True),
        'fecha_final': fields.date('Fecha final', readonly=True),
        #'fecha_contestacion': fields.date('Fecha contestacion'),
        'tema': fields.char('Tema', size=64, select=True),
        'datos': fields.text('Datos'),
        'tipo': fields.selection([('pedido', 'Pedido'), ('consulta', 'Consulta')], 'Tipo', select=True),
        'comentarios': fields.text('Comentarios'),
        'owner': fields.many2one('res.users', 'Destinatario', readonly=True),
        'estado': fields.selection(AVAILABLE_STATES, 'Estado', select=True),
        'estado_visto': fields.selection(AVAILABLE_STATES_SELECCION, 'Estado'),
        'historico': fields.one2many('maquipal.envio', 'nota_id', 'Historico'),
        'resultado': fields.selection([
                    ('vendido', 'Vendido'),
                    ('perdido', 'Perdido')], 'Resultado', select=True),
        'perdido_motivo': fields.selection([
                    ('precio', 'Precio'),
                    ('retraso', 'Retraso'),
                    ('plazo_entrega', 'Plazo de entrega'),
                    ('afinidad', 'Afinidad'),
                    ('marca_calidad', 'Marca - Calidad'),
                    ('mal_servicio', 'Mal servicio')], 'Motivo de la perdida'),
        'perdido_explicacion': fields.text('Comentarios'),
        'vendido_llegada': fields.date('Dia de llegada'),
        'vendido_entrega': fields.date('Dia de entrega'),
        'vendido_transportista': fields.char('Transportista', size=64),
        'vendido_portes': fields.selection([
                    ('pagados', 'Pagados'),
                    ('debidos', 'Debidos')], 'Portes'),
        'vendido_proveedor': fields.char('Proveedor', size=64),
        'vendido_cobrar_portes': fields.char('Cobrar portes', size=64),
        'vendido_explicacion': fields.text('Comentarios'),
        'aviso': fields.char('Aviso', size=140),
    }
    _defaults = {
        #'fecha_inicio': lambda *a: time.strftime("%d/%m/%Y"),
        'fecha_inicio': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'estado': 'no_comenzado',
        'estado_visto': 'no_comenzado',
        'owner': _get_default_user,
    }

    def establecer_fecha(self, cr, uid, ids, context=None):
        """
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        """

        value = {}
        data = context and context.get('active_ids', []) or []

        meeting_obj = self.pool.get('crm.meeting')
        nota_obj = self.pool.get('maquipal.nota')
        data_obj = self.pool.get('ir.model.data')
        
        #select the view
        #id2 = data_obj._get_id(cr, uid, 'maquipal', 'crm_case_form_view_meet')
        id2 = data_obj._get_id(cr, uid, 'maquipal', 'maquipal_anotacion')
        id3 = data_obj._get_id(cr, uid, 'maquipal', 'view_calendario_inherit_tree')    
        if id2:
            id2 = data_obj.browse(cr, uid, id2, context=context).res_id
        if id3:
            id3 = data_obj.browse(cr, uid, id3, context=context).res_id 

        #pdb.set_trace()

        for this in self.browse(cr, uid, ids, context=context):
            #pdb.set_trace()
            new_meeting = meeting_obj.create(cr, uid, {
                    #'name': this.tema,
                    'name': this.id,
                    'cliente': this.cliente_id.name,
                    'partner_id': this.cliente_id.id,
                    'partner_address_id': this.cliente_id.address[0].id,
                    'email_from': this.cliente_id.address[0].email,
                    'contacto': this.contacto,
                    'phone': this.phone,
                    'mobile': this.mobile,
                    'nota': this.tema,
                    'fecha_inicio': this.fecha_inicio,
                    'datos': this.datos,

            }, context=context)

            value = {
                'name': 'Nueva Fecha',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.meeting',
                'res_id' : new_meeting,
                'views': [(id2, 'form'), (id3, 'tree')],
                'target': 'current',
                'type': 'ir.actions.act_window',
            }

        return value


    def enviar_a(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        context.update({'active_ids': ids})

        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'maquipal', 'view_maquipal_envio')
        value = {}

        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id

        #pdb.set_trace()

        value = {
                'name': 'Enviar a',
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'maquipal.envio',
                'view_id': False,
                #'view_id': 'view_nota_form2',
                'context': context,
                'views': [(view_id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'nodestroy': True
        }

        return value


    def cerrar_nota(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        context.update({'active_ids': ids})


        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'maquipal', 'view_maquipal_cerrar_nota')
        value = {}

        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id

        #pdb.set_trace()

        value = {
                'name': 'Cerrar Nota',
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'maquipal.cerrar.nota',
                'view_id': False,
                #'view_id': 'view_nota_form2',
                'context': context,
                'views': [(view_id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'nodestroy': True
        }


        return value

maquipal_nota()
