import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App'
import Home from './pages/Home'
import Services from './pages/Services'
import About from './pages/About'
import Contact from './pages/Contact'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import Root from './Root'
import './styles.css'
const Admin = React.lazy(() => import('./pages/Admin'))
const Profile = React.lazy(() => import('./pages/Profile'))
const Account = React.lazy(() => import('./pages/Account'))

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root><App /></Root>,
    children: [
      { index: true, element: <Home /> },
      { path: 'services', element: <Services /> },
      { path: 'about', element: <About /> },
      { path: 'contact', element: <Contact /> },
      { path: 'login', element: <Login /> },
      { path: 'signup', element: <Signup /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'profile', element: <React.Suspense fallback={null}><Profile /></React.Suspense> },
      { path: 'account', element: <React.Suspense fallback={null}><Account /></React.Suspense> },
      { path: 'admin', element: <React.Suspense fallback={null}><Admin /></React.Suspense> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
