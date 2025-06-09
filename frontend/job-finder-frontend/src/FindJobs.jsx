import React, { useEffect, useState } from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import { Spinner, Alert, Card, Accordion, Button } from 'react-bootstrap'

export default function FindJobs() {
  const [specs, setSpecs] = useState([])
  const [selected, setSelected] = useState({})
  const [experience, setExperience] = useState('')
  const [jobLinks, setJobLinks] = useState({})
  const [loading, setLoading] = useState(false)
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState({ text: '', variant: '' })
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

  const handleSpecClick = (site, name) =>
    setSelected(prev => ({
      ...prev,
      [site]: { ...prev[site], [name]: !prev[site]?.[name] }
    }))

  const fetchJobs = async () => {
    const chosen = Object.entries(selected).flatMap(([site, values]) =>
      Object.keys(values)
        .filter(key => key !== '_open' && values[key])
        .map(name => ({ site, name }))
    )
    
    if (!experience) {
      setMessage({ text: 'Please select an experience level', variant: 'danger' })
      return
    }
    
    if (!chosen.length) {
      setMessage({ text: 'Please select at least one specialization', variant: 'danger' })
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
      setMessage({ text: 'Error fetching jobs', variant: 'danger' })
    } finally {
      setLoading(false)
    }
  }

  const handleFile = e => setFile(e.target.files[0])

  const uploadCv = async e => {
    e.preventDefault()
    if (!file) {
      return setMessage({ text: 'No file selected', variant: 'danger' })
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
    } catch {
      setMessage({ text: 'Failed to process CV', variant: 'danger' })
    } finally {
      setCvLoading(false)
    }
  }

  return (
    <div className="container my-5" style={{ maxWidth: '900px' }}>
      <Card className="shadow-sm mb-4">
        <Card.Body className="text-center">
          <h1 className="mb-3" style={{ color: '#2c3e50' }}>Find Your Dream Job</h1>
          <p className="text-muted">
            Upload your CV or manually select your skills to get personalized job recommendations
          </p>
        </Card.Body>
      </Card>

      {message.text && (
        <Alert variant={message.variant} className="mb-4" dismissible onClose={() => setMessage({ text: '', variant: '' })}>
          {message.text}
        </Alert>
      )}

      <Card className="shadow-sm mb-4">
        <Card.Body>
          <h4 className="mb-3">Upload Your CV (Optional)</h4>
          <form onSubmit={uploadCv} className="d-flex align-items-center">
            <div className="flex-grow-1 me-3">
              <input 
                type="file" 
                accept="application/pdf" 
                onChange={handleFile} 
                className="form-control"
                id="cvUpload"
              />
            </div>
            <Button type="submit" variant="primary" disabled={cvLoading}>
              {cvLoading ? (
                <>
                  <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                  <span className="ms-2">Analyzing</span>
                </>
              ) : 'Upload CV'}
            </Button>
          </form>
          <small className="text-muted">We will automatically detect your skills and experience level</small>
        </Card.Body>
      </Card>

      <Card className="shadow-sm mb-4">
        <Card.Body className="text-center">
          <h4 className="mb-3">Experience Level</h4>
          <div className="d-flex flex-wrap gap-2 justify-content-center">
            {['junior', 'mid', 'senior'].map(level => (
              <Button
                key={level}
                variant={experience === level ? 'primary' : 'outline-primary'}
                onClick={() => setExperience(level)}
                className="text-capitalize"
              >
                {level}
              </Button>
            ))}
          </div>
        </Card.Body>
      </Card>

      <Card className="shadow-sm mb-4">
        <Card.Body>
          <h4 className="mb-3">Specializations</h4>
          
          <Accordion>
            {[...new Set(specs.map(s => s.site))].map(site => (
              <Accordion.Item eventKey={site} key={site}>
                <Accordion.Header>
                  <span className="fw-bold">{site}</span>
                </Accordion.Header>
                <Accordion.Body>
                  <div className="d-flex flex-wrap gap-2">
                    {specs
                      .filter(s => s.site === site)
                      .map((s, i) => (
                        <Button
                          key={i}
                          variant={selected[site]?.[s.name] ? 'primary' : 'outline-primary'}
                          onClick={() => handleSpecClick(site, s.name)}
                          className="text-nowrap"
                        >
                          {s.name}
                        </Button>
                      ))}
                  </div>
                </Accordion.Body>
              </Accordion.Item>
            ))}
          </Accordion>
        </Card.Body>
      </Card>

      <div className="d-grid mb-5">
        <Button 
          variant="primary" 
          size="lg" 
          onClick={fetchJobs} 
          disabled={loading}
          className="py-3"
        >
          {loading ? (
            <>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
              <span className="ms-2">Searching Jobs</span>
            </>
          ) : (
            'Find Matching Jobs'
          )}
        </Button>
      </div>

      {Object.keys(jobLinks).length > 0 && (
        <Card className="shadow-sm">
          <Card.Body>
            <h3 className="mb-4">Matching Jobs</h3>
            {Object.entries(jobLinks).map(([spec, urls]) => (
              <div key={spec} className="mb-4">
                <h5 className="mb-3">{spec}</h5>
                <ul className="list-group">
                  {urls.map((url, i) => (
                    <li key={i} className="list-group-item d-flex justify-content-between align-items-center">
                      <a href={url} target="_blank" rel="noopener noreferrer" className="text-truncate me-3">
                        {new URL(url).hostname.replace('www.', '')} - {spec}
                      </a>
                      <Button variant="outline-primary" size="sm" href={url} target="_blank">
                        View
                      </Button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </Card.Body>
        </Card>
      )}
    </div>
  )
}