# -*- coding: utf-8 -*-

from osv import osv, fields
import pdb

class maquipal_envio(osv.osv_memory):
    """ Envio de nota a otro usuario """
    _name = 'maquipal.envio'
    _description = 'Envio de nota a otro usuario'
    _columns = {
        'usuario_destino': fields.many2one('res.users', 'Enviar a', required=True),
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

        vals = {
            'owner': envio[0].usuario_destino.id
        }

        nota.write(vals, context=context)
        message = "La nota ha sido enviada a '%s'" % envio[0].usuario_destino.name
        self.log(cr, uid, nota.id, message)


        # return {
        #     'view_type': 'form',
        #     'view_mode': 'form,tree',
        #     'view_id': board_view_form,
        #     'domain': '[]',
        #     'type': 'ir.actions.act_window',
        # }


        return {'type': 'ir.actions.act_window_close'}


maquipal_envio()