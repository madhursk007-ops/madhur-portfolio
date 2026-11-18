# OpsBoard — Operations Workflow Dashboard

A browser-based operations dashboard for initiative tracking, owners, due dates, status, progress and spreadsheet-friendly CSV exchange.

## Run
Open `index.html` in a modern browser. No build step or dependencies required.

## Features
- KPI summaries for total, in-progress, completed and overdue initiatives.
- Editable initiative status and progress.
- Add initiatives with owner and due date.
- Import CSV and export the current register to CSV.
- Average progress and status distribution summaries.
- Browser localStorage persistence and resettable sample data.

## CSV format
Required headers: `title,owner,due,status,progress`. Status values: Planned, In Progress, Completed.

## Scope and limitations
This is a standalone prototype demonstrating spreadsheet-style operational reporting. It is not integrated with Microsoft Excel, SharePoint, Power BI or Microsoft 365. Data remains in the browser; there is no multi-user access, authentication or server-side audit trail.

## Stack
HTML, CSS, JavaScript, localStorage, browser CSV import/export.
