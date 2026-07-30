from datetime import datetime, timezone

from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    owner = db.relationship("User")
    tasks = db.relationship(
        "Task", backref="project", cascade="all, delete-orphan", lazy="dynamic"
    )

    def to_dict(self, include_task_count: bool = True) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "owner_name": self.owner.full_name if self.owner else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_task_count:
            data["task_count"] = self.tasks.count()
        return data

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Project {self.name}>"
