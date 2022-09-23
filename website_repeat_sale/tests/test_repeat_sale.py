#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase
from odoo.addons.website_repeat_sale.controllers.main import WebSaleOrderRepeat


class TestRepeatSale (HttpCase):

    def setUp(self):
        super().setUp()
        self.controller = WebSaleOrderRepeat()

    def test_repeat_order(self):

        def get_demo_orders():
            return self.env['sale.order'].search(
                [
                    ('partner_id', '=', self.ref('base.partner_demo')),
                ],
            )

        self.assertFalse(get_demo_orders())

        tour_service = "odoo.__DEBUG__.services['web_tour.tour']"
        self.browser_js(
            "/",
            "%s.run('shop_buy_product')" % tour_service,
            "%s.tours.shop_buy_product.ready" % tour_service,
            login="demo",
        )
        order = get_demo_orders()
        self.assertEquals(len(order), 1)
        # Repeat order with controller
        repeat_result = self.url_open('/order/repeat', data={'id': order.id})
        self.assertEqual(repeat_result.status_code, 200)
