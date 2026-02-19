import datetime
import unittest

from pydantic import TypeAdapter, RootModel

from flexcity_app.models import Asset
from flexcity_app.services.activation import (
    select_assets,
    algo_best_price_for_volume,
    get_total_volume_and_cost_asset,
    get_total_power_and_cost,
)


def add_availability_to_assets(assets: list[Asset], date: datetime.date):
    for asset in assets:
        asset.availability = [date]
    return assets


class TestActivation(unittest.TestCase):
    default_assets = [
        {
            "code": "asset_a",
            "name": "Only mondays",
            "activation_cost": 1.2,
            "availability": [
                "2026-02-16",
                "2026-02-23",
            ],
            "volume": 2,
        },
        {
            "code": "asset_b",
            "name": "Only even days",
            "activation_cost": 1.0,
            "availability": [
                "2026-02-16",
                "2026-02-18",
                "2026-02-20",
                "2026-02-22",
            ],
            "volume": 3,
        },
        {
            "code": "asset_c",
            "name": "Every days",
            "activation_cost": 1.5,
            "availability": [
                "2026-02-16",
                "2026-02-17",
                "2026-02-18",
                "2026-02-19",
                "2026-02-20",
                "2026-02-21",
                "2026-02-22",
                "2026-02-23",
            ],
            "volume": 1,
        },
    ]

    assets_asset_a_cheaper_all_others = [
        {
            "code": "asset_a",
            "name": "",
            "activation_cost": 1.7,
            "availability": ["2026-02-16"],
            "volume": 3,
        },
        {
            "code": "asset_b",
            "name": "",
            "activation_cost": 1.0,
            "availability": ["2026-02-16"],
            "volume": 1,
        },
        {
            "code": "asset_c",
            "name": "",
            "activation_cost": 1.5,
            "availability": ["2026-02-16"],
            "volume": 1,
        },
        {
            "code": "asset_d",
            "name": "",
            "activation_cost": 1.2,
            "availability": ["2026-02-16"],
            "volume": 1,
        },
    ]

    assets_asset_a_cheaper_all_others2 = [
        {
            "code": "asset_b",
            "name": "",
            "activation_cost": 1.0,
            "availability": ["2026-02-16"],
            "volume": 1,
        },
        {
            "code": "asset_c",
            "name": "",
            "activation_cost": 1.5,
            "availability": ["2026-02-16"],
            "volume": 1,
        },
        {
            "code": "asset_a",
            "name": "",
            "activation_cost": 1.7,
            "availability": ["2026-02-16"],
            "volume": 3,
        },
        {
            "code": "asset_d",
            "name": "",
            "activation_cost": 1.2,
            "availability": ["2026-02-16"],
            "volume": 1,
        },
    ]

    list_20_assets = [
        {
            "code": "asset_a",
            "name": "",
            "activation_cost": 1.2,
            "availability": [],
            "volume": 2,
        },
        {
            "code": "asset_b",
            "name": "",
            "activation_cost": 1.0,
            "availability": [],
            "volume": 3,
        },
        {
            "code": "asset_c",
            "name": "",
            "activation_cost": 1.5,
            "availability": [],
            "volume": 1,
        },
        {
            "code": "asset_d",
            "name": "",
            "activation_cost": 3.1,
            "availability": [],
            "volume": 4,
        },
        {
            "code": "asset_e",
            "name": "",
            "activation_cost": 0.5,
            "availability": [],
            "volume": 1,
        },
        {
            "code": "asset_f",
            "name": "",
            "activation_cost": 2.0,
            "availability": [],
            "volume": 2,
        },
        {
            "code": "asset_g",
            "name": "",
            "activation_cost": 1.8,
            "availability": [],
            "volume": 3,
        },
        {
            "code": "asset_h",
            "name": "",
            "activation_cost": 0.8,
            "availability": [],
            "volume": 1,
        },
        {
            "code": "asset_i",
            "name": "",
            "activation_cost": 2.5,
            "availability": [],
            "volume": 4,
        },
        {
            "code": "asset_j",
            "name": "",
            "activation_cost": 1.3,
            "availability": [],
            "volume": 2,
        },
        {
            "code": "asset_k",
            "name": "",
            "activation_cost": 0.9,
            "availability": [],
            "volume": 1,
        },
        {
            "code": "asset_l",
            "name": "",
            "activation_cost": 2.2,
            "availability": [],
            "volume": 3,
        },
        {
            "code": "asset_m",
            "name": "",
            "activation_cost": 1.6,
            "availability": [],
            "volume": 2,
        },
        {
            "code": "asset_n",
            "name": "",
            "activation_cost": 0.7,
            "availability": [],
            "volume": 1,
        },
        {
            "code": "asset_o",
            "name": "",
            "activation_cost": 2.8,
            "availability": [],
            "volume": 4,
        },
        {
            "code": "asset_p",
            "name": "",
            "activation_cost": 1.4,
            "availability": [],
            "volume": 15,
        },
    ]

    list_assets_with_even_volume = [
        {
            "code": "asset_a",
            "name": "",
            "activation_cost": 1.2,
            "availability": [],
            "volume": 2,
        },
        {
            "code": "asset_b",
            "name": "",
            "activation_cost": 2.1,
            "availability": [],
            "volume": 6,
        },
        {
            "code": "asset_c",
            "name": "",
            "activation_cost": 0.5,
            "availability": [],
            "volume": 2,
        },
        {
            "code": "asset_d",
            "name": "",
            "activation_cost": 1.5,
            "availability": [],
            "volume": 4,
        },
        {
            "code": "asset_e",
            "name": "",
            "activation_cost": 3.1,
            "availability": [],
            "volume": 8,
        },
    ]

    def test_select_asset(self):
        date = datetime.date.fromisoformat("2026-02-16")
        volume = 4
        asset_list = TypeAdapter(list[Asset]).validate_python(self.default_assets)

        res = select_assets(date, volume, asset_list)

        total_power, cost = get_total_power_and_cost(res)

        self.assertEqual(2, len(res))
        self.assertEqual(4, total_power)
        self.assertEqual(2.5, cost)
        total_volume, cost = get_total_volume_and_cost_asset(res)
        self.assertTupleEqual((total_power, cost), (total_volume, cost))

    def test_select_assets_requested_volume_too_high(self):
        date = datetime.date.fromisoformat("2026-02-17")
        volume = 4
        asset_list = TypeAdapter(list[Asset]).validate_python(self.default_assets)

        with self.assertRaises(ValueError):
            select_assets(date, volume, asset_list)

    def test_select_assets_one_asset_is_cheaper_than_all_others(self):
        date = datetime.date.fromisoformat("2026-02-16")
        volume = 3
        asset_list = TypeAdapter(list[Asset]).validate_python(
            self.assets_asset_a_cheaper_all_others
        )

        res = select_assets(date, volume, asset_list)

        power, cost = get_total_power_and_cost(res)

        self.assertEqual(1, len(res))
        self.assertEqual(3, power)
        self.assertEqual(1.7, cost)

    def test_select_assets_one_asset_is_cheaper_than_all_others_new_order(self):
        date = datetime.date.fromisoformat("2026-02-16")
        volume = 3
        asset_list = TypeAdapter(list[Asset]).validate_python(
            self.assets_asset_a_cheaper_all_others2
        )

        res = select_assets(date, volume, asset_list)

        power, cost = get_total_power_and_cost(res)

        self.assertEqual(1, len(res))
        self.assertEqual(3, power)
        self.assertEqual(1.7, cost)

    def test_algo_default_assets(self):
        volume = 4
        asset_list = TypeAdapter(list[Asset]).validate_python(self.default_assets)

        res = algo_best_price_for_volume(volume, asset_list)

        self.assertListEqual(["asset_b", "asset_c"], [asset.code for asset in res])
        power, cost = get_total_volume_and_cost_asset(res)
        self.assertEqual(4, power)
        self.assertEqual(2.5, cost)

    def test_algo_20_assets_volume_8(self):
        volume = 8
        asset_list = TypeAdapter(list[Asset]).validate_python(self.list_20_assets)

        res = algo_best_price_for_volume(volume, asset_list)

        self.assertListEqual(["asset_a", "asset_b", "asset_g"], [a.code for a in res])
        power, cost = get_total_volume_and_cost_asset(res)
        self.assertEqual(8, power)
        self.assertEqual(4.0, cost)

    def test_algo_20_assets_volume_13(self):
        volume = 13
        asset_list = TypeAdapter(list[Asset]).validate_python(self.list_20_assets)

        res = algo_best_price_for_volume(volume, asset_list)

        self.assertListEqual(
            ["asset_a", "asset_b", "asset_e", "asset_g", "asset_i"],
            [a.code for a in res],
        )
        power, cost = get_total_volume_and_cost_asset(res)
        self.assertEqual(13, power)
        self.assertEqual(7.0, cost)

    def test_algo_best_price_for_volume_assets_even_volume_odd(self):
        volume = 7
        asset_list = TypeAdapter(list[Asset]).validate_python(
            self.list_assets_with_even_volume
        )

        res = algo_best_price_for_volume(volume, asset_list)

        self.assertListEqual(["asset_c", "asset_d"], [a.code for a in res])
        power, cost = get_total_volume_and_cost_asset(res)
        self.assertEqual(6, power)
        self.assertEqual(2, cost)

    def test_select_assets_assets_even_volume_odd(self):
        volume = 7
        date = datetime.date.fromisoformat("2026-02-16")
        asset_list = TypeAdapter(list[Asset]).validate_python(
            self.list_assets_with_even_volume
        )
        add_availability_to_assets(asset_list, date)

        res = select_assets(date, volume, asset_list)

        self.assertListEqual(["asset_b", "asset_c"], [a.code for a in res])
        total_volume, cost = get_total_volume_and_cost_asset(res)
        self.assertEqual(8, total_volume)
        self.assertEqual(2.6, cost)
        power_activated, cost = get_total_power_and_cost(res)
        self.assertEqual(7, power_activated)
        self.assertEqual(2.6, cost)

    def test_helper_to_fill_date_in_assets(self):
        """helper to fill date in assets and print results"""
        Assets = RootModel[list[Asset]]
        date = datetime.date.fromisoformat("2026-02-16")
        # 20 assets
        assets_to_fill = self.list_20_assets
        # even volume
        # assets_to_fill = self.list_20_assets

        asset_list = TypeAdapter(list[Asset]).validate_python(assets_to_fill)

        assets = Assets([asset for asset in asset_list])
        add_availability_to_assets(asset_list, date)

        one_line_str = assets.model_dump_json()
        print(one_line_str)

        indent_str = assets.model_dump_json(indent=2)
        print(indent_str)
