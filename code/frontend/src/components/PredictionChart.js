import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function PredictionChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({/* features */})
    })
    .then(res => res.json())
    .then(predictions => {
      setData(predictions.map((p, i) => ({ day: i+1, value: p })));
    });
  }, []);

  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="day" />
      <YAxis />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  );
}