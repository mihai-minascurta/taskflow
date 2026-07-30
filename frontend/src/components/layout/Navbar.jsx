import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <header className="navbar">
      <Link to="/dashboard" className="navbar-brand">
        TaskFlow
      </Link>
      {user && (
        <div className="navbar-user">
          <span>{user.full_name}</span>
          <button className="btn btn-secondary btn-sm" onClick={logout}>
            Log out
          </button>
        </div>
      )}
    </header>
  )
}
