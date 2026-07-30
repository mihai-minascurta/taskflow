import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import * as projectsApi from '../api/projects'
import * as tasksApi from '../api/tasks'
import * as usersApi from '../api/users'
import TaskList from '../components/tasks/TaskList'
import TaskForm from '../components/tasks/TaskForm'
import LoadingSpinner from '../components/common/LoadingSpinner'
import ErrorMessage from '../components/common/ErrorMessage'

export default function ProjectDetail() {
  const { id } = useParams()

  const [project, setProject] = useState(null)
  const [tasks, setTasks] = useState([])
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [actionError, setActionError] = useState('')
  // null = closed, 'new' = create form, a task object = edit form
  const [formState, setFormState] = useState(null)

  useEffect(() => {
    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  async function loadData() {
    setLoading(true)
    setLoadError('')
    try {
      const [projectData, tasksData, usersData] = await Promise.all([
        projectsApi.getProject(id),
        projectsApi.listProjectTasks(id),
        usersApi.listUsers(),
      ])
      setProject(projectData)
      setTasks(tasksData)
      setUsers(usersData)
    } catch (err) {
      setLoadError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleStatusChange(task, status) {
    setActionError('')
    try {
      const updated = await tasksApi.updateTask(task.id, { status })
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
    } catch (err) {
      setActionError(err.message)
    }
  }

  async function handleDelete(task) {
    const confirmed = window.confirm(`Delete task "${task.title}"?`)
    if (!confirmed) return

    setActionError('')
    try {
      await tasksApi.deleteTask(task.id)
      setTasks((prev) => prev.filter((t) => t.id !== task.id))
    } catch (err) {
      setActionError(err.message)
    }
  }

  async function handleSubmit(payload) {
    if (formState === 'new') {
      const created = await tasksApi.createTask(payload)
      setTasks((prev) => [created, ...prev])
    } else {
      const updated = await tasksApi.updateTask(formState.id, payload)
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
    }
    setFormState(null)
  }

  if (loading) {
    return <LoadingSpinner label="Loading project…" />
  }

  if (loadError || !project) {
    return (
      <div>
        <Link to="/dashboard" className="back-link">
          ← Back to projects
        </Link>
        <ErrorMessage message={loadError || 'Project not found.'} />
      </div>
    )
  }

  return (
    <div>
      <Link to="/dashboard" className="back-link">
        ← Back to projects
      </Link>

      <div className="page-header">
        <div>
          <h1>{project.name}</h1>
          <p className="page-subtitle">
            {project.description || 'No description provided.'} &middot; Owner:{' '}
            {project.owner_name || 'Unknown'}
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setFormState('new')}>
          + New Task
        </button>
      </div>

      <ErrorMessage message={actionError} />

      <TaskList
        tasks={tasks}
        onStatusChange={handleStatusChange}
        onEdit={setFormState}
        onDelete={handleDelete}
      />

      {formState && (
        <TaskForm
          task={formState === 'new' ? null : formState}
          users={users}
          projectId={project.id}
          onSubmit={handleSubmit}
          onCancel={() => setFormState(null)}
        />
      )}
    </div>
  )
}
