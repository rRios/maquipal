# -*- coding: utf-8 -*-

import time

from report import report_sxw

class maquipal_cliente_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context=None):
		super(maquipal_cliente_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
			'time': time,
		})

report_sxw.report_sxw('report.maquipal.cliente', 'maquipal.cliente', 'addons/maquipal/report/maquipal_cliente_report.rml', parser=maquipal_cliente_report, header="external")