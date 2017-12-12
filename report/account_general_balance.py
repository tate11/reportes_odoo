# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
from functools import reduce

"""
ACTIVOS_CIRCULANTE_IDS
select id, name from account_account where name in ('BANCOS','FONDO DE CAJA CHICA','CLIENTES','IMPUESTOS ACREDITABLES PAGADOS'
,'IMPUESTOS ACREDITABLES POR','PAGAR','DEUDORES DIVERSOS','INVENTARIOS','IMPUESTOS A FAVOR','PAGOS PROVISIONALES DE ISR');

id  |              name              
-----+--------------------------------
 111 | INVENTARIOS
  33 | BANCOS
   3 | CLIENTES
   9 | IMPUESTOS ACREDITABLES PAGADOS
  10 | DEUDORES DIVERSOS
   6 | FONDO DE CAJA CHICA
  15 | PAGOS PROVISIONALES DE ISR
  12 | INVENTARIOS
  14 | IMPUESTOS A FAVOR

ACTIVOS_NO_CIRCULANTE_IDS
select id, name from account_account where name in ('EQUIPO DE INSTALACION', 'DEPN. ACUM. DE EQUIPO DE INSTALACION'
, 'MOBILIARIO Y EQUIPO DE OFICINA', 'DEPN. ACUM. DE MOB. Y EQUIPO DE OFICINA', 'EQUIPO DE TRANSPORTE', 'DEPN. ACUM. EQUIPO DE TRANSPORTE'
, 'EQUIPO DE COMPUTO', 'DEPN. ACUM. EQUIPO DE COMPUTO', 'GASTOS DE INSTALACION Y ADAPTACION', 'AMORT. DE GTOS. DE INST. Y ADAPTACION');
 id  |                  name                   
-----+-----------------------------------------
 196 | DEPN. ACUM. EQUIPO DE TRANSPORTE
 195 | EQUIPO DE TRANSPORTE
  20 | EQUIPO DE TRANSPORTE
  18 | MOBILIARIO Y EQUIPO DE OFICINA
 192 | DEPN. ACUM. DE EQUIPO DE INSTALACION
  22 | EQUIPO DE COMPUTO
  23 | DEPN. ACUM. EQUIPO DE COMPUTO
  19 | DEPN. ACUM. DE MOB. Y EQUIPO DE OFICINA
  21 | DEPN. ACUM. EQUIPO DE TRANSPORTE
 200 | GASTOS DE INSTALACION Y ADAPTACION
 194 | DEPN. ACUM. DE MOB. Y EQUIPO DE OFICINA
 193 | MOBILIARIO Y EQUIPO DE OFICINA
 191 | EQUIPO DE INSTALACION
 197 | EQUIPO DE COMPUTO
  26 | AMORT. DE GTOS. DE INST. Y ADAPTACION
  25 | GASTOS DE INSTALACION Y ADAPTACION
  16 | EQUIPO DE INSTALACION
  17 | DEPN. ACUM. DE EQUIPO DE INSTALACION
 467 | EQUIPO DE TRANSPORTE
 469 | EQUIPO DE COMPUTO
 470 | EQUIPO DE INSTALACION
 468 | EQUIPO DE COMPUTO

ACTIVOS_DIFERIDO
select id, name from account_account where name in ('DEPOSITOS EN GARANTIA', 'PAGOS ANTICIPADOS', 'ANTICIPO A PROVEEDORES');
 id  |          name          
-----+------------------------
 199 | DEPOSITOS EN GARANTIA
  24 | DEPOSITOS EN GARANTIA
  13 | PAGOS ANTICIPADOS
   7 | ANTICIPO A PROVEEDORES

PASIVO_CORTO_PLAZO
 select id, name from account_account where name in ('OTRAS CUENTAS POR PAGAR', 'ACREEDORES DIVERSOS', 'SUELDOS Y COMISIONES POR PAGAR', 
 'IMPUESTOS Y DERECHOS POR PAGAR', 'IVA POR PAGAR', 'IVA POR PAGAR DIFERIDO', 'OTROS PASIVOS POR PAGAR', 'IMPUESTO SOBRE LA RENTA', 
 'DOCUMENTOS POR PAGAR', 'PROVEEDORES', 'IMPUESTOS RETENIDOS', 'PROVISION CONTRIB DE S SOCIAL X PAGAR', 'PTU');
 id  |                 name                  
-----+---------------------------------------
 236 | OTRAS CUENTAS POR PAGAR
  31 | SUELDOS Y COMISIONES POR PAGAR
  35 | IVA POR PAGAR
  27 | PROVEEDORES
  28 | OTRAS CUENTAS POR PAGAR
  29 | ACREEDORES DIVERSOS
  39 | PROVISION CONTRIB DE S SOCIAL X PAGAR
  42 | IMPUESTO SOBRE LA RENTA
 123 | IVA POR PAGAR
  38 | IMPUESTOS RETENIDOS
  40 | OTROS PASIVOS POR PAGAR
  43 | DOCUMENTOS POR PAGAR
  41 | PTU
 307 | SUELDOS Y COMISIONES POR PAGAR
 309 | IVA POR PAGAR
 122 | IVA POR PAGAR

CAPITAL
select id, name from account_account where name in ('CAPITAL SUSCRITO', 'RESERVA LEGAL', 'RESULTADO DE EJERCICIOS ANTERIORES', 'RESULTADO DEL EJERCICIO');
id  |                name                
-----+------------------------------------
  45 | CAPITAL SUSCRITO
  46 | RESERVA LEGAL
  48 | RESULTADO DE EJERCICIOS ANTERIORES
 333 | RESERVA LEGAL

"""
ACTIVOS_CIRCULANTE_IDS=[33, 3, 9, 10, 6, 15, 12, 14]
ACTIVOS_NO_CIRCULANTE_IDS=[20, 18, 19, 22, 23, 21,26, 25, 16, 17]
ACTIVOS_DIFERIDO=[24, 13, 7]
PASIVO_CORTO_PLAZO=[31, 35, 27, 37, 28, 29, 39, 42, 38, 40, 43, 41]
CAPITAL=[45, 46, 48]

