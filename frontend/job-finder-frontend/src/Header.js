// Header.js

import React from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

const WebsiteHeader = () => {
  return (
    <header className="website-header">
      <nav className="navbar navbar-expand-md navbar-light bg-light">
        <div className="container text-center">
          <NavLink exact to="/" className="navbar-brand mx-auto">
            Job Finder
          </NavLink>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <NavLink exact to="/" className="nav-link" activeClassName="active">
                  Home
                </NavLink>
              </li>
              <li className="nav-item">
              </li>
              <li>
                <NavLink to="/find-jobs" className="nav-link" activeClassName="active">
                  Find jobs
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default WebsiteHeader;
