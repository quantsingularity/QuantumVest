const DataTracking = artifacts.require("DataTracking");

contract("DataTracking", (accounts) => {
  let instance;
  const admin = accounts[0];

  before(async () => {
    instance = await DataTracking.deployed();
  });

  it("should store market data", async () => {
    await instance.addDataPoint("ETH", 2500, 1000000, { from: admin });
    const data = await instance.getHistoricalData("ETH");
    assert.equal(data.length, 1, "Data storage failed");
  });
});
