import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PredictionChart from './components/PredictionChart';
import PortfolioOptimization from './components/PortfolioOptimization';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Dashboard} />
        <Route path="/predictions" component={PredictionChart} />
        <Route path="/optimize" component={PortfolioOptimization} />
      </Switch>
    </Router>
  );
}

export default App;