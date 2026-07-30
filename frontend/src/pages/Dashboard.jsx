import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import * as projectsApi from '../api/projects'
import * as usersApi from '../api/users'
import ProjectList from '../components/projects/ProjectList'
import ProjectForm from '../components/projects/ProjectForm'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'

export default function Dashboard() {
  const navigate = useNavigate()

  const [projects, setProjects] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  // null = closed, 'new' = create form, a project object = edit form
  const [formState, setFormState] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    setError('')
    try {
      const [projectsData, usersData] = await Promise.all([
        projectsApi.listProjects(),
        usersApi.listUsers(),
      ])
      setProjects(projectsData)
      setUsers(usersData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleOpen(project) {
    navigate(`/projects/${project.id}`)
  }

  async function handleDelete(project) {
    const confirmed = window.confirm(
      `Delete project "${project.name}"? This will also delete all of its tasks and comments.`
    )
    if (!confirmed) return

    setError('')
    try {
      await projectsApi.deleteProject(project.id)
      setProjects((prev) => prev.filter((p) => p.id !== project.id))
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSubmit(payload) {
    if (formState === 'new') {
      const created = await projectsApi.createProject(payload)
      setProjects((prev) => [created, ...prev])
    } else {
      const updated = await projectsApi.updateProject(formState.id, payload)
      setProjects((prev) => prev.map((p) => (p.id === updated.id ? updated : p)))
    }
    setFormState(null)
  }

  if (loading) {
    return <LoadingSpinner label="Loading projects…" />
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Projects</h1>
          <p className="page-subtitle">All the projects your team is working on.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setFormState('new')}>
          + New Project
        </button>
      </div>

      <ErrorMessage message={error} />

      <ProjectList
        projects={projects}
        onOpen={handleOpen}
        onEdit={setFormState}
        onDelete={handleDelete}
      />

      {formState && (
        <ProjectForm
          project={formState === 'new' ? null : formState}
          users={users}
          onSubmit={handleSubmit}
          onCancel={() => setFormState(null)}
        />
      )}
    </div>
  )
}
