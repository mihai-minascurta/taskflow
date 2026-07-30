import { useState } from 'react'
import ErrorMessage from '../common/ErrorMessage'

export default function ProjectForm({ project, users, onSubmit, onCancel }) {
  const isEditing = Boolean(project)

  const [name, setName] = useState(project?.name || '')
  const [description, setDescription] = useState(project?.description || '')
  const [ownerId, setOwnerId] = useState(project?.owner_id || users[0]?.id || '')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    if (!name.trim()) {
      setError('Project name is required.')
      return
    }

    setSubmitting(true)
    setError('')
    try {
      await onSubmit({
        name: name.trim(),
        description: description.trim(),
        owner_id: Number(ownerId),
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="card modal-card" onClick={(e) => e.stopPropagation()}>
        <h2>{isEditing ? 'Edit Project' : 'New Project'}</h2>
        <ErrorMessage message={error} />
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="project-name">
              Name
            </label>
            <input
              id="project-name"
              className="form-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoFocus
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="project-description">
              Description
            </label>
            <textarea
              id="project-description"
              className="form-textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="project-owner">
              Owner
            </label>
            <select
              id="project-owner"
              className="form-select"
              value={ownerId}
              onChange={(e) => setOwnerId(e.target.value)}
            >
              {users.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.full_name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Saving…' : isEditing ? 'Save Changes' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
