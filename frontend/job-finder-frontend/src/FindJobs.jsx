import React, { useEffect, useState } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'

export default function FindJobs() {
  const [specs, setSpecs] = useState([])
  const [selected, setSelected] = useState({})
  const [experience, setExperience] = useState('')
  const [jobLinks, setJobLinks] = useState({})
  const [loading, setLoading] = useState(false)
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')
  const [cvLoading, setCvLoading] = useState(false)

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/specs/').then(({ data }) => {
      const result = []
      for (const [site, list] of Object.entries(data)) {
        list.forEach(name => result.push({ site, name }))
      }
      setSpecs(result)
    })
  }, [])

  const handleSiteClick = site =>
    setSelected(prev => ({
      ...prev,
      [site]: { ...(prev[site] || {}), _open: !prev[site]?._open }
    }))

  const handleSpecClick = (site, name) =>
    setSelected(prev => ({
      ...prev,
      [site]: { ...prev[site], [name]: !prev[site]?.[name] }
    }))

  const updateExperience = level => setExperience(level)

  const fetchJobs = async () => {
    const chosen = Object.entries(selected).flatMap(([site, values]) =>
      Object.keys(values)
        .filter(key => key !== '_open' && values[key])
        .map(name => ({ site, name }))
    )
    if (!experience || !chosen.length) {
      alert('Choose experience level and at least one specialization.')
      return
    }

    setLoading(true)
    const params = new URLSearchParams()
    chosen.forEach(({ name }) => params.append('specialization', name))
    params.append('exp_level', experience)

    try {
      const { data } = await axios.get('http://127.0.0.1:8000/api/jobs/', { params })
      const grouped = {}
      for (const site in data.links) {
        for (const spec in data.links[site]) {
          grouped[spec] = [...(grouped[spec] || []), ...data.links[site][spec]]
        }
      }
      setJobLinks(grouped)
    } catch {
      alert('Error fetching jobs.')
    } finally {
      setLoading(false)
    }
  }

  const handleFile = e => setFile(e.target.files[0])

  const uploadCv = async e => {
    e.preventDefault()
    if (!file) {
      return setMessage('No file selected.')
    }
    setCvLoading(true)

    const form = new FormData()
    form.append('cv', file)

    try {
      const res = await fetch('http://127.0.0.1:8000/api/upload-cv/', {
        method: 'POST',
        body: form
      })
      const data = await res.json()

      const updated = {}
      Object.entries(data.predicted_specializations).forEach(([site, specs]) => {
        updated[site] = { _open: true }
        specs.forEach(([name]) => {
          updated[site][name] = true
        })
      })
      setSelected(updated)
      setExperience(data.predicted_experience_level.toLowerCase())
      setMessage('Upload successful.')
    } 
    catch {
      setMessage('Failed to process CV.')
    } 
    finally {
      setCvLoading(false)
    }
  }

  return (
    <div className="container my-5">
      <h1 className="text-center mb-4">Find Jobs</h1>

      <form onSubmit={uploadCv} className="text-center mb-4">
        <input type="file" accept="application/pdf" onChange={handleFile} />
        <button className="btn btn-primary mx-2">Upload CV</button>
      </form>

      {message && <p className="text-center">{message}</p>}
      {cvLoading && <p className="text-center">Analyzing CV...</p>}

      <div className="mb-4 text-center">
        <h3>Experience Level</h3>
        <div className="btn-group">
          {['junior', 'mid', 'senior'].map(level => (
            <button
              key={level}
              type="button"
              className={`btn ${experience === level ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => updateExperience(level)}
            >
              {level.charAt(0).toUpperCase() + level.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="mb-4">
        <h3>Specializations</h3>
        <ul className="list-unstyled">
          {[...new Set(specs.map(s => s.site))].map(site => (
            <li key={site} className="mb-3 text-start">
              <span
                onClick={() => handleSiteClick(site)}
                style={{ cursor: 'pointer', fontWeight: 'bold', color: '#007bff' }}
              >
                {selected[site]?._open ? '▼' : '►'} {site}
              </span>
              {selected[site]?._open && (
                <div className="mt-2 p-3 border rounded bg-light">
                  <div className="row">
                    {specs
                      .filter(s => s.site === site)
                      .map((s, i) => (
                        <div key={i} className="col-6 col-md-4 mb-2">
                          <button
                            onClick={() => handleSpecClick(site, s.name)}
                            className={`btn ${selected[site]?.[s.name] ? 'btn-success' : 'btn-outline-success'} w-100`}
                          >
                            {s.name}
                          </button>
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>

      <button className="btn btn-success w-100" onClick={fetchJobs} disabled={loading}>
        {loading ? 'Loading...' : 'Find Job Links'}
      </button>

      {Object.keys(jobLinks).length > 0 && (
        <div className="mt-4">
          {Object.entries(jobLinks).map(([spec, urls]) => (
            <div key={spec} className="mb-4">
              <h4 className="text-center">{spec}</h4>
              <div className="d-flex flex-wrap justify-content-center">
                {urls.map((url, i) => (
                  <a key={i} href={url} target="_blank" rel="noopener noreferrer" className="btn btn-link m-2">
                    {url}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
