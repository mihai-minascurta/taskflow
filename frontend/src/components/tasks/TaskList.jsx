import TaskItem from './TaskItem'

const COLUMNS = [
  { status: 'todo', title: 'To Do' },
  { status: 'in_progress', title: 'In Progress' },
  { status: 'done', title: 'Done' },
]

export default function TaskList({ tasks, onStatusChange, onEdit, onDelete }) {
  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        No tasks in this project yet. Add the first one to get moving.
      </div>
    )
  }

  return (
    <div className="task-board">
      {COLUMNS.map((col) => {
        const columnTasks = tasks.filter((t) => t.status === col.status)
        return (
          <div className="task-column" key={col.status}>
            <div className="task-column-header">
              <h3>{col.title}</h3>
              <span className="task-count">{columnTasks.length}</span>
            </div>
            {columnTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onStatusChange={onStatusChange}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))}
          </div>
        )
      })}
    </div>
  )
}