class ReportGeneralBalanceEcosoft(models.AbstractModel):
    _name = 'report.account.report_generalbalance_ecosoft'

    def calc_total (self, lista):
        t=0
        for a in lista:
            t= t+a['balance']
        return t

    def calc_data (self, lista, period_data, context):
        results=[]
        if period_data:
            for a in lista:
                result={
                    'balance' : a.with_context(context).balance,
                    'name' : a.with_context(context).name
                }
                results.append(result)
        else:
            for a in lista:
                result={
                    'balance' : a.balance,
                    'name' : a.name                
                }
                results.append(result)
        return results        

    @api.model
    def render_html(self, wizard, data=None):
        context = self._context.copy()
        period_data = data['form'].get('period_id', False)
        choose_period = data['form'].get('choose_period', False)
        with_period = period_data and choose_period
        
        if with_period :
            context.update({'periods': [period_data[0]]})
        

        activo_circulante = self.env['account.account'].browse(ACTIVOS_CIRCULANTE_IDS)
        activo_circulante=self.calc_data(activo_circulante, period_data, context)
        t_activo_circulante=self.calc_total(activo_circulante) 
                       
        #t_activo_circulante = reduce ((lambda x,y: x + y), activo_circulante)
        #print 'total:' + str(t_activo_circulante)
        activo_no_circulante = self.env['account.account'].browse(ACTIVOS_NO_CIRCULANTE_IDS)
        activo_no_circulante=self.calc_data(activo_no_circulante, period_data, context)
        t_activo_no_circulante=self.calc_total(activo_no_circulante)
        
        activo_diferido = self.env['account.account'].browse(ACTIVOS_DIFERIDO)
        activo_diferido=self.calc_data(activo_diferido, period_data, context)
        t_activo_diferido=self.calc_total(activo_diferido)

        pasivo_corto_plazo = self.env['account.account'].browse(PASIVO_CORTO_PLAZO)
        pasivo_corto_plazo=self.calc_data(pasivo_corto_plazo, period_data, context)
        t_pasivo_corto_plazo=self.calc_total(pasivo_corto_plazo)

        capital = self.env['account.account'].browse(CAPITAL)
        capital=self.calc_data(capital, period_data, context)
        t_capital=self.calc_total(capital)
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        totales = {
            't_activo_circulante':t_activo_circulante, 
            't_activo_no_circulante':t_activo_no_circulante,
            't_activo_diferido': t_activo_diferido,
            't_pasivo_corto_plazo': t_pasivo_corto_plazo,
            't_capital': t_capital,
            't_activo': t_activo_circulante + t_activo_no_circulante + t_activo_diferido,
            't_pasivo_capital': t_pasivo_corto_plazo + t_capital
            }
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'activo_circulante': activo_circulante,
            'activo_no_circulante': activo_no_circulante,
            'activo_diferido': activo_diferido,
            'pasivo_corto_plazo': pasivo_corto_plazo,
            'capital': capital, 
            'totales': totales,
            'periodo': with_period and period_data[1]           
        }
        return self.env['report'].render('account_trial_balance_ecosoft.report_generalbalance_ecosoft', docargs)