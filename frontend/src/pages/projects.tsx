import { useState } from 'react'

export default function Projects() {
  const [projects, setProjects] = useState([
    { id: 1, name: 'Commercial Building', client: 'ABC Corp', status: 'Active' },
    { id: 2, name: 'Residential Tower', client: 'XYZ Developers', status: 'Design' },
  ])

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Projects</h1>
      </nav>

      <div className="container mx-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">All Projects</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">
            New Project
          </button>
        </div>

        <div className="grid gap-4">
          {projects.map(project => (
            <div key={project.id} className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-bold">{project.name}</h3>
                  <p className="text-gray-600">Client: {project.client}</p>
                </div>
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded">
                  {project.status}
                </span>
              </div>
              <div className="mt-4 flex gap-2">
                <button className="text-blue-600">Open</button>
                <button className="text-gray-600">Export</button>
                <button className="text-gray-600">Share</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
