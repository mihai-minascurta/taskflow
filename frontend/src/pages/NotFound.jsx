import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="login-page">
      <div className="card login-card" style={{ textAlign: 'center' }}>
        <h1 className="login-title">404</h1>
        <p className="login-subtitle">This page doesn't exist.</p>
        <Link to="/dashboard" className="btn btn-primary" style={{ justifyContent: 'center' }}>
          Back to dashboard
        </Link>
      </div>
    </div>
  )
}
