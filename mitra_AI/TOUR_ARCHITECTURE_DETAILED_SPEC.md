# TOUR_ARCHITECTURE_DETAILED_SPEC.md - Tour Guide Architecture Specification

This document provides a detailed layout of the architecture, reactive state boundaries, positioning calculation engine, and modal lifecycle event coordination for the Mitra AI Tour Guide system.

---

## 1. Architectural Core

The Tour Guide system uses a decoupled, event-driven state pattern to isolate the tour's control overlays from React page renders and next-themes transitions.

```
       [ Zustand State Store (useTourStore) ]
                         |
           (Controls active step index)
                         |
                         v
       [ TourGuide Controller Component ] <---- [ MASTER_TOUR_STEPS ]
                         |
      +------------------+------------------+
      |                                     |
      v                                     v
[ Spotlight Overlay Mask ]         [ Popover Card Component ]
 (Mix-blend SVG overlay)            (Rendered adjacent to target)
      |                                     |
      v                                     v
[ Target element highlighting ]     [ Custom visual mini-mockup previews ]
 (Center auto-scroll viewport)       (dialog fields, cards, sidebar list)
```

---

## 2. Decoupled Theme & Overlay Isolation

* **Theme Class Observation**: A `MutationObserver` targets the `class` attribute of `document.documentElement`. Changes triggered by the sidebar's theme toggle are captured in real-time, allowing the popover card to swap light/dark CSS classes without unmounting or resetting the tour state.
* **Double-Backdrop Suppression**: When a dialog opens, the tour spotlight serves as the primary dimming overlay. To prevent double-backdrop stacking, the Radix dialog component is modified to check an optional `isTourActive` prop. When true, the native overlay background is set to `bg-transparent backdrop-blur-none pointer-events-none`, passing click triggers directly to the underlying spotlight mask.

---

## 3. Position Calculation Engine (Middleware Specification)

All coordinates are calculated relative to the target element's bounding rect:

$$\text{Target} = \{ \text{top}, \text{bottom}, \text{left}, \text{right}, \text{width}, \text{height} \}$$

### Positioning Middlewares
1. **Offset**: Adds an explicit offset padding (16px for `nav-sidebar`, 12px for others) between the popover edge and target rect edge to prevent overlap.
2. **Flip Middleware**: Detects whether the calculated popover bounds cross the screen limits. If true, the system flips the direction (e.g. `bottom` $\leftrightarrow$ `top`, `left` $\leftrightarrow$ `right`).
3. **Shift Middleware**: Clamps coordinates so they stay within screen boundaries, using a `16px` safe margin:
   $$\text{Margin} \le \text{left} \le \text{window.innerWidth} - \text{popoverWidth} - \text{Margin}$$
   $$\text{Margin} \le \text{top} \le \text{window.innerHeight} - \text{popoverHeight} - \text{Margin}$$
4. **Dynamic Height Tracker**: Uses a `ResizeObserver` on `popoverRef` to track the exact height of the popover card, ensuring the clamping calculation is always accurate.

---

## 4. Modal Lifecycle & Route Transition Specification

* **Lifecycle Trigger**: Navigating steps or closing the tour invokes `closeAllModals()` in the store.
* **Event Broadcasting**: The store dispatches a custom window event:
  ```typescript
  window.dispatchEvent(new CustomEvent('mitra-tour-close-modals'))
  ```
* **Page Subscription**: Active modals on `/organizations`, `/projects`, and `/users` subscribe to this event and call their respective close handlers (e.g., setting `open` states to `false`). This guarantees clean route transitions without layout artifacts.

---

## 5. Directory & File Reference
* `frontend/src/config/tourConfig.ts`: Steps registry and user role helpers.
* `frontend/src/stores/tour.ts`: Zustand store for state management.
* `frontend/src/components/TourGuide.tsx`: Overlay mask and coordinate positioning calculation engine.
* `frontend/src/components/TourCard.tsx`: Previews and mini-mockups.
* `frontend/src/components/ui/dialog.tsx`: Dialog Content wrapper overlay override.
* `frontend/src/routes/__root.tsx`: Mount controller and auto-start check hook.
