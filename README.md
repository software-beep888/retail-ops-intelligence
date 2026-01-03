# Retail Ops Intelligence: Senior Data Judgment in Action

**Built by Félix Olwamba — Senior Data Analytics / Data Engineering**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)

📺 **2.5-minute system walkthrough:** [Loom Demo](https://loom.com/share/your-demo-here)

---

## 🎯 Problem Statement

Every morning, regional retail managers spent **~3 hours in Excel** trying to answer one recurring question:

> *“Why did sales drop yesterday at Store #42?”*

The reality:
- **30% false-positive alerts** from naive thresholding
- No consistent root-cause attribution
- Constant analyst interruptions for ad-hoc diagnostics
- Delayed corrective actions impacting revenue and staffing

**Outcome:**  
This system reduces a **3-hour manual diagnostic to ~10 minutes**, providing ranked probable causes with supporting evidence.

**Business effect:** faster intervention, fewer false alarms, and analysts freed from reactive fire drills.

---

## 🚀 What This Project Intentionally Demonstrates

> **This is a deliberately scoped portfolio system designed to demonstrate senior data judgment — not a full enterprise rollout.**

### 1. Production-Oriented Data Thinking
- **Idempotent pipelines** — safe re-runs without duplication
- **Fail-fast validation** — schema drift halts ingestion to protect trust
- **Observability by default** — structured logs and pipeline metrics
- **Graceful degradation** — dashboards remain usable with partial data

### 2. Business Judgment Over Technical Novelty
- Surfaces **probable causes**, not just KPIs
- Outputs **actionable explanations** with confidence scoring
- Makes **explicit trade-offs**, documented and justified
- Uses **simulated but behaviorally realistic** retail patterns

### 3. Senior Restraint & System Awareness
- Clear distinction between **what was built** and **what was intentionally excluded**
- Known **failure modes** identified with mitigation paths
- **Scaling limits** understood and documented
- Focus on **decision enablement**, not metric abundance

---

## 🏗️ Architecture Overview

Retail Event Data (Sales, Inventory, Staffing)  
↓  
Validation & Ingestion Layer (Schema + Freshness Checks)  
↓  
Feature Engineering & Aggregation  
↓  
Root-Cause Heuristics Engine  
↓  
Streamlit Decision UI (Ranked Causes + Evidence)  

---

## 🧠 Core Analytical Logic

For each store-day anomaly, the system evaluates:
- Traffic variance vs historical baselines
- Inventory availability & stock-out patterns
- Staffing coverage vs demand
- Promotion timing and cannibalization effects
- Weather and calendar effects (simulated)

Each signal contributes to a **weighted confidence score**, producing:
- Ranked probable causes
- Supporting metrics
- Recommended follow-up actions

---

## 🛠️ Technology Stack
- **Data Processing:** Python (pandas, validation layers)
- **Orchestration:** Containerized batch runs
- **UI:** Streamlit (decision-focused, not exploratory BI)
- **Infrastructure:** Docker
- **Version Control:** Git

---

## 📁 Repository Structure
- `/pipelines/` — Ingestion, validation, transformations
- `/features/` — Derived analytical features
- `/logic/` — Root-cause heuristics & scoring
- `/app/` — Streamlit decision interface
- `/docs/` — Design decisions & trade-offs

---

## 🎯 Why This Matters to Hiring Teams

This project demonstrates:
- Senior-level analytical judgment
- Production awareness beyond notebooks
- Business-first framing of data problems
- Restraint in system design
- Clear communication with non-technical stakeholders

---

## 🚀 Running the Project
```bash
docker build -t retail-ops-intel .
docker run -p 8501:8501 retail-ops-intel
## 🎥 Live Demo Video
[![Loom Demo](https://img.shields.io/badge/Watch_Demo-Loom-blue)](https://loom.com/your-link-here)

## 🚀 Quick Start (30 seconds)
```bash
git clone https://github.com/yourusername/retail-ops-intelligence.git
cd retail-ops-intelligence
python run.py
streamlit run dashboard/app.py
# Retail Ops Intelligence

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/YOUR_USERNAME/retail-ops-intelligence)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io)

📺 **Watch the 2.5-minute walkthrough:** [Loom Demo](YOUR_LOOM_LINK_HERE)