import React from 'react'

export default function Services() {
  const services = [
    { title: 'Website Development', desc: 'Modern, responsive websites and portals — fast, accessible, SEO-friendly.' },
    { title: 'Optional Managed Hosting', desc: 'We can host and manage your site with SSL, monitoring, and backups.' },
    { title: 'Custom Software', desc: 'From MVPs to enterprise systems built to scale.' },
    { title: 'Cloud & DevOps', desc: 'AWS architecture, CI/CD, observability, and cost optimization.' },
    { title: 'Data & AI', desc: 'Data pipelines, analytics dashboards, and AI integrations.' },
  ]
  return (
    <section>
      <h2>Services</h2>
      <p className="section-muted">Need a website or web app? We can build it — and if you want, we can host it too.</p>
      <div className="grid">
        {services.map((s) => (
          <div className="card" key={s.title}>
            <h3>{s.title}</h3>
            <p>{s.desc}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
