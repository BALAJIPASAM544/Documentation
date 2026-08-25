# Unified, Role-Gated Tour Guide System

This document explains the files, folders, and layout changes added to implement the unified, role-gated Tour Guide system in **Mitra AI**.

## 1. Newly Added Files & Directories

Three new files were introduced under the `frontend/src/` folder tree.

### `src/config/tourConfig.ts`

**Role:** Configures the master tour step registry and tour metadata.

**Details:**
- Contains the `MASTER_TOUR_STEPS` configuration.
- Defines explicit target selectors for tour steps.
- Defines popover placement for each step.
- Supports custom visual previews.
- Provides helper functions such as:
  - `normalizeRole`
  - `getStepsForRole`
- Filters tour steps based on user roles:
  - Super Admin
  - Admin
  - User

### `src/components/TourCard.tsx`

**Role:** Renders custom visual previews inside tour popover cards.

**Details:**
- Contains reusable React components for tour previews.
- Includes mini mockups that visually demonstrate UI elements and workflows.
- Examples include:
  - Sidebar navigation
  - Project files dropdown
  - User modal fields

### `src/routes/users/index.tsx`

**Role:** Provides route mapping for `/users`.

**Details:**
- Re-exports and renders the `UserManagementPage` component.
- Adds the `/users` route.
- Resolves TanStack Router redirect loops during tour step navigation.

---

## 2. Modified Existing Core Tour Files

### `src/components/TourGuide.tsx`

**Role:** Main React component responsible for highlighting tour targets and rendering tour popovers.

**Changes:**
- Implemented automatic scrolling using:
  ```ts
  element.scrollIntoView({
    behavior: 'smooth',
    block: 'center'
  })
