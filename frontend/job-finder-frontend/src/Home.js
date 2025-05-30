// Home.js
import React from 'react';

export default function Home() {
  return (
    <div className="container text-center my-5">
      <h1 className="display-4 fw-bold mb-4">Welcome to Job Finder</h1>
      <p className="lead mb-4">
        Your career starts here. Upload your CV or select your traits manually and find jobs best suited for you.
      </p>
      <a href="/find-jobs" className="btn btn-primary btn-lg">
        Get Started &nbsp; <span aria-hidden="true">→</span>
      </a>
    </div>
  );
}
