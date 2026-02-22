package com.flexcity.flexcity_app_kotlin

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

@RestController
class ActivationController(private val assetService: ActivationService) {
    @PostMapping("/activation")
    fun activation(@RequestBody body: ActivationBody): ResponseEntity<List<AssetToActivate>> {
        println("Received activation request for date: ${body.date} and volume: ${body.volume}")
        println("current list of assets: ${assetService.assetsAvailable}")

        val assetsToActivate = assetService.selectAssets(body.date, body.volume, assetService.assetsAvailable)

        return ResponseEntity.ok().body(assetsToActivate)
    }

    @PutMapping("/assets")
    fun updateAssets(@RequestBody assets: List<Asset>): ResponseEntity<Void> {
        assetService.updateAssets(assets)
        return ResponseEntity.noContent().build()
    }
}