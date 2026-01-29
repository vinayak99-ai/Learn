/**
 * Data Transfer Objects (DTOs) for Java Backend APIs
 * 
 * This file contains all request and response DTOs used by the
 * AssetDataController. These define the contract between the
 * Python orchestrator and Java backend.
 */

package com.investment.backend.dto;

import java.util.List;

// ============================================================================
// REQUEST DTOs
// ============================================================================

/**
 * Request DTO for getting asset price.
 */
public class AssetPriceRequest {
    private String assetId;
    
    public String getAssetId() { return assetId; }
    public void setAssetId(String assetId) { this.assetId = assetId; }
}

/**
 * Request DTO for getting asset classification.
 */
public class AssetClassificationRequest {
    private String assetId;
    
    public String getAssetId() { return assetId; }
    public void setAssetId(String assetId) { this.assetId = assetId; }
}

/**
 * Request DTO for getting asset baskets.
 */
public class AssetBasketRequest {
    private Criteria criteria;
    
    public Criteria getCriteria() { return criteria; }
    public void setCriteria(Criteria criteria) { this.criteria = criteria; }
    
    /**
     * Search criteria for filtering assets.
     */
    public static class Criteria {
        private String sector;
        private String industry;
        private String marketCap;
        private String priceRange;
        private Double minGrowth;
        
        // Getters and setters
        public String getSector() { return sector; }
        public void setSector(String sector) { this.sector = sector; }
        
        public String getIndustry() { return industry; }
        public void setIndustry(String industry) { this.industry = industry; }
        
        public String getMarketCap() { return marketCap; }
        public void setMarketCap(String marketCap) { this.marketCap = marketCap; }
        
        public String getPriceRange() { return priceRange; }
        public void setPriceRange(String priceRange) { this.priceRange = priceRange; }
        
        public Double getMinGrowth() { return minGrowth; }
        public void setMinGrowth(Double minGrowth) { this.minGrowth = minGrowth; }
    }
}

/**
 * Request DTO for getting asset research data.
 */
public class AssetResearchRequest {
    private String assetId;
    
    public String getAssetId() { return assetId; }
    public void setAssetId(String assetId) { this.assetId = assetId; }
}

// ============================================================================
// RESPONSE DTOs
// ============================================================================

/**
 * Response DTO for asset price data.
 */
public class AssetPriceResponse {
    private String assetId;
    private Double currentPrice;
    private Double previousClose;
    private Double changePercent;
    private Long volume;
    private String lastUpdated;
    
    // Getters and setters
    public String getAssetId() { return assetId; }
    public void setAssetId(String assetId) { this.assetId = assetId; }
    
    public Double getCurrentPrice() { return currentPrice; }
    public void setCurrentPrice(Double currentPrice) { this.currentPrice = currentPrice; }
    
    public Double getPreviousClose() { return previousClose; }
    public void setPreviousClose(Double previousClose) { this.previousClose = previousClose; }
    
    public Double getChangePercent() { return changePercent; }
    public void setChangePercent(Double changePercent) { this.changePercent = changePercent; }
    
    public Long getVolume() { return volume; }
    public void setVolume(Long volume) { this.volume = volume; }
    
    public String getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(String lastUpdated) { this.lastUpdated = lastUpdated; }
}

/**
 * Response DTO for asset classification data.
 */
public class AssetClassificationResponse {
    private String assetId;
    private String sector;
    private String industry;
    private String marketCap;
    private String geography;
    private String assetType;
    
    // Getters and setters
    public String getAssetId() { return assetId; }
    public void setAssetId(String assetId) { this.assetId = assetId; }
    
    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }
    
    public String getIndustry() { return industry; }
    public void setIndustry(String industry) { this.industry = industry; }
    
    public String getMarketCap() { return marketCap; }
    public void setMarketCap(String marketCap) { this.marketCap = marketCap; }
    
    public String getGeography() { return geography; }
    public void setGeography(String geography) { this.geography = geography; }
    
    public String getAssetType() { return assetType; }
    public void setAssetType(String assetType) { this.assetType = assetType; }
}

/**
 * Response DTO for asset basket search results.
 */
public class AssetBasketResponse {
    private List<String> assetIds;
    private Integer totalCount;
    
    // Getters and setters
    public List<String> getAssetIds() { return assetIds; }
    public void setAssetIds(List<String> assetIds) { 
        this.assetIds = assetIds;
        this.totalCount = assetIds != null ? assetIds.size() : 0;
    }
    
    public Integer getTotalCount() { return totalCount; }
    public void setTotalCount(Integer totalCount) { this.totalCount = totalCount; }
}

/**
 * Response DTO for asset research data.
 */
public class AssetResearchResponse {
    private String assetId;
    private Double peRatio;
    private Double revenueGrowth;
    private Double profitMargin;
    private String consensusRating;
    private Integer analystCount;
    private Double targetPrice;
    private List<String> riskFactors;
    
    // Getters and setters
    public String getAssetId() { return assetId; }
    public void setAssetId(String assetId) { this.assetId = assetId; }
    
    public Double getPeRatio() { return peRatio; }
    public void setPeRatio(Double peRatio) { this.peRatio = peRatio; }
    
    public Double getRevenueGrowth() { return revenueGrowth; }
    public void setRevenueGrowth(Double revenueGrowth) { this.revenueGrowth = revenueGrowth; }
    
    public Double getProfitMargin() { return profitMargin; }
    public void setProfitMargin(Double profitMargin) { this.profitMargin = profitMargin; }
    
    public String getConsensusRating() { return consensusRating; }
    public void setConsensusRating(String consensusRating) { 
        this.consensusRating = consensusRating; 
    }
    
    public Integer getAnalystCount() { return analystCount; }
    public void setAnalystCount(Integer analystCount) { this.analystCount = analystCount; }
    
    public Double getTargetPrice() { return targetPrice; }
    public void setTargetPrice(Double targetPrice) { this.targetPrice = targetPrice; }
    
    public List<String> getRiskFactors() { return riskFactors; }
    public void setRiskFactors(List<String> riskFactors) { this.riskFactors = riskFactors; }
}
