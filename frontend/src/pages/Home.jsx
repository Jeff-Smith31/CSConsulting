import React from 'react'
import { Link } from 'react-router-dom'

export default function Home() {
  React.useEffect(() => {
    const els = document.querySelectorAll('.reveal')
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) e.target.classList.add('visible')
      })
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 })
    els.forEach(el => obs.observe(el))
    return () => obs.disconnect()
  }, [])

  return (
    <>
      <section className="hero">
        <div className="reveal visible">
          <img src={new URL('../assets/logo.svg', import.meta.url).href} alt="CodeSmith Consulting logo" className="hero-logo" />
          <h1 className="gradient-text">Website Development, Cloud, and Data — Done Right</h1>
          <p>We build fast, modern websites and custom software, backed by scalable cloud and pragmatic data solutions. Optional hosting available.</p>
          <div className="cta">
            <Link className="button" to="/services">Explore Services</Link>
            <Link className="button button-outline" to="/signup">Get Started</Link>
          </div>
        </div>
      </section>

      <section className="section">
        <h2 className="section-title reveal">Why CodeSmith</h2>
        <div className="grid">
          <div className="card reveal">
            <h3>Outcome-Focused</h3>
            <p>We align engineering with your business goals to deliver measurable results.</p>
          </div>
          <div className="card reveal">
            <h3>Cloud-Native</h3>
            <p>AWS-first architectures with security, reliability, and cost in mind.</p>
          </div>
          <div className="card reveal">
            <h3>Pragmatic Delivery</h3>
            <p>Small, iterative releases that reduce risk and build momentum.</p>
          </div>
        </div>
      </section>

      <section className="section section-alt">
        <h2 className="section-title reveal">Website Development</h2>
        <div className="grid">
          <div className="card reveal"><h3>Modern, Responsive Sites</h3><p>From marketing sites to client portals — fast, accessible, SEO-friendly, and easy to maintain.</p></div>
          <div className="card reveal"><h3>Custom Web Apps</h3><p>React frontends and Python backends tailored to your workflow with secure auth and payments.</p></div>
          <div className="card reveal"><h3>Optional Managed Hosting</h3><p>We can host and manage your site with monitoring, backups, and SSL so you don’t have to.</p></div>
        </div>
      </section>

      <section className="section">
        <h2 className="section-title reveal">See Our Work</h2>
        <p className="section-muted reveal">Explore a few of our public projects and collaborations.</p>
        <div className="grid">
          <div className="card reveal">
            <h3>jeffrey-smith-dev.com</h3>
            <p>A personal developer portfolio showcasing projects and skills.</p>
            <a className="button button-outline" href="https://jeffrey-smith-dev.com" target="_blank" rel="noreferrer">Visit site</a>
          </div>
          <div className="card reveal">
            <h3>Mel's Super Awesome Wedding Photography</h3>
            <p>Photography website highlighting beautiful wedding moments.</p>
            <a className="button button-outline" href="http://melssuperawesomeweddingphotographywebsite.com/" target="_blank" rel="noreferrer">Visit site</a>
          </div>
        </div>
      </section>

      <section className="section section-alt">
        <h2 className="section-title reveal">What You Get</h2>
        <div className="grid">
          <div className="card reveal"><h3>Performance</h3><p>Core Web Vitals, accessibility, SEO, and speed baked in.</p></div>
          <div className="card reveal"><h3>Security</h3><p>Best practices for auth, headers, rate limiting, and data protection.</p></div>
          <div className="card reveal"><h3>Ownership</h3><p>Clear handoff with docs, or have us manage it for you with hosting.</p></div>
        </div>
      </section>

      <section className="section">
        <h2 className="section-title reveal">By the Numbers</h2>
        <div className="grid">
          <div className="card reveal"><h3 className="stat">95%+</h3><p>Lighthouse performance on typical builds</p></div>
          <div className="card reveal"><h3 className="stat">99.9%</h3><p>Target uptime with managed hosting</p></div>
          <div className="card reveal"><h3 className="stat">1–2 weeks</h3><p>Typical MVP turnaround</p></div>
        </div>
      </section>

      <section className="section cta-banner reveal">
        <h3>Ready to move fast?</h3>
        <p className="section-muted">Kick off your project with a focused discovery and an MVP in as little as 1–2 weeks.</p>
        <div className="cta">
          <a className="button" href="/contact">Start the conversation</a>
          <a className="button button-outline" href="/services">See services</a>
        </div>
      </section>
    </>
  )
}
