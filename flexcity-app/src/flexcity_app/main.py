from fastapi import FastAPI, HTTPException

from flexcity_app.models import ActivationBody, Asset, AssetToActivate
from .config import settings
from .services.activation import (
    select_assets,
    get_total_power_and_cost,
    get_total_volume_and_cost_asset,
)

app = FastAPI(
    title="Activation API",
    description="API to activate assets based on requested date and volume",
)


@app.post(
    "/activation",
    response_model=list[AssetToActivate],
    responses={500: {"model": str}},
    summary="Activate assets based on requested date and volume",
    description="Provide a date in format 'YYYY-MM-DD' and a integer volume",
)
def activation(data: ActivationBody):
    try:
        print(f"activation received {str(data.date)=} {data.volume=}")
        print(f"current asset list {settings.asset_list=}")

        result = select_assets(data.date, data.volume, settings.asset_list)

        print(f"Assets selected for activation: {[asset.code for asset in result]}")
        total_power, cost = get_total_power_and_cost(result)
        total_volume_available, _ = get_total_volume_and_cost_asset(result)
        print(
            f"Total power: {total_power} kW, Total cost: {cost} € - (Total volume available: {total_volume_available} kW)"
        )

        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put(
    "/assets",
    status_code=204,
    summary="Update the list of assets available for activation",
    description="Provide a list of assets with their code, name, activation cost, availability and volume",
)
def update_assets(assets: list[Asset]):
    print("request to update assets")

    # print(f"current asset list {settings.asset_list=}")
    settings.asset_list = assets
    print(f"updated asset list {settings.asset_list=}")
