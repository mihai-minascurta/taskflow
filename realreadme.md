Real README - Rezumat compact al proiectului
===========================================

Scop
-----
Acest repo conține un frontend, un backend și fișiere de infrastructură. Eu am preluat rolul de DevOps: am primit frontend-ul, backend-ul și baza de date inițial, apoi le-am făcut funcționale, le-am containerizat și le-am migrat să ruleze pe AWS folosind Terraform + Kubernetes.

Ce folosește proiectul (pe scurt)
---------------------------------
- Frontend: Vite + React (folder `frontend`, `package.json`, `src/`)
- Backend: Python Flask (folder `backend`, `wsgi.py`, `requirements.txt`)
- DB schema & seed: `database/schema.sql`, `database/seed.sql`, plus `backend/seed.py`
- Containerizare: `Dockerfile` în `frontend/` și `backend/`
- Infra as Code: `terraform/` (module: `alb`, `cluster`, `rds`, `ebs-csi`, `iam`, `networking`, `workers`, etc.)
- Kubernetes manifests: `kubernetes/` (deployments, services, ingress, jobs/init-db)
- Monitoring: ServiceMonitor manifest în `kubernetes/monitoring`

Ce am făcut eu (DevOps summary)
-------------------------------
- Am creat și adaptat Terraform pentru AWS: provisionare EKS, RDS (DB gestionat de AWS), ALB, EBS CSI, IAM roles, rețea.
- Am construit/actualizat fișiere Kubernetes pentru a rula aplicațiile în EKS: `deployment/`, `service/`, `ingress/`, job pentru inițializare DB.
- Am definit pipeline-ul de image workflow (clădire push către ECR) și legătura cu manifestele K8s (deploy pe EKS).
- Am asigurat persistența și stocarea (EBS + CSI) și migrarea bazei de date către RDS (managed DB).
- Am adăugat job pentru seed/inițializare DB și health checks + monitoring (ServiceMonitor).

Cum folosesc (comenzi esențiale)
--------------------------------
Local (dev):
```bash
# Backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
FLASK_APP=backend/wsgi.py flask run

# Frontend
cd frontend
npm install
npm run dev

# Seed DB local
python backend/seed.py
```

Deploy pe AWS (rezumat):
```bash
# 1. Terraform: init + apply pentru provisioning infra (EKS, RDS, ALB, IAM etc.)
cd terraform
terraform init
terraform apply

# 2. Build & push Docker images -> ECR
# 3. kubectl apply -f kubernetes/deployment -n <namespace>
# 4. Rulez job init-db: kubectl apply -f kubernetes/jobs/init-db.yaml
```

Fișiere importante (unde găsești lucrurile)
-----------------------------------------
- Backend entry: [backend/wsgi.py](backend/wsgi.py)
- Backend code: [backend/app/](backend/app/)
- Frontend: [frontend/src/](frontend/src/)
- Terraform modules: [terraform/modules/](terraform/modules/)
- K8s manifests: [kubernetes/](kubernetes/)
- DB schema & seed: [database/schema.sql](database/schema.sql) și [database/seed.sql](database/seed.sql)

Note rapide
-----------
- DB este mutată la AWS RDS (managed) — am migrat schema/seed și am configurat acces din EKS.
- Ingress folosește ALB (module `alb` + controller) pentru expunere publică.
- Monitoring minimal prin `ServiceMonitor` pentru integrare Prometheus.
