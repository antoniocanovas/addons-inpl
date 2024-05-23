# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from .common import TestL10nEsIpnrCommon


class TestL10nEsIpnrPriceRange(TestL10nEsIpnrCommon):
    def test_wrong_date(self):
        with self.assertRaises(ValidationError):
            self.env["l10n.es.ipnr.amount"].create(
                {
                    "name": "Test",
                    "price": 0.1,
                    "date_from": "2021-01-01",
                    "date_to": "2020-01-01",
                }
            )

    def test_overlapping_dates(self):
        self.env["l10n.es.ipnr.amount"].create(
            {
                "name": "Test-1",
                "price": 0.1,
                "date_from": "2020-01-01",
                "date_to": "2021-01-01",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["l10n.es.ipnr.amount"].create(
                {
                    "name": "Test-2",
                    "price": 0.1,
                    "date_from": "2020-01-07",
                    "date_to": "2021-01-07",
                }
            )

    def test_ipnr_date_from_required(self):
        with self.assertRaises(ValidationError):
            self.company.write({"ipnr_date_from": False})
