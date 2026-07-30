export default function ProjectCard({ project, onOpen, onEdit, onDelete }) {
  return (
    <div className="card card-clickable project-card" onClick={() => onOpen(project)}>
      <h3>{project.name}</h3>
      <p>{project.description || 'No description provided.'}</p>
      <div className="project-card-meta">
        <span>Owner: {project.owner_name || 'Unknown'}</span>
        <span>{project.task_count} task{project.task_count === 1 ? '' : 's'}</span>
      </div>
      <div
        className="project-card-actions"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="btn btn-secondary btn-sm" onClick={() => onEdit(project)}>
          Edit
        </button>
        <button className="btn btn-danger btn-sm" onClick={() => onDelete(project)}>
          Delete
        </button>
      </div>
    </div>
  )
}
