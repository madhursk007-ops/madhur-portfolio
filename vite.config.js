import { defineConfig } from 'vite';

// GitHub Pages serves this repository under /madhur-portfolio/.
// Other hosts (including Render) serve from the domain root.
const base = process.env.GITHUB_ACTIONS === 'true' ? '/madhur-portfolio/' : '/';

export default defineConfig({ base });
