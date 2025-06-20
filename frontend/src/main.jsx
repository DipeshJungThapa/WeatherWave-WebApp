// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { BrowserRouter } from 'react-router-dom';
import { DistrictProvider } from './context/DistrictContext.jsx';
import { AuthProvider } from './context/AuthContext.jsx';
import { PreferencesProvider } from './context/PreferencesContext.jsx'; // <--- NEW: Import PreferencesProvider

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      {/* <--- NEW: PreferencesProvider wraps everything else */}
      <PreferencesProvider>
        <AuthProvider>
          <DistrictProvider>
            <App />
          </DistrictProvider>
        </AuthProvider>
      </PreferencesProvider>
    </BrowserRouter>
  </React.StrictMode>,
);