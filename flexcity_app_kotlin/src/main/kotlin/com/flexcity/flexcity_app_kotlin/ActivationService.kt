package com.flexcity.flexcity_app_kotlin

import org.springframework.stereotype.Service
import java.time.LocalDate

@Service
class ActivationService {
    var assetsAvailable = listOf(
        Asset(
            "asset_a",
            "Only mondays",
            1.2,
            listOf(
                LocalDate.parse("2026-02-16"),
                LocalDate.parse("2026-02-23"),
                LocalDate.parse("2026-03-02"),
                LocalDate.parse("2026-03-09"),
                LocalDate.parse("2026-03-16"),
                LocalDate.parse("2026-03-23"),
                LocalDate.parse("2026-03-30")
            ),
            2
        ),
        Asset(
            "asset_b",
            "Only even days",
            1.0,
            listOf(
                LocalDate.parse("2026-02-16"),
                LocalDate.parse("2026-02-18"),
                LocalDate.parse("2026-02-20"),
                LocalDate.parse("2026-02-22"),
                LocalDate.parse("2026-02-24"),
                LocalDate.parse("2026-02-26"),
                LocalDate.parse("2026-02-28"),
                LocalDate.parse("2026-03-02"),
                LocalDate.parse("2026-03-04"),
                LocalDate.parse("2026-03-06"),
                LocalDate.parse("2026-03-08"),
                LocalDate.parse("2026-03-10"),
                LocalDate.parse("2026-03-12"),
                LocalDate.parse("2026-03-14"),
                LocalDate.parse("2026-03-16"),
                LocalDate.parse("2026-03-18"),
                LocalDate.parse("2026-03-20"),
                LocalDate.parse("2026-03-22"),
                LocalDate.parse("2026-03-24"),
                LocalDate.parse("2026-03-26"),
                LocalDate.parse("2026-03-28"),
                LocalDate.parse("2026-03-30")
            ),
            3
        ),
        Asset(
            "asset_c",
            "Every days",
            1.5,
            listOf(
                LocalDate.parse("2026-02-16"),
                LocalDate.parse("2026-02-17"),
                LocalDate.parse("2026-02-18"),
                LocalDate.parse("2026-02-19"),
                LocalDate.parse("2026-02-20"),
                LocalDate.parse("2026-02-21"),
                LocalDate.parse("2026-02-22"),
                LocalDate.parse("2026-02-23"),
                LocalDate.parse("2026-02-24"),
                LocalDate.parse("2026-02-25"),
                LocalDate.parse("2026-02-26"),
                LocalDate.parse("2026-02-27"),
                LocalDate.parse("2026-02-28"),
                LocalDate.parse("2026-03-01"),
                LocalDate.parse("2026-03-02"),
                LocalDate.parse("2026-03-03"),
                LocalDate.parse("2026-03-04"),
                LocalDate.parse("2026-03-05"),
                LocalDate.parse("2026-03-06"),
                LocalDate.parse("2026-03-07"),
                LocalDate.parse("2026-03-08"),
                LocalDate.parse("2026-03-09"),
                LocalDate.parse("2026-03-10"),
                LocalDate.parse("2026-03-11"),
                LocalDate.parse("2026-03-12"),
                LocalDate.parse("2026-03-13"),
                LocalDate.parse("2026-03-14"),
                LocalDate.parse("2026-03-15"),
                LocalDate.parse("2026-03-16"),
                LocalDate.parse("2026-03-17"),
                LocalDate.parse("2026-03-18"),
                LocalDate.parse("2026-03-19"),
                LocalDate.parse("2026-03-20"),
                LocalDate.parse("2026-03-21"),
                LocalDate.parse("2026-03-22"),
                LocalDate.parse("2026-03-23"),
                LocalDate.parse("2026-03-24"),
                LocalDate.parse("2026-03-25"),
                LocalDate.parse("2026-03-26"),
                LocalDate.parse("2026-03-27"),
                LocalDate.parse("2026-03-28"),
                LocalDate.parse("2026-03-29"),
                LocalDate.parse("2026-03-30")
            ),
            1
        )

    )

    fun selectAssets(date: LocalDate, volume: Int, assets: List<Asset>): List<AssetToActivate> {
        println("Activating assets for date: $date and volume: $volume")

        assetsAvailable = filterAssetsByDate(date, assets)

        //TODO implement activation logic

        //TODO REMOVE THIS FAKE RESPONSE
        return listOf(
            AssetToActivate("fake", "response", 1.0, 100, 10)
        )
    }

    fun updateAssets(assets: List<Asset>) {
        this.assetsAvailable = assets
        println("Assets updated: $assets")
    }

    fun filterAssetsByDate(date: LocalDate, assets: List<Asset>): List<Asset> {
        return assets.filter { it.availability.contains(date) }
    }
}