# -*- coding: utf-8 -*-

from osv import fields, osv
import pdb

class product_product(osv.osv):
    _name = 'product.product'
    _description = 'Maquina'
    _inherit = 'product.product'
    _columns = {
        'marca': fields.char('Marca', size=64, select=True),
        'modelo': fields.char('Modelo', size=64, required=True, select=True),
        'serie': fields.char('Serie', size=64, required=True, select=True),
        'cliente_id': fields.many2one('res.partner', 'Cliente', required=True, select=True),
        'mod_motor': fields.char('Mod. Motor', size=64),
        'serie_motor': fields.char('Serie Motor', size=64),
        'mod_convertidor': fields.char('Mod. Convertidor', size=64),
        'serie_convertidor': fields.char('Serie Convertidor', size=64),
        'f_combustible': fields.char('F. Combustible', size=64),
        'f_aceite': fields.char('F. Aceite', size=64),
        'f_aire_ext': fields.char('F. Aire Ext', size=64),
        'f_aire_int': fields.char('F. Aire Int', size=64),
        'f_hidraulico': fields.char('F. Hidraulico', size=64),
        'f_convertidor': fields.char('F. Convertidor', size=64),
        't_dientes': fields.char('T. Dientes', size=64),
        'correa_alter': fields.char('Correa Alternador', size=64),
        'correa_venti': fields.char('Correa Ventilador', size=64),
        'alternador': fields.char('Alternador', size=64),
        'm_arranque': fields.char('M. Arranque', size=64),
        'ruedas': fields.char('Ruedas', size=64),
        'mastil': fields.char('Mastil', size=64),
        'bateria': fields.char('Bateria', size=64),
        'comentarios': fields.text('Comentarios'),
    }

    def crear_nota_desde_maquina(self, cr, uid, ids, context=None):
        """
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        """
        value = {}
        data = context and context.get('active_ids', []) or []
        nota_obj = self.pool.get('maquipal.nota')
        maquina_obj = self.pool.get('product.product')

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
            
            if this.cliente_id.riesgo == False:
                campo_riesgo = ''
            else:
                campo_riesgo = this.cliente_id.riesgo
            if this.cliente_id.comment == False:
                campo_comment = ''
            else:
                campo_comment = this.cliente_id.comment

            campo_avisos = 'Riesgo: '+campo_riesgo+'\n\n'+campo_comment
            
            new_nota = nota_obj.create(cr, uid, {
                    'cliente_id': this.cliente_id.id,
                    'phone': this.cliente_id.phone,
                    'mobile': this.cliente_id.mobile,
                    'contacto': this.cliente_id.address[0].name,
                    'avisos': campo_avisos,
                    'maquina': this.id,
                    'modelo': this.modelo,
                    'serie': this.serie,
            }, context=context)


            value = {
                'name': 'Nueva Nota',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'maquipal.nota',
                'res_id' : new_nota,
                'views': [(id2, 'form'), (id3, 'tree'), (False, 'calendar')],
                'target': 'current',
                'type': 'ir.actions.act_window',
            }

        return value

    # def default_get(self, cr, uid, fields, context=None):
    #     """
    #     This function gets default values
    #     @param self: The object pointer
    #     @param cr: the current row, from the database cursor
    #     @param uid: the current user's ID for security checks
    #     @param fields: List of fields for default value
    #     @param context: A standard dictionary for contextual values

    #     @return: default values of fields
    #     """
    #     maquina_obj = self.pool.get('product.product')
    #     data = context and context.get('active_ids', []) or []
    #     res = super(maquipal_nota_desde_maquina, self).default_get(cr, uid, fields, context=context)
    #     for maquina in maquina_obj.browse(cr, uid, data, context=context):
    #         if 'cliente_id' in fields:
    #             res.update({'cliente_id': maquina.cliente_id.name})
    #         if 'phone' in fields:
    #             res.update({'phone': maquina.cliente_id.phone})
    #         if 'contacto' in fields:
    #             res.update({'contacto': maquina.cliente_id.address[0].name})
    #         if 'maquina' in fields:
    #             res.update({'maquina': maquina.name})
    #         if 'modelo' in fields:
    #             res.update({'modelo': maquina.modelo})
    #         if 'serie' in fields:
    #             res.update({'serie': maquina.serie})
        
    #     return res

product_product()

