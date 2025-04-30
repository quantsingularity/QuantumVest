import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import './styles/App.css';

// Components
import Dashboard from './components/Dashboard';
import PredictionChart from './components/PredictionChart';
import PortfolioOptimization from './components/PortfolioOptimization';
import Analytics from './components/pages/Analytics';
import Settings from './components/pages/Settings';
import Homepage from './components/pages/Homepage/Homepage';
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import ErrorBoundary from './components/ui/ErrorBoundary';
import ToastManager from './components/ui/ToastManager';

// Context Providers
import { ThemeProvider } from './contexts/ThemeContext';

// App wrapper to access router context
function AppContent() {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentPage, setCurrentPage] = useState('Dashboard');
  const [isHomepage, setIsHomepage] = useState(location.pathname === '/');
  
  useEffect(() => {
    // Update isHomepage state whenever location changes
    setIsHomepage(location.pathname === '/');
    updatePageTitle(location.pathname);
  }, [location]);
  
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };
  
  // Update page title based on current route
  const updatePageTitle = (pathname) => {
    switch(pathname) {
      case '/':
        setCurrentPage('Home');
        break;
      case '/dashboard':
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
    <div className="app-container">
      <ErrorBoundary>
        <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
        <div className={`content-wrapper ${sidebarOpen ? 'sidebar-open' : ''} ${isHomepage ? 'homepage-mode' : ''}`}>
          <Header toggleSidebar={toggleSidebar} pageTitle={currentPage} />
          <main className={`main-content ${isHomepage ? 'homepage-content' : ''}`}>
            <ErrorBoundary>
              <Routes>
                <Route path="/" element={
                  <AnimatePresence mode="wait">
                    <motion.div
                      key="homepage"
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
                    >
                      <Homepage />
                    </motion.div>
                  </AnimatePresence>
                } />
                <Route path="/dashboard" element={
                  <AnimatePresence mode="wait">
                    <motion.div
                      key="dashboard"
                      initial="initial"
                      animate="in"
                      exit="out"
                      variants={pageVariants}
                      transition={pageTransition}
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
  );
}

// Main App component
function App() {
  return (
    <ThemeProvider>
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;
