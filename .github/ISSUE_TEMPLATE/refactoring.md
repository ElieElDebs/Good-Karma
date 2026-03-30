---
name: "🛠️ Refactoring / Technical Debt"
about: Suggest code improvements without changing functionality
title: "[REFACTOR] "
labels: ["refactor", "technical-debt"]
---

### 🎯 Objective
What is the main goal of this refactoring? (e.g., Simplifying the scoring logic, improving Next.js component reusability, or optimizing FastAPI middleware).

### 🔍 Area of Focus
Which part of the codebase is affected?
- [ ] `Morlana_frontend` (Next.js/React)
- [ ] `Morlana_backend` (FastAPI/Python logic)
- [ ] `Docker / Deployment` (Compose, Dockerfiles)
- [ ] `Database Layer` (Qdrant schemas/queries)

### ⚙️ Proposed Changes
Briefly describe the structural changes you want to make. 
*Example: "Extract the KPI calculation logic into a standalone utility class to make it easier to test."*

### 🚀 Benefits
How will this improve the project?
- [ ] **Maintainability:** Easier to read and modify.
- [ ] **Performance:** Faster execution or lower memory footprint.
- [ ] **Testability:** Makes it easier to write unit tests.
- [ ] **Scalability:** Better structure for adding future subreddits or features.

### ✅ Verification Plan
How will we ensure that **nothing broke**? 
*(Since refactoring shouldn't change behavior, this is the most important part!)*

### Additional Context
Link any related issues or technical debt discussions here.