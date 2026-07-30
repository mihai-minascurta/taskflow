import ProjectCard from './ProjectCard'

export default function ProjectList({ projects, onOpen, onEdit, onDelete }) {
  if (projects.length === 0) {
    return (
      <div className="empty-state">
        No projects yet. Create your first project to get started.
      </div>
    )
  }

  return (
    <div className="project-grid">
      {projects.map((project) => (
        <ProjectCard
          key={project.id}
          project={project}
          onOpen={onOpen}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
