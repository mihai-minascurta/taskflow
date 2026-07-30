import { useState } from 'react'
import CommentSection from './CommentSection'

const STATUS_OPTIONS = [
  { value: 'todo', label: 'To Do' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'done', label: 'Done' },
]

export default function TaskItem({ task, onStatusChange, onEdit, onDelete }) {
  const [showComments, setShowComments] = useState(false)

  return (
    <div className="task-card">
      <p className="task-card-title">{task.title}</p>
      {task.description && <p className="task-card-desc">{task.description}</p>}

      <div className="task-card-meta">
        <span className={`badge badge-${task.priority}`}>{task.priority}</span>
        {task.assignee_name && <span>Assigned: {task.assignee_name}</span>}
        {task.due_date && <span>Due: {task.due_date}</span>}
      </div>

      <div className="task-card-actions">
        <select
          className="form-select"
          value={task.status}
          onChange={(e) => onStatusChange(task, e.target.value)}
        >
          {STATUS_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        <div>
          <button
            className="btn-link"
            onClick={() => setShowComments((v) => !v)}
            style={{ marginRight: '0.6rem' }}
          >
            {showComments ? 'Hide' : `Comments (${task.comment_count})`}
          </button>
          <button className="btn-link" onClick={() => onEdit(task)} style={{ marginRight: '0.6rem' }}>
            Edit
          </button>
          <button
            className="btn-link"
            style={{ color: 'var(--color-danger)' }}
            onClick={() => onDelete(task)}
          >
            Delete
          </button>
        </div>
      </div>

      {showComments && <CommentSection taskId={task.id} />}
    </div>
  )
}
