# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    def calcular_digito_verificador(self, numero):
        # Invertir el número para empezar desde el final
        numero = numero[::-1]

        suma = 0
        # Aplicar las multiplicaciones de 3 y 1 alternadas
        for i, digito in enumerate(numero):
            digito = int(digito)
            if i % 2 == 0:
                suma += digito * 3
            else:
                suma += digito * 1

        # Calcular el dígito verificador
        siguiente_decena = (suma + 9) // 10 * 10
        digito_verificador = siguiente_decena - suma

        return digito_verificador

    def generar_sscc(self, digito_extension, numero_identificacion_empresa, numero_serie):
        # Concatenar los componentes del SSCC
        base_sscc = f"{digito_extension}{numero_identificacion_empresa}{numero_serie}"

        # Calcular el dígito verificador
        digito_verificador = self.calcular_digito_verificador(base_sscc)

        # Formar el SSCC completo
        sscc_completo = f"{base_sscc}{digito_verificador}"

        return sscc_completo

