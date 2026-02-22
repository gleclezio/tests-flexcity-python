package com.flexcity.flexcity_app_kotlin

import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test
import java.time.LocalDate

class ActivationServiceTest {
    val assets = listOf(
        Asset(
            "asset_a",
            "",
            1.2,
            listOf(
                LocalDate.parse("2026-02-16"), LocalDate.parse("2026-02-23")
            ),
            2
        ),
        Asset(
            "asset_b",
            "",
            1.0,
            listOf(
                LocalDate.parse("2026-02-16"),
                LocalDate.parse("2026-02-18"),
            ),
            3
        ),
        Asset(
            "asset_c",
            "",
            1.5,
            listOf(
                LocalDate.parse("2026-02-16"),
                LocalDate.parse("2026-02-17"),
                LocalDate.parse("2026-02-18"),
            ),
            1
        )
    )

    @Test
    fun filterAssetsByDate() {
        val activationService = ActivationService()
        val date = LocalDate.parse("2026-02-17")

        val res = activationService.filterAssetsByDate(date, this.assets)
        assertEquals(1, res.size)
    }


}