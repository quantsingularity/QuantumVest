import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/pages/Dashboard';
import PredictionChart from './components/pages/PredictionChart';
import PortfolioOptimization from './components/pages/PortfolioOptimization';
import Analytics from './components/pages/Analytics';
import Settings from './components/pages/Settings';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Sidebar from './components/layout/Sidebar';
import ErrorBoundary from './components/ui/ErrorBoundary';
import ToastManager from './components/ui/ToastManager';
import { ThemeProvider } from './contexts/ThemeContext';
import { motion, AnimatePresence } from 'framer-motion';
import './styles/App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentPage, setCurrentPage] = useState('Dashboard');
  
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Update page title based on current route
  const updatePageTitle = (pathname) => {
    switch(pathname) {
      case '/':
        setCurrentPage('Dashboard');
        break;
      case '/predictions':
        setCurrentPage('Predictions');
        break;
      case '/optimize':
        setCurrentPage('Portfolio Optimization');
        break;
      case '/analytics':
        setCurrentPage('Analytics');
        break;
      case '/settings':
        setCurrentPage('Settings');
        break;
      default:
        setCurrentPage('Dashboard');
    }
  };

  // Page transition variants
  const pageVariants = {
    initial: {
      opacity: 0,
      y: 20
    },
    in: {
      opacity: 1,
      y: 0
    },
    out: {
      opacity: 0,
      y: -20
    }
  };

  const pageTransition = {
    type: 'tween',
    ease: 'anticipate',
    duration: 0.4
  };

  return (
    <ThemeProvider>
      <Router>
        <div className="app-container">
          <ErrorBoundary>
            <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
            <div className={`content-wrapper ${sidebarOpen ? 'sidebar-open' : ''}`}>
              <Header toggleSidebar={toggleSidebar} pageTitle={currentPage} />
              <main className="main-content">
                <ErrorBoundary>
                  <Routes>
                    <Route path="/" element={
                      <AnimatePresence mode="wait">
                        <motion.div
                          key="dashboard"
                          initial="initial"
                          animate="in"
                          exit="out"
                          variants={pageVariants}
                          transition={pageTransition}
                          onLoad={() => updatePageTitle('/')}
                        >
                          <Dashboard />
                        </motion.div>
                      </AnimatePresence>
                    } />
                    <Route path="/predictions" element={
                      <AnimatePresence mode="wait">
                        <motion.div
                          key="predictions"
                          initial="initial"
                          animate="in"
                          exit="out"
                          variants={pageVariants}
                          transition={pageTransition}
                          onLoad={() => updatePageTitle('/predictions')}
                        >
                          <PredictionChart />
                        </motion.div>
                      </AnimatePresence>
                    } />
                    <Route path="/optimize" element={
                      <AnimatePresence mode="wait">
                        <motion.div
                          key="optimize"
                          initial="initial"
                          animate="in"
                          exit="out"
                          variants={pageVariants}
                          transition={pageTransition}
                          onLoad={() => updatePageTitle('/optimize')}
                        >
                          <PortfolioOptimization />
                        </motion.div>
                      </AnimatePresence>
                    } />
                    <Route path="/analytics" element={
                      <AnimatePresence mode="wait">
                        <motion.div
                          key="analytics"
                          initial="initial"
                          animate="in"
                          exit="out"
                          variants={pageVariants}
                          transition={pageTransition}
                          onLoad={() => updatePageTitle('/analytics')}
                        >
                          <Analytics />
                        </motion.div>
                      </AnimatePresence>
                    } />
                    <Route path="/settings" element={
                      <AnimatePresence mode="wait">
                        <motion.div
                          key="settings"
                          initial="initial"
                          animate="in"
                          exit="out"
                          variants={pageVariants}
                          transition={pageTransition}
                          onLoad={() => updatePageTitle('/settings')}
                        >
                          <Settings />
                        </motion.div>
                      </AnimatePresence>
                    } />
                  </Routes>
                </ErrorBoundary>
              </main>
              <Footer />
            </div>
            <ToastManager />
          </ErrorBoundary>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
