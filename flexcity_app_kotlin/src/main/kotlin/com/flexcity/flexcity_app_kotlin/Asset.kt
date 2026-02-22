package com.flexcity.flexcity_app_kotlin

import java.time.LocalDate

data class Asset(
    val code: String,
    val name: String,
    val activationCost: Double,
    val availability: List<LocalDate>,
    val volume: Int
)

data class AssetToActivate(
    val code: String,
    val name: String,
    val activationCost: Double,
    val powerRequested: Int,
    val volume: Int
)
