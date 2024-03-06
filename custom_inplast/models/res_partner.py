# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"


    # Campos de migración facilitados por el cliente, se pueden eliminar en un futuro para PROVEEDORES (de momento):
    mig_iban = fields.Char('mig_iban')
    mig_tipoproveedor = fields.Char('mig_tipoproveedor')
    mig_actividad = fields.Char('mig_actividad')
    mig_1cargo = fields.Char('mig_1cargo')
    mig_1nombre = fields.Char('mig_1nombre')
    mig_2cargo = fields.Char('mig_2cargo')
    mig_2nombre = fields.Char('mig_2nombre')
    mig_3cargo = fields.Char('mig_3cargo')
    mig_3nombre = fields.Char('mig_3nombre')
    mig_1telefono = fields.Char('mig_1telefono')
    mig_2telefono = fields.Char('mig_2telefono')
    mig_3telefono = fields.Char('mig_3telefono')
    mig_1email = fields.Char('mig_1email')
    mig_2email = fields.Char('mig_2email')
    mig_3email = fields.Char('mig_3email')
    mig_observacionescompra = fields.Text('mig_observacionescompra')
    mig_comentarios = fields.Text('mig_comentarios')
    mig_codigocontable = fields.Integer('mig_codigocontable')
    mig_codigodefinicion = fields.Char('mig_codigodefinicion')
    mig_codigocliente = fields.Integer('mig_codigocliente')
    mig_codigoseccion = fields.Char('mig_codigoseccion')
    mig_codigocanal = fields.Char('mig_codigocanal')
    mig_codigozona = fields.Char('mig_codigozona')
    mig_codigotransporte = fields.Char('mig_codigotransporte')
    mig_tipoportes = fields.Char('mig_tipoportes')
    mig_grupoiva = fields.Integer('mig_grupoiva')
    mig_indicadoriva = fields.Char('mig_indicadoriva')
    mig_dtoprontopago = fields.Float('mig_dtoprontopago')
    mig_retencion = fields.Integer('mig_retencion')
    mig_fechaapro = fields.Date('mig_fechaapro')

    # Campos de ventas:
    mig_fecha_alta = fields.Date('mig_fecha_alta')
    mig_fax = fields.Char('mig_fax')
    mig_descuento = fields.Char('mig_descuento')
    mig_codigocomisionista = fields.Integer('mig_codigocomisionista')
    mig_codigocomisionista2 = fields.Integer('mig_codigocomisionista2')
    mig_agruparalbaranes = fields.Char('mig_agruparalbaranes')
    mig_riesgomaximo = fields.Char('mig_riesgomaximo')
    mig_compariesgo = fields.Char('mig_compariesgo')
    mig_numriesgo = fields.Char('mig_numriesgo')
    mig_tpriesgo = fields.Char('mig_tpriesgo')
    mig_comeninplast = fields.Text('mig_comeninplast')
    mig_actualizaprecio = fields.Char('mig_actualizaprecio')
    mig_indicerevision = fields.Char('mig_indicerevision')
    mig_valultimoindice = fields.Integer('mig_valultimoindice')
    mig_fecharevisionprecio = fields.Date('mig_fecharevisionprecio')
    mig_palet1 = fields.Char('mig_palet1')
    mig_palet2 = fields.Char('mig_palet2')
    mig_palet3 = fields.Char('mig_palet3')
    mig_palet4 = fields.Char('mig_palet4')
    mig_palet5 = fields.Char('mig_palet5')
    mig_clientechep = fields.Char('mig_clientechep')
    mig_docsoporte = fields.Char('mig_docsoporte')
    mig_observacionestarifa = fields.Text('mig_observacionestarifa')
    mig_riesgoinplast = fields.Float('mig_riesgoinplast')
    mig_riesgoamapfre = fields.Float('mig_riesgoamapfre')
    mig_riesgoinplastfecha = fields.Date('mig_riesgoinplastfecha')
    mig_riesgomapfrefecha = fields.Date('mig_riesgomapfrefecha')
    mig_riesgoinplastfecharev = fields.Date('mig_riesgoinplastfecharev')
    mig_riesgomapfrefecharev = fields.Date('mig_riesgomapfrefecharev')
    mig_observaciones = fields.Text('mig_observaciones')
    mig_observacionescliente = fields.Text('mig_observacionescliente')
    mig_observacionesenvio = fields.Text('mig_observacionesenvio')
    mig_ibaninplast = fields.Char('mig_ibaninplast')
    mig_preciodistintocolor = fields.Char('mig_preciodistintocolor')
    mig_comenproformaa = fields.Text('mig_comenproformaa')
    mig_comenproformab = fields.Text('mig_comenproformab')
    mig_tipoc = fields.Char('mig_tipoc')
    mig_tipoc2 = fields.Char('mig_tipoc2')
    mig_codigocuenta = fields.Char('mig_codigocuenta')
    mig_agente1 = fields.Char('mig_agente1')
    mig_preciopead = fields.Integer('mig_preciopead')
    mig_tipocomunicacioncli = fields.Char('mig_tipocomunicacioncli')
    mig_spread = fields.Integer('mig_spread')
    mig_proformaemail = fields.Char('mig_proformaemail')
    mig_grupo = fields.Integer('mig_grupo')







