import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../../styles/Sidebar.css';
import { motion } from 'framer-motion';

const Sidebar = ({ isOpen, toggleSidebar }) => {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname === path ? 'active' : '';
    };

    return (
        <>
            {isOpen && <div className="sidebar-overlay" onClick={toggleSidebar}></div>}
            <motion.aside
                className={`sidebar ${!isOpen ? 'sidebar-collapsed' : ''}`}
                initial={{ x: -280 }}
                animate={{ x: isOpen ? 0 : -280 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
                <div className="sidebar-header">
                    <div className="logo">
                        <div className="logo-icon">Q</div>
                        <h2>QuantumVest</h2>
                    </div>
                </div>

                <nav className="sidebar-nav">
                    <ul>
                        <motion.li whileHover={{ x: 5 }} transition={{ duration: 0.2 }}>
                            <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
                                <i className="nav-icon dashboard-icon"></i>
                                <span>Dashboard</span>
                            </Link>
                        </motion.li>
                        <motion.li whileHover={{ x: 5 }} transition={{ duration: 0.2 }}>
                            <Link to="/" className={`nav-link ${isActive('/')}`}>
                                <i className="nav-icon home-icon"></i>
                                <span>Home</span>
                            </Link>
                        </motion.li>
                        <motion.li whileHover={{ x: 5 }} transition={{ duration: 0.2 }}>
                            <Link
                                to="/predictions"
                                className={`nav-link ${isActive('/predictions')}`}
                            >
                                <i className="nav-icon predictions-icon"></i>
                                <span>Predictions</span>
                            </Link>
                        </motion.li>
                        <motion.li whileHover={{ x: 5 }} transition={{ duration: 0.2 }}>
                            <Link to="/optimize" className={`nav-link ${isActive('/optimize')}`}>
                                <i className="nav-icon portfolio-icon"></i>
                                <span>Portfolio</span>
                            </Link>
                        </motion.li>
                        <motion.li whileHover={{ x: 5 }} transition={{ duration: 0.2 }}>
                            <Link to="/analytics" className={`nav-link ${isActive('/analytics')}`}>
                                <i className="nav-icon analytics-icon"></i>
                                <span>Analytics</span>
                            </Link>
                        </motion.li>
                        <motion.li whileHover={{ x: 5 }} transition={{ duration: 0.2 }}>
                            <Link to="/settings" className={`nav-link ${isActive('/settings')}`}>
                                <i className="nav-icon settings-icon"></i>
                                <span>Settings</span>
                            </Link>
                        </motion.li>
                    </ul>
                </nav>

                <div className="sidebar-footer">
                    <div className="user-info">
                        <div className="user-avatar">JD</div>
                        <div className="user-details">
                            <p className="user-name">John Doe</p>
                            <p className="user-plan">Premium Plan</p>
                        </div>
                    </div>
                </div>
            </motion.aside>
        </>
    );
};

export default Sidebar;
