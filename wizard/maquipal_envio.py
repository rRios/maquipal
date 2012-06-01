# -*- coding: utf-8 -*-

from osv import osv, fields
import time
import pdb

class maquipal_envio(osv.osv_memory):
    """ Envio de nota a otro usuario """

    _name = 'maquipal.envio'
    _description = 'Envio de nota a otro usuario'
    _columns = {
        'usuario_origen': fields.many2one('res.users', 'Origen', readonly=True),
        'usuario_destino': fields.many2one('res.users', 'Enviar a', required=True),
        'comentario': fields.text('Comentario'),
        'nota_id': fields.many2one('maquipal.nota', 'Nota'),
        'fecha_envio': fields.date('Fecha envio', readonly=True, select=True),
        'urgente': fields.boolean('Urgente'),
    }

    _rec_name = 'usuario_destino'

    # def _get_nota_id(self, cr, uid, ids, context=None):
    #     """
    #     Saca el id de la nota a enviar
    #     @param self: The object pointer
    #     @param cr: the current row, from the database cursor,
    #     @param uid: the current user’s ID for security checks,
    #     @param ids: List of Lead to Partner's IDs
    #     @param context: A standard dictionary for contextual values
    #     """
    #     #record_id = context and context.get('active_id') or False
    #     record_id = ids['active_id']
    #     #pdb.set_trace()
    #     if not record_id:
    #         return {'type': 'ir.actions.act_window_close'}
    #     return record_id

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


    _defaults = {
        'usuario_origen': _get_default_user,
        'fecha_envio': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }


    def action_cancel(self, cr, uid, ids, context=None):
        """
        Closes Lead To Opportunity form
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Lead to Partner's IDs
        @param context: A standard dictionary for contextual values

        """
        return {'type': 'ir.actions.act_window_close'}


    def action_maquipal_envio(self, cr, uid, ids, context=None):
        """ Cambia el owner de la nota y regresa al board
        """
        record_id = context and context.get('active_ids') or False
        if not record_id:
            return {'type': 'ir.actions.act_window_close'}


        notas = self.pool.get('maquipal.nota')
        nota = notas.browse(cr, uid, record_id, context=context)

        envio = self.browse(cr, uid, ids, context=context)

        elestado = 'no_comenzado'
        if envio[0].urgente:
            elestado = 'urgente'

        vals = {
            'owner': envio[0].usuario_destino.id,
            'estado': elestado,
            'estado_visto': elestado,
        }

        nota[0].write(vals, context=context)

        message = "La nota ha sido enviada a '%s'" % envio[0].usuario_destino.name
        self.log(cr, uid, nota[0].id, message)

        vals2 = {
            'nota_id': nota[0].id,
        }
        envio[0].write(vals2, context = context)


        return {'type': 'ir.actions.act_window_close'}


maquipal_envio()