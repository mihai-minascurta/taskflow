"""
Seed the database with demo data using the ORM.

This is an alternative to running database/seed.sql directly with psql — use
whichever fits your workflow. Both produce equivalent data.

Usage (from the backend/ directory, with the virtualenv active and .env
configured):

    python seed.py
"""

import logging
from datetime import date

from app import create_app
from app.extensions import db
from app.models.comment import TaskComment
from app.models.project import Project
from app.models.task import Task
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")


def seed():
    app = create_app()

    with app.app_context():
        logger.info("Clearing existing data...")
        TaskComment.query.delete()
        Task.query.delete()
        Project.query.delete()
        User.query.delete()
        db.session.commit()

        logger.info("Creating users...")
        jsmith = User(username="jsmith", email="jsmith@taskflow.local", full_name="Jamie Smith")
        jsmith.set_password("password123")

        agarcia = User(username="agarcia", email="agarcia@taskflow.local", full_name="Alex Garcia")
        agarcia.set_password("password123")

        mchen = User(username="mchen", email="mchen@taskflow.local", full_name="Morgan Chen")
        mchen.set_password("password123")

        db.session.add_all([jsmith, agarcia, mchen])
        db.session.commit()

        logger.info("Creating projects...")
        website = Project(
            name="Website Redesign",
            description="Refresh the marketing site with the new brand guidelines.",
            owner_id=jsmith.id,
        )
        mobile = Project(
            name="Mobile App Launch",
            description="Ship v1.0 of the companion mobile app to the app stores.",
            owner_id=agarcia.id,
        )
        internal = Project(
            name="Internal Tools Cleanup",
            description="Consolidate and document internal scripts and dashboards.",
            owner_id=mchen.id,
        )
        db.session.add_all([website, mobile, internal])
        db.session.commit()

        logger.info("Creating tasks...")
        tasks = [
            Task(project_id=website.id, title="Audit current site content",
                 description="Go through every page and flag outdated copy.",
                 status="done", priority="medium", assigned_to=jsmith.id,
                 due_date=date(2026, 6, 10)),
            Task(project_id=website.id, title="Design new homepage layout",
                 description="Create hi-fi mockups in Figma for review.",
                 status="in_progress", priority="high", assigned_to=agarcia.id,
                 due_date=date(2026, 7, 5)),
            Task(project_id=website.id, title="Implement responsive navbar",
                 description="Build the new nav component with mobile menu support.",
                 status="todo", priority="medium", assigned_to=mchen.id,
                 due_date=date(2026, 8, 1)),
            Task(project_id=website.id, title="Set up analytics tracking",
                 description="Add event tracking for key CTAs.",
                 status="todo", priority="low", assigned_to=jsmith.id,
                 due_date=date(2026, 8, 15)),
            Task(project_id=mobile.id, title="Finalize onboarding flow",
                 description="Reduce onboarding to 3 screens max.",
                 status="in_progress", priority="high", assigned_to=agarcia.id,
                 due_date=date(2026, 8, 3)),
            Task(project_id=mobile.id, title="Fix push notification bug",
                 description="Notifications are duplicated on Android.",
                 status="todo", priority="high", assigned_to=mchen.id,
                 due_date=date(2026, 7, 31)),
            Task(project_id=mobile.id, title="Prepare App Store listing",
                 description="Screenshots, description, and keywords.",
                 status="todo", priority="medium", assigned_to=agarcia.id,
                 due_date=date(2026, 8, 20)),
            Task(project_id=internal.id, title="Document deployment scripts",
                 description="Write down what each ad-hoc script actually does.",
                 status="in_progress", priority="medium", assigned_to=mchen.id,
                 due_date=date(2026, 8, 10)),
            Task(project_id=internal.id, title="Consolidate cron jobs",
                 description="Merge overlapping scheduled jobs into one runner.",
                 status="todo", priority="low", assigned_to=jsmith.id,
                 due_date=date(2026, 9, 1)),
            Task(project_id=internal.id, title="Remove unused internal dashboard",
                 description="Confirm nobody uses the old reporting dashboard, then archive it.",
                 status="todo", priority="low", assigned_to=mchen.id,
                 due_date=None),
        ]
        db.session.add_all(tasks)
        db.session.commit()

        logger.info("Creating comments...")
        comments = [
            TaskComment(task_id=tasks[0].id, user_id=jsmith.id,
                        comment="Finished the audit — spreadsheet is in the shared drive."),
            TaskComment(task_id=tasks[1].id, user_id=agarcia.id,
                        comment="First draft is up for review, feedback welcome."),
            TaskComment(task_id=tasks[1].id, user_id=jsmith.id,
                        comment="Looks great, just tweak the hero spacing on mobile."),
            TaskComment(task_id=tasks[4].id, user_id=agarcia.id,
                        comment="Down to 3 screens now, testing with a few users this week."),
            TaskComment(task_id=tasks[5].id, user_id=mchen.id,
                        comment="Repro'd it on Pixel 6 — looks like a duplicate FCM listener."),
            TaskComment(task_id=tasks[7].id, user_id=mchen.id,
                        comment="About halfway through documenting the backup script."),
        ]
        db.session.add_all(comments)
        db.session.commit()

        logger.info(
            "Seed complete: %s users, %s projects, %s tasks, %s comments",
            User.query.count(), Project.query.count(), Task.query.count(),
            TaskComment.query.count(),
        )


if __name__ == "__main__":
    seed()
