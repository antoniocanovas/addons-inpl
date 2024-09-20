=======
SSCC generator base
=======

.. |badge1| image:: /pnt_sscc_generator_base/static/img/status.png
    :alt: Production/Stable
.. |badge2| image:: /pnt_sscc_generator_base/static/img/license.png
    :alt: License: AGPL-3

|badge1| |badge2|

Hereda de ir.sequence para generar códigos de expedición SSCC.

**Índice de contenidos**

.. contents::
   :local:

Instalación
===========

Acceder a aplicaciones e instalar el módulo SSCC code Generator.

Configuración
=============

En configuración de inventario hay un nuevo menú para configurar la secuencia para códigos SSCC.

Uso
===

Este módulo debe ser usado para generar los códigos de expedición.
SSCC = self.env["ir.sequence"].next_by_code("pnt.sscc.code")

Limitaciones / Problemas conocidos
==================================

No se conocen.

Registro de cambios
===================

17.0.1.0.0 (09-09-2024)
~~~~~~~~~~~~~~~~~~~~~~~

* Versión inicial.

Creditos
========

Autores
~~~~~~~

* `Punt Sistemes <https://www.puntsistemes.es>`__

Contribuidores
~~~~~~~~~~~~~~

* `Punt Sistemes <https://www.puntsistemes.es>`__:

  * Pedro Baños <pguirao@puntsistemes.es>
  * Adrián Muñoz <amunoz@puntsistemes.es>


Mantenedores
~~~~~~~~~~~~

Mantenido por `Punt Sistemes <https://www.puntsistemes.es>`__.

.. image:: /pnt_sscc_generator_base/static/img/punt-sistemes.png
   :alt: Punt Sistemes
   :target: https://www.puntsistemes.es
