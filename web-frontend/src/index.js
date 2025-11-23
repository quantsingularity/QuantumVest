import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { ThemeProvider } from './contexts/ThemeContext';
import { NotificationProvider } from './contexts/NotificationContext';
import './styles/App.css';

ReactDOM.render(
    <React.StrictMode>
        <ThemeProvider>
            <NotificationProvider>
                <App />
            </NotificationProvider>
        </ThemeProvider>
    </React.StrictMode>,
    document.getElementById('root'),
);
