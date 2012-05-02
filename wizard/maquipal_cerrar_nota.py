# -*- coding: utf-8 -*-

from osv import osv, fields
from .. import maquipal_nota
import time
import pdb

class maquipal_cerrar_nota(osv.osv_memory):
	""" Para cerrar una nota """

	def _get_default_resultado(self, cr, uid, ids, context=None):
		""" Obtiene el resultado """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.resultado

	def _get_default_perdido_motivo(self, cr, uid, ids, context=None):
		""" Obtiene perdido_motivo """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.perdido_motivo

	def _get_default_perdido_explicacion(self, cr, uid, ids, context=None):
		""" Obtiene perdido_explicacion """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.perdido_explicacion

	def _get_default_vendido_llegada(self, cr, uid, ids, context=None):
		""" Obtiene vendido_llegada """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_llegada

	def _get_default_vendido_entrega(self, cr, uid, ids, context=None):
		""" Obtiene vendido_entrega """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_entrega

	def _get_default_vendido_transportista(self, cr, uid, ids, context=None):
		""" Obtiene vendido_transportista """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_transportista

	def _get_default_vendido_portes(self, cr, uid, ids, context=None):
		""" Obtiene vendido_portes """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_portes

	def _get_default_vendido_proveedor(self, cr, uid, ids, context=None):
		""" Obtiene vendido_proveedor """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_proveedor

	def _get_default_vendido_cobrar_portes(self, cr, uid, ids, context=None):
		""" Obtiene vendido_cobrar_portes """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_cobrar_portes

	def _get_default_vendido_explicacion(self, cr, uid, ids, context=None):
		""" Obtiene vendido_explicacion """
		notas = self.pool.get('maquipal.nota')
		lanota = notas.browse(cr, uid, ids['active_id'], context=context)

		return lanota.vendido_explicacion

	_name = 'maquipal.cerrar.nota'
	_descrption = 'Wizard para cerrar una nota'
	_columns = {
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
		'resultado': _get_default_resultado,
		'perdido_motivo': _get_default_perdido_motivo,
		'perdido_explicacion': _get_default_perdido_explicacion,
		'vendido_llegada': _get_default_vendido_llegada,
		'vendido_entrega': _get_default_vendido_entrega,
		'vendido_transportista': _get_default_vendido_transportista,
		'vendido_portes': _get_default_vendido_portes,
		'vendido_proveedor': _get_default_vendido_proveedor,
		'vendido_cobrar_portes': _get_default_vendido_cobrar_portes,
		'vendido_explicacion': _get_default_vendido_explicacion,
	}

	def action_cancel(self, cr, uid, ids, context=None):
		"""
		Cierra cerrar nota
		@param self: The object pointer
		@param cr: the current row, from the database cursor
		@param uid: the current user's ID for security checks
		@param ids: list of notas ids
		@param context: a standard dictionary for contextual values
		"""
		return {'type': 'ir.actions.act_window_close'}

	def action_maquipal_cerrar_nota(self, cr, uid, ids, context=None):
		""" Guarda los cambios que se hubieran hecho en el resultado
			y cambia el estado y la fecha final
		"""
		record_id = context and context.get('active_id') or False
		if not record_id:
			return {'type': 'ir.actions.act_window_close'}

		notas = self.pool.get('maquipal.nota')
		nota = notas.browse(cr, uid, record_id, context=context)

		this = self.browse(cr, uid, ids, context)
		fecha_final = time.strftime('%Y-%m-%d %H:%M:%S')

		vals = {
			'resultado': this[0].resultado,
			'perdido_motivo': this[0].perdido_motivo,
			'perdido_explicacion': this[0].perdido_explicacion,
			'vendido_llegada': this[0].vendido_llegada,
			'vendido_entrega': this[0].vendido_entrega,
			'vendido_transportista': this[0].vendido_transportista,
			'vendido_portes': this[0].vendido_portes,
			'vendido_proveedor': this[0].vendido_proveedor,
			'vendido_cobrar_portes': this[0].vendido_cobrar_portes,
			'vendido_explicacion': this[0].vendido_explicacion,
			'fecha_final': fecha_final,
			'estado': 'cerrado',
		}
		nota.write(vals, context=context)

		#pdb.set_trace()
		return {'type': 'ir.actions.act_window_close'}

maquipal_cerrar_nota()
