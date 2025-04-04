import React, { useState } from 'react';
import { Button, Slider, Typography } from '@material-ui/core';

export default function PortfolioOptimization() {
  const [risk, setRisk] = useState(5);
  const [result, setResult] = useState(null);

  const optimize = async () => {
    const response = await fetch('/api/optimize', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ riskLevel: risk })
    });
    setResult(await response.json());
  };

  return (
    <div>
      <Typography>Risk Tolerance: {risk}</Typography>
      <Slider value={risk} onChange={(e,v) => setRisk(v)} min={1} max={10} />
      <Button variant="contained" onClick={optimize}>Optimize</Button>
      {result && (
        <div>
          <Typography>Recommended Allocation:</Typography>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}