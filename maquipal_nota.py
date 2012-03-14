# -*- coding: utf-8 -*-

from osv import fields, osv
import pdb

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
        #data = {'partner_address_id': addr['contact']}
        #data.update(self.onchange_partner_address_id(cr, uid, ids, addr['contact'])['value'])
        data = self.onchange_partner_address_id(cr, uid, ids, addr['contact'])['value']
        #data.update(self.onchange_partner_address_id(cr, uid, ids, addr['contact'])['value'])
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

    _name = 'maquipal.nota'
    _description = 'Nota'
    _columns = {
        'cliente_id': fields.many2one('res.partner', 'Cliente'),
        'phone': fields.char('Telefono', size=64),
        'contacto': fields.char('Contacto', size=64),
        'maquina': fields.many2one('product.product', 'Maquina'),
        'modelo': fields.char('Modelo', size=64),
        'serie': fields.char('Serie', size=64),
        'tema': fields.char('Tema', size=64),
    }
    _defaults = {
        #'telefono': _get_default_telefono,
    }

maquipal_nota()
