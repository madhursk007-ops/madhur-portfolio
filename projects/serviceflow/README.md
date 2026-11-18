# ServiceFlow — IT Service Desk Prototype

A browser-based service-desk workflow demo for ticket intake, priority, requester, team ownership, status lifecycle and queue filtering.

## Run
Open `index.html` in a modern browser. No build step or dependencies required.

## Features
- Create service requests with requester, description, priority and assignee.
- Search and filter the ticket queue.
- Update tickets through Open, In Progress and Resolved.
- KPI counters for open, active, resolved and high-priority tickets.
- Browser localStorage persistence and resettable sample data.

## Scope and limitations
This is an independent front-end prototype inspired by common IT service-management workflows. It does not connect to Jira, Confluence, identity systems or an enterprise ticketing platform. Data is local to the browser; there is no authentication, shared database, notifications or SLA engine.

## Stack
HTML, CSS, JavaScript, localStorage.
