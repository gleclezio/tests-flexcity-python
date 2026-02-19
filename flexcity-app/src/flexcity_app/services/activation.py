import datetime

from flexcity_app.models import Asset, AssetToActivate


def select_assets(
    date: datetime.date, volume: int, asset_list: list[Asset]
) -> list[AssetToActivate]:
    """
    Select assets to activate based on the requested date and volume.
    The selection has the cheapest cost for at least the requested volume.

    :param date: The date for which the activation is requested
    :param volume: The total volume of kW needed
    :param asset_list: The list of available assets
    :return: A list of selected assets to activate
    :raises ValueError: If there is not enough available power to reach the requested volume
    """
    # Only keep assets available on the requested date
    available_assets = [asset for asset in asset_list if date in asset.availability]

    # check if we can cover the activation volume request
    available_power = sum(asset.volume for asset in available_assets)
    if available_power < volume:
        raise ValueError(
            f"Not enough available power to reach the requested volume. Available: {available_power} kW, requested: {volume} kW"
        )

    # Try, 1st, to reach the requested volume
    # if result power < requested volume, we increase the volume request until we reach it
    selected_assets = []
    power_request = volume
    power = volume - 1
    while power < volume:
        selected_assets = algo_best_price_for_volume(power_request, available_assets)
        power, _ = get_total_volume_and_cost_asset(selected_assets)
        power_request += 1

    # prepare output data model with only expected fields (remove availability for example)
    asset_to_activate = [
        AssetToActivate(**asset.model_dump()) for asset in selected_assets
    ]

    # Shall we reduce volume of assets to fit the requested volume ?
    # check if we will provide more power than requested
    if power > volume:
        power_gap = power - volume
        # reduce power on at least one asset
        try:
            # downgrade the asset with the biggest volume that can be downgraded to fill the gap
            # TODO can be optimized, but keep it simple for now
            asset_to_downgrade = max(
                [asset for asset in asset_to_activate if asset.volume > power_gap],
                key=lambda asset: asset.volume,
            )
            asset_to_downgrade.power_requested = asset_to_downgrade.volume - power_gap
        except ValueError:
            print("no asset can be downgraded, we keep the overproduction")

    return asset_to_activate


def get_total_volume_and_cost_asset(
    assets: list[Asset] | list[AssetToActivate],
) -> tuple[int, float]:
    """Calculate the total volume and total cost of a list of assets."""
    total_volume = sum(asset.volume for asset in assets)
    total_cost = sum(asset.activation_cost for asset in assets)
    return total_volume, total_cost


def get_total_power_and_cost(assets: list[AssetToActivate]):
    """Calculate the total power requested and total cost of a list of assets."""
    total_power = sum(asset.power_requested for asset in assets)
    total_cost = sum(asset.activation_cost for asset in assets)
    return total_power, total_cost


# def algo_simplest(volume: int, asset_list: list[Asset]) -> list[AssetToActivate]:
#     # Sort assets cheapest first
#     sorted_assets = sorted(asset_list, key=lambda asset: asset.activation_cost)
#
#     selected_assets: list[AssetToActivate] = []
#     remaining_volume = volume
#
#     for asset in sorted_assets:
#         if remaining_volume <= 0:
#             break
#
#         # Determine how much volume to activate for this asset
#         activation_volume = min(asset.volume, remaining_volume)
#
#         # Create AssetToActivate instance with the requested power
#         asset_input_data = asset.model_dump() | {"power_requested": activation_volume}
#         selected_assets.append(AssetToActivate(**asset_input_data))
#
#         remaining_volume -= activation_volume
#
#     return selected_assets


def algo_best_price_for_volume(max_volume: int, asset_list: list[Asset]) -> list[Asset]:
    """Dynamic programming algorithm to find the combination of assets that provides the best price for a given volume.

    If we are not able to find a price for the requested volume, the function returns the best price for the closest volume below the requested volume.

    :param max_volume: The maximum volume requested
    :param asset_list: The list of assets
    :return: The list of assets that provides the best price for the given volume.
    """
    # print(f"Algo input \n\t{max_volume=}\n\t{asset_list=}")

    INF = float("inf")
    # best prices for each volume from 0 to max_volume (best price set to infinity)
    best_prices = [INF] * (max_volume + 1)
    best_prices[0] = 0
    # assets chosen for each volume from 0 to max_volume
    chosen = [[] for _ in range(max_volume + 1)]

    for asset in asset_list:
        cost = asset.activation_cost
        volume = asset.volume

        if volume > max_volume:
            continue

        # for each capacity from max_volume to the current asset volume
        for v in range(max_volume, volume - 1, -1):
            new_cost = best_prices[v - volume] + cost
            # check if the price of the gap (current capacity - asset volume) is defined
            # and if the price of the current capacity is better
            if best_prices[v - volume] != INF and new_cost < best_prices[v]:
                best_prices[v] = new_cost
                chosen[v] = chosen[v - volume] + [asset]

    # get the best volume found
    best_volume = max((v for v in range(max_volume + 1) if best_prices[v] != INF))

    return chosen[best_volume]
