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
        record_id = context and context.get('active_id') or False
        if not record_id:
            return {'type': 'ir.actions.act_window_close'}

        #obtenemos las vistas del destino
        # models_data = self.pool.get('ir.model.data')
        # board_view_form = models_data._get_id(
        #     cr, uid, 'maquipal', 'board_maquipal_form')
        # if board_view_form:
        #     board_view_form = models_data.browse(
        #         cr, uid, board_view_form, context=context).res_id

        #modificamos la nota
        notas = self.pool.get('maquipal.nota')
        nota = notas.browse(cr, uid, record_id, context=context)

        envio = self.browse(cr, uid, ids, context=context)
        #pdb.set_trace()
        #envio[0].nota_id = nota.id
        #envio[0].write({'nota_id': nota.id}, context=context)
        #self.write(cr, uid, ids, {'nota_id': nota.id}, context=context)
        # self.nota_id = nota.id
        vals = {
            'owner': envio[0].usuario_destino.id,
            'estado': 'no_comenzado',
        }

        #pdb.set_trace()
        nota.write(vals, context=context)
        #nota.write(cr, uid, vals)
        message = "La nota ha sido enviada a '%s'" % envio[0].usuario_destino.name
        self.log(cr, uid, nota.id, message)

        vals2 = {
            'nota_id': nota.id,
        }
        envio[0].write(vals2, context = context)


        # return {
        #     'view_type': 'form',
        #     'view_mode': 'form,tree',
        #     'view_id': board_view_form,
        #     'domain': '[]',
        #     'type': 'ir.actions.act_window',
        # }


        return {'type': 'ir.actions.act_window_close'}


maquipal_envio()