-- TaskFlow demo/seed data
--
-- All three demo users share the password: password123
-- (hashed below with Werkzeug's scrypt algorithm to match backend/app/models/user.py)
--
-- Run with:
--   psql -U taskflow_user -d taskflow_db -f seed.sql
--
-- NOTE: safe to re-run — existing rows are cleared first.

BEGIN;

TRUNCATE TABLE task_comments, tasks, projects, users RESTART IDENTITY CASCADE;

-- ---------------------------------------------------------------------------
-- users
-- ---------------------------------------------------------------------------
INSERT INTO users (username, email, password_hash, full_name) VALUES
('jsmith',  'jsmith@taskflow.local',  'scrypt:32768:8:1$xB2Vm4m5IdsB5ib6$d4e58f1d3c96e2fa66b334a32ce6283ad9aa615689674480c136932c3ccef9beba5dc40310d21c9de13a7a31ebe42833b77ae79b5d276ef5febaf19770b409d1', 'Jamie Smith'),
('agarcia', 'agarcia@taskflow.local', 'scrypt:32768:8:1$xB2Vm4m5IdsB5ib6$d4e58f1d3c96e2fa66b334a32ce6283ad9aa615689674480c136932c3ccef9beba5dc40310d21c9de13a7a31ebe42833b77ae79b5d276ef5febaf19770b409d1', 'Alex Garcia'),
('mchen',   'mchen@taskflow.local',   'scrypt:32768:8:1$xB2Vm4m5IdsB5ib6$d4e58f1d3c96e2fa66b334a32ce6283ad9aa615689674480c136932c3ccef9beba5dc40310d21c9de13a7a31ebe42833b77ae79b5d276ef5febaf19770b409d1', 'Morgan Chen');

-- ---------------------------------------------------------------------------
-- projects
-- ---------------------------------------------------------------------------
INSERT INTO projects (name, description, owner_id) VALUES
('Website Redesign',       'Refresh the marketing site with the new brand guidelines.', 1),
('Mobile App Launch',      'Ship v1.0 of the companion mobile app to the app stores.', 2),
('Internal Tools Cleanup', 'Consolidate and document internal scripts and dashboards.', 3);

-- ---------------------------------------------------------------------------
-- tasks
-- ---------------------------------------------------------------------------
INSERT INTO tasks (project_id, title, description, status, priority, assigned_to, due_date) VALUES
(1, 'Audit current site content',        'Go through every page and flag outdated copy.',         'done',        'medium', 1, '2026-06-10'),
(1, 'Design new homepage layout',         'Create hi-fi mockups in Figma for review.',              'in_progress', 'high',   2, '2026-07-05'),
(1, 'Implement responsive navbar',        'Build the new nav component with mobile menu support.', 'todo',        'medium', 3, '2026-08-01'),
(1, 'Set up analytics tracking',          'Add event tracking for key CTAs.',                       'todo',        'low',    1, '2026-08-15'),
(2, 'Finalize onboarding flow',           'Reduce onboarding to 3 screens max.',                    'in_progress', 'high',   2, '2026-08-03'),
(2, 'Fix push notification bug',          'Notifications are duplicated on Android.',               'todo',        'high',   3, '2026-07-31'),
(2, 'Prepare App Store listing',          'Screenshots, description, and keywords.',                'todo',        'medium', 2, '2026-08-20'),
(3, 'Document deployment scripts',        'Write down what each ad-hoc script actually does.',      'in_progress', 'medium', 3, '2026-08-10'),
(3, 'Consolidate cron jobs',              'Merge overlapping scheduled jobs into one runner.',      'todo',        'low',    1, '2026-09-01'),
(3, 'Remove unused internal dashboard',   'Confirm nobody uses the old reporting dashboard, then archive it.', 'todo', 'low', 3, NULL);

-- ---------------------------------------------------------------------------
-- task_comments
-- ---------------------------------------------------------------------------
INSERT INTO task_comments (task_id, user_id, comment) VALUES
(1, 1, 'Finished the audit — spreadsheet is in the shared drive.'),
(2, 2, 'First draft is up for review, feedback welcome.'),
(2, 1, 'Looks great, just tweak the hero spacing on mobile.'),
(5, 2, 'Down to 3 screens now, testing with a few users this week.'),
(6, 3, 'Repro''d it on Pixel 6 — looks like a duplicate FCM listener.'),
(8, 3, 'About halfway through documenting the backup script.');

COMMIT;
