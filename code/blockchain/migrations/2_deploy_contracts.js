const DataTracking = artifacts.require("DataTracking");
const TrendAnalysis = artifacts.require("TrendAnalysis");

module.exports = async function(deployer) {
  await deployer.deploy(DataTracking);
  const dataTracker = await DataTracking.deployed();
  
  // Use Chainlink ETH/USD price feed address
  await deployer.deploy(TrendAnalysis, "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"); 
};