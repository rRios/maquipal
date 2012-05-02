# -*- coding: utf-8 -*-

from osv import fields, osv
from datetime import datetime
import time
import pdb

AVAILABLE_STATES = [
    ('no_comenzado', 'No Comenzado'),
    ('urgente', 'Urgente'),
    ('pte_proveedor', 'Pte. Proveedor'),
    ('llamar', 'Llamar'),
    ('en_curso', 'En Curso'),
    ('pte_cliente', 'Pte. Cliente'),
    ('ofertado', 'Ofertado'),
    ('retrasado', 'Retrasado'),
    ('entregado', 'Entregado'),
    ('avisado', 'Avisado'),
    ('recogen', 'Recogen'),
    ('recepcionado', 'Recepcionado'),
    ('cerrado', 'Cerrado'),
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
        return {'value': {'phone': address.phone, 'contacto': address.name}}

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

    _name = 'maquipal.nota'
    _description = 'Nota'
    _rec_name = 'fecha_inicio'
    _columns = {
        'cliente_id': fields.many2one('res.partner', 'Cliente', select=True),
        'phone': fields.char('Telefono', size=64),
        'contacto': fields.char('Contacto', size=64),
        'maquina': fields.many2one('product.product', 'Maquina', select=True),
        'modelo': fields.char('Modelo', size=64, select=True),
        'serie': fields.char('Serie', size=64, select=True),
        'fecha_inicio': fields.date('Fecha inicio', readonly=True, select=True),
        'fecha_final': fields.date('Fecha final', readonly=True),
        'fecha_contestacion': fields.date('Fecha contestacion'),
        'tema': fields.char('Tema', size=64, select=True),
        'datos': fields.text('Datos'),
        'tipo': fields.selection([('pedido', 'Pedido'), ('consulta', 'Consulta')], 'Tipo', select=True),
        'avisos': fields.text('Avisos'),
        'owner': fields.many2one('res.users', 'Destinatario', readonly=True),
        'estado': fields.selection(AVAILABLE_STATES, 'Estado', select=True),
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
    }
    _defaults = {
        #'fecha_inicio': lambda *a: time.strftime("%d/%m/%Y"),
        'fecha_inicio': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'estado': 'no_comenzado',
        'owner': _get_default_user,
    }

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

    # def action_no_comenzado(self, cr, uid, ids, context=None):
    #     """Pasa a no comenzado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'no_comenzado'})
    #     return True

    # def action_pte_proveedor(self, cr, uid, ids, context=None):
    #     """Pasa a pte proveedor
    #     """
    #     self.write(cr, uid, ids, {'estado': 'pte_proveedor'})
    #     return True

    # def action_llamar(self, cr, uid, ids, context=None):
    #     """Pasa a llamar
    #     """
    #     self.write(cr, uid, ids, {'estado': 'llamar'})
    #     return True

    # def action_en_curso(self, cr, uid, ids, context=None):
    #     """Pasa a en curso
    #     """
    #     self.write(cr, uid, ids, {'estado': 'en_curso'})
    #     return True

    # def action_pte_cliente(self, cr, uid, ids, context=None):
    #     """Pasa a pte cliente
    #     """
    #     self.write(cr, uid, ids, {'estado': 'pte_cliente'})
    #     return True

    # def action_ofertado(self, cr, uid, ids, context=None):
    #     """Pasa a ofertado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'ofertado'})
    #     return True

    # def action_retrasado(self, cr, uid, ids, context=None):
    #     """Pasa a retrasado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'retrasado'})
    #     return True

    # def action_terminado(self, cr, uid, ids, context=None):
    #     """Pasa a terminado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'terminado'})
    #     return True

    # def action_entregado(self, cr, uid, ids, context=None):
    #     """Pasa a entregado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'entregado'})
    #     return True

    # def action_avisado(self, cr, uid, ids, context=None):
    #     """Pasa a avisado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'avisado'})
    #     return True

    # def action_recogen(self, cr, uid, ids, context=None):
    #     """Pasa a recogen
    #     """
    #     self.write(cr, uid, ids, {'estado': 'recogen'})
    #     return True

    # def action_recepcionado(self, cr, uid, ids, context=None):
    #     """Pasa a recepcionado
    #     """
    #     self.write(cr, uid, ids, {'estado': 'recepcionado'})
    #     return True

    # def action_urgente(self, cr, uid, ids, context=None):
    #     """Pasa a urgente
    #     """
    #     self.write(cr, uid, ids, {'estado': 'urgente'})
    #     return True

    # def action_inicio(self, cr, uid, ids, context=None):
    #     """Pasa al estado inicial
    #     """
    #     #pdb.set_trace()
    #     self.write(cr, uid, ids, {'state': 'inicio'})
    #     return True

    # def action_final(self, cr, uid, ids, context=None):
    #     """Pasa al estado final
    #     """
    #     self.write(cr, uid, ids, {'state': 'final'})
    #     return True

maquipal_nota()
