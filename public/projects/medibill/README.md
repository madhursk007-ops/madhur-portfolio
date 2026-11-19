# MediBill — Pharmacy Billing Suite

MediBill is an offline-first browser prototype for a pharmacy. It includes billing, UPI QR generation, inventory/batch tracking, bill history, insights, purchases, GST summaries, sales reports and settings.

## Run
Open `index.html` through a local static server or deploy the folder to a static host. It can be installed as a PWA in supported browsers. `manifest.json` and `sw.js` provide the install/offline shell.

## Desktop
For a Windows desktop package, use a trusted Electron build pipeline around this static app. This repository includes the PWA version; a signed installer and auto-update channel are not configured.

## Important limitations
- Data is stored in browser localStorage on the current device. It is not a shared multi-user database.
- UPI QR codes encode a UPI payment intent. The app does not verify bank settlement; staff must confirm payment manually.
- GST rates are configurable per product. The GST report is an operational summary, not a filed return or compliance certification.
- No pharmacy dispensing, prescription validation, controlled-drug register or statutory audit workflow is provided.
- Before live business use, add secure authentication, hosted database, server-side validation, audit logs, encrypted backups, batch-level costing, payment-gateway reconciliation, tested tax rules and professional compliance review.

This is a prototype, not a replacement for a certified accounting or pharmacy management system.
