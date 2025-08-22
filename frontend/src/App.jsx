import React from 'react'
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import logo from './assets/logo.svg'
import avatarDefault from './assets/avatar-default.svg'
import { useAuth } from './auth.jsx'

export default function App() {
  const { token, user, logout } = useAuth()
  const navigate = useNavigate()
  const loc = useLocation()
  const [menuOpen, setMenuOpen] = React.useState(false)
  const [mobileOpen, setMobileOpen] = React.useState(false)
  const menuRef = React.useRef(null)

  React.useEffect(() => { setMenuOpen(false); setMobileOpen(false) }, [loc.pathname])

  const isAdmin = !!(user && user.is_admin)
  const initial = user?.name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase()

  React.useEffect(() => {
    const el = document.querySelector('.site-header')
    const onScroll = () => {
      if (!el) return
      if (window.scrollY > 4) el.classList.add('scrolled')
      else el.classList.remove('scrolled')
    }
    onScroll()
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  React.useEffect(() => {
    function onDocClick(e) {
      if (!menuRef.current) return
      if (!menuRef.current.contains(e.target)) setMenuOpen(false)
    }
    function onKey(e) { if (e.key === 'Escape') { setMenuOpen(false); setMobileOpen(false) } }
    document.addEventListener('mousedown', onDocClick)
    document.addEventListener('touchstart', onDocClick)
    window.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onDocClick)
      document.removeEventListener('touchstart', onDocClick)
      window.removeEventListener('keydown', onKey)
    }
  }, [])

  return (
    <div>
      <header className="site-header">
        <div className="container header-inner">
          <div className="brand" onClick={() => navigate('/') }>
            <img src={logo} alt="CodeSmith Consulting" />
            <span>CodeSmith Consulting</span>
          </div>
          <button className="hamburger" aria-label="Toggle menu" aria-controls="primary-nav" aria-expanded={mobileOpen} onClick={() => setMobileOpen(v=>!v)}>
            <span className={`bar ${mobileOpen ? 'open' : ''}`}></span>
            <span className={`bar ${mobileOpen ? 'open' : ''}`}></span>
            <span className={`bar ${mobileOpen ? 'open' : ''}`}></span>
          </button>
          <nav id="primary-nav" className={`nav-links ${mobileOpen ? 'open' : ''}`}>
            <Link to="/">Home</Link>
            <Link to="/services">Services</Link>
            <Link to="/about">About</Link>
            <Link to="/contact">Contact</Link>
            {token ? (
              <div className="profile-menu" ref={menuRef}>
                <button className="profile-button" onClick={() => setMenuOpen(v=>!v)} aria-haspopup="menu" aria-expanded={menuOpen}>
                  <span className="avatar">
                    {initial ? <span className="avatar-initial">{initial}</span> : <img src={avatarDefault} alt="profile" />}
                  </span>
                  <span className={`chevron ${menuOpen ? 'open' : ''}`}>▾</span>
                </button>
                {menuOpen && (
                  <div className="dropdown" role="menu">
                    <button className="dropdown-item" onClick={() => navigate('/dashboard')}>Dashboard</button>
                    <button className="dropdown-item" onClick={() => navigate('/profile')}>Profile</button>
                    <button className="dropdown-item" onClick={() => navigate('/account')}>Account</button>
                    {isAdmin && <button className="dropdown-item" onClick={() => navigate('/admin')}>Admin Dashboard</button>}
                    <div className="dropdown-sep" />
                    <button className="dropdown-item" onClick={() => { setMenuOpen(false); logout() }}>Logout</button>
                  </div>
                )}
              </div>
            ) : (
              <>
                {loc.pathname !== '/login' && <Link to="/login">Login</Link>}
                {loc.pathname !== '/signup' && <Link className="button get-started" to="/signup">Get Started</Link>}
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="container">
        <Outlet />
      </main>
      <footer className="site-footer">
        <div className="container">© {new Date().getFullYear()} CodeSmith Consulting, LLC</div>
      </footer>
    </div>
  )
}
