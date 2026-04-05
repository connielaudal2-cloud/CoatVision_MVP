# Netlify Frontend Checklist (CoatVision)

Use this when deploying the dashboard to Netlify.

## Environment Variables

Set these in **Netlify → Site Settings → Environment Variables**:

- `VITE_API_URL`: backend external URL (e.g., `https://coatvision-mvp-lyxvision.onrender.com`)
- `VITE_SUPABASE_URL`: `https://<project>.supabase.co`
- `VITE_SUPABASE_ANON_KEY`: Supabase anon key (frontend-safe)

## Build Settings

In **Netlify → Site Settings → Build & Deploy**:

- **Base directory**: `frontend` (or `coatvision-app` if deploying the app folder)
- **Build command**: `npm ci && npm run build`
- **Publish directory**: `dist`

## Post-Deploy Checks

- Open the Netlify URL and confirm API calls hit `VITE_API_URL`
- Check CORS on the backend allows your Netlify domain (e.g., `https://<site>.netlify.app`)
- Verify Supabase auth redirect URLs include the Netlify domain

## Notes

- Do not expose `SUPABASE_SERVICE_ROLE_KEY` or `OPENAI_API_KEY` as frontend env vars
- For preview deploys, ensure backend CORS includes the preview URL pattern (`https://*--<site>.netlify.app`)
- Netlify redirects for SPA routing: add a `_redirects` file in the `public/` directory with `/* /index.html 200`
