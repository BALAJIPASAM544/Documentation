# TOUR_GLOBAL_ORIENTATION_LEVEL1.md - Level 1 Global Platform Orientation

This document outlines the high-level Level 1 Global Platform Orientation plan, designed to introduce all user roles (Super Admin, Admin, User) to the central layouts and dashboards of Mitra AI.

---

## 1. Role Scope Matrix

Level 1 orientation presents users with a curated sequence of steps showing the platform elements they are authorized to access:

| Role | Step Scope | Path Focus |
| :--- | :--- | :--- |
| **Super Admin** | 8 Steps | Navigation sidebar, Dashboard metrics, Findings grid, Output queue, tenant Organizations manager, Projects database, Create Project dialog, User Directory page. |
| **Admin** | 7 Steps | Navigation sidebar, Dashboard metrics, Findings grid, Output queue, Projects database, Create Project dialog, User Directory page. |
| **User** | 7 Steps | Navigation sidebar, Dashboard metrics, Findings grid, Output queue, User assigned projects cards, Archive uploads page, Project analysis overview, SVG Topology map. |

---

## 2. Step Sequence Matrix

### Step 1: persistent Sidebar
* **Target Selector**: `[data-tour="nav-sidebar"]`
* **Route**: `/dashboard`
* **Focus**: Persistent navigation menu options (Dashboard, Organizations, Projects, User Management). The highlighted area automatically resizes depending on the options visible to the user's role.
* **Placement**: `right-start` (offset `16px`).

### Step 2: Dashboard Overview
* **Target Selector**: `[data-tour="metric-overview"]`
* **Route**: `/dashboard`
* **Focus**: Telemetry counters (total uploaded projects, source code configurations, flow counts, open issues).
* **Placement**: `bottom` (offset `12px`).

### Step 3: Representative Flows & Findings
* **Target Selector**: `[data-tour="findings-section"]`
* **Route**: `/dashboard`
* **Focus**: Flow inventories, severity listings, XML warnings, and unresolved configurations.
* **Placement**: `top` (offset `12px`).

### Step 4: Live Analysis Output
* **Target Selector**: `[data-tour="analysis-drawer"]`
* **Route**: `/dashboard`
* **Focus**: Popped-out analysis queue tracking extraction pipelines, and the **Open report** button.
* **Placement**: `left` (offset `12px`).

### Step 5: Customer Tenants (Super Admin Only)
* **Target Selector**: `[data-tour="org-header-row"]`
* **Route**: `/organizations`
* **Focus**: Organizations directory header, governing client accounts, active domains, and tenant status.
* **Placement**: `bottom` (offset `12px`).

### Step 6: Projects Portfolio (Super Admin / Admin Only)
* **Target Selector**: `[data-tour="project-header-row"]`
* **Route**: `/projects`
* **Focus**: Projects workspace header, tracking engaged projects, and completion percentages.
* **Placement**: `bottom` (offset `12px`).

### Step 7: Create Project Engagement (Super Admin / Admin Only)
* **Target Selector**: `[data-tour="project-create-btn"]`
* **Route**: `/projects`
* **Focus**: Project setup trigger to allocate resources and set AWS targets.
* **Placement**: `bottom-start` (offset `12px`).

### Step 8: User Directory Title (Super Admin / Admin Only)
* **Target Selector**: `[data-tour="user-header-row"]`
* **Route**: `/users`
* **Focus**: User directory workspace, auditing credentials, project groups, and roles.
* **Placement**: `bottom` (offset `12px`).

### Step 9: Invite New User (Super Admin / Admin Only)
* **Target Selector**: `[data-tour="user-create-btn"]`
* **Route**: `/users`
* **Focus**: Button trigger to launch the user provisioning configuration dialog.
* **Placement**: `bottom-start` (offset `12px`).

### Step 10: Access Control Table (Super Admin / Admin Only)
* **Target Selector**: `[data-tour="user-table-header"]`
* **Route**: `/users`
* **Focus**: Table header row of active user listings, deactivation hooks, and access configurations.
* **Placement**: `top` (offset `12px`).

### Step 11: Assigned Projects (User Only)
* **Target Selector**: `[data-tour="project-header-row"]`
* **Route**: `/projects`
* **Focus**: User projects workspace list to launch their migrations.
* **Placement**: `bottom` (offset `12px`).

### Step 12: Code Archive Dropzone (User Only)
* **Target Selector**: `[data-tour="project-upload-dropzone"]`
* **Route**: `/migration/uploads`
* **Focus**: ZIP package upload dropzone (up to 50MB) to start flow analysis.
* **Placement**: `bottom-start` (offset `12px`).

### Step 13: Project Analysis Workspace (User Only)
* **Target Selector**: `[data-tour="project-analysis-view"]`
* **Route**: `/migration/analysis`
* **Focus**: Flow inventories, scores, and dependency charts.
* **Placement**: `bottom` (offset `12px`).

### Step 14: System Topology (User Only)
* **Target Selector**: `[data-tour="project-architecture-map"]`
* **Route**: `/migration/architecture`
* **Focus**: SVG system topology diagram and export tools.
* **Placement**: `bottom` (offset `12px`).
