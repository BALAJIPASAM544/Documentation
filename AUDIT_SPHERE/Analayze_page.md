
Task Title
Replace Evidence Preview with Evidence File Links in Analysis Results

Task Description
Update the **Analysis Result** page under the **Evidence** tab to display uploaded evidence as clickable file links instead of embedded previews.

Requirements
 After a user:
  1. Selects a zone.
  2. Reads the instructions.
  3. Uploads one or more evidence files.
  4. Clicks **Analyze Zone**.
The Analysis Result page should:
  Remove all existing image/video preview components.
  Display uploaded evidence as clickable links:
    * Evidence File 1
    * Evidence File 2
    * Evidence File 3
    * ...
  The links should work for all supported file types (e.g., **.jpg, .jpeg, .png, .mp4, .pdf**, etc.).
  The display should be independent of the file type; only the file link should be shown.

 Acceptance Criteria

 ✅ No image or video previews are displayed in the Evidence tab.
 ✅ Every uploaded evidence file is listed as a clickable link.
 ✅ Links are numbered sequentially based on upload order.
 ✅ Clicking a link opens or downloads the corresponding evidence file.
 ✅ The implementation works for all supported evidence file types.


This task title and description clearly communicate the UI change and provide actionable acceptance criteria for implementation.

Changes Implemented:

Removed evidence preview functionality from the Analysis Result page.
Replaced image/video/file preview cards with clickable evidence links.
Displayed uploaded evidence as sequential links:
Evidence File 1
Evidence File 2
...
Updated the View All evidence modal to display link-only entries instead of media previews.
Ensured the implementation is file type agnostic, supporting all uploaded evidence formats (e.g., .jpg, .jpeg, .png, .mp4, .pdf, etc.).
Removed obsolete video preview modal, related state management, and helper functions associated with media preview.


-------------------------------------------------------------------------------------------------
 UI Changes Required

1. Evidence File Link Styling

   * The "Evidence File 1" entry is currently displayed as a button.
   * Remove the button styling and display it as plain text.
   * Style it similar to the existing **"View Reference"** text link shown below it.

2. Audit Pagination

   * Update the pagination to display only a single page number at a time.
   * Remove the display of the second page number.
   * The displayed page number should update dynamically as the user navigates using the **Previous** and **Next** arrow buttons.


Outcome:

The Analysis Result page now presents uploaded evidence as simple, clickable links regardless of file type, resulting in a cleaner and more consistent user experience.


--------------------------------------------------------------------------------------
 Task: Fix Non-Working Evidence File Links

Issue

* In some audit zones, clicking the evidence file link does not open the uploaded file.
* Investigate the root cause and resolve the issue without making any unrelated UI or functional changes.

Changes Implemented

* Preserved the existing SAS token generation flow.
* Rebuilt a clean base URL using only the **scheme**, **host**, and **path** before generating a new SAS token.
* Returned the URL in the format:
  * `clean_base_url + ? + new_sas_token`
    instead of appending a new SAS token to the original URL.

Root Cause

* Some evidence URLs stored in the database already contained expired or existing query parameters.
* Appending a new SAS token to these URLs resulted in invalid links, preventing certain evidence files from opening.

Resolution

* The application now generates a fresh SAS token against a clean blob URL, ensuring that every evidence link is valid regardless of whether the stored database URL contains old query parameters.

Outcome

* Evidence file links now open correctly across all audit zones.
* No UI behavior or other application functionality was modified.

