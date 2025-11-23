import React from 'react';
import { Link } from 'react-router-dom';
import '../../../styles/Homepage.css';

const HomepageNavMenu = () => {
    return (
        <div className="homepage-nav-menu">
            <div className="homepage-nav-container">
                <div className="homepage-nav-logo">
                    <div className="logo-icon">Q</div>
                    <span>QuantumVest</span>
                </div>
                <nav className="homepage-nav-links">
                    <Link to="/" className="homepage-nav-link active">
                        Home
                    </Link>
                    <Link to="/dashboard" className="homepage-nav-link">
                        Dashboard
                    </Link>
                    <Link to="/predictions" className="homepage-nav-link">
                        Predictions
                    </Link>
                    <Link to="/optimize" className="homepage-nav-link">
                        Portfolio
                    </Link>
                    <Link to="/analytics" className="homepage-nav-link">
                        Analytics
                    </Link>
                    <Link to="/settings" className="homepage-nav-link">
                        Settings
                    </Link>
                </nav>
                <div className="homepage-nav-actions">
                    <Link to="/dashboard" className="homepage-nav-button">
                        Get Started
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default HomepageNavMenu;
