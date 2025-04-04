import React, { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography } from '@material-ui/core';

export default function Dashboard() {
  const [marketData, setMarketData] = useState([]);

  useEffect(() => {
    fetch('/api/blockchain-data/ETH')
      .then(res => res.json())
      .then(data => setMarketData(data));
  }, []);

  return (
    <Grid container spacing={3}>
      {marketData.slice(-5).map((entry, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <Card>
            <CardContent>
              <Typography>Price: ${entry.price}</Typography>
              <Typography>Volume: {entry.volume}</Typography>
              <Typography color="textSecondary">
                {new Date(entry.timestamp*1000).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}