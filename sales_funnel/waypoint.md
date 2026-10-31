# Sales Funnel: Waypoint

**Status (waypoint, 2026-10-31):** blocked, parked for later.

## Goal

Rebuild the database behind a Claude.ai artifact titled **"REIS Prospect Desk"**
(`https://claude.ai/artifact/YGYXTzJRD5iYQEJrFNBFyH`), owned by someone else.

## What's blocked

1. **Artifact read access.** The `Artifact` tool's `read` action requires the
   owner to grant access in the *original* session where the link was shared —
   that can't be approved from this session. The artifact has not been read.
2. **Browser fallback.** Tried to open the artifact in Chrome via the
   `claude-in-chrome` extension to inspect it in developer tools instead. The
   extension is not connected (not installed/running, or not logged into the
   same claude.ai account as this session).

## Caveat to keep in mind when resumed

Even once the page loads, it may not actually expose the underlying data:
- If it's a static HTML/JS artifact with data baked into the page source, dev
  tools (View Source, Network tab, `window.__data` style globals) should work.
- If it calls a live backend, we'd only see the API shape, not necessarily the
  full dataset — and reconstructing someone else's backend data from a
  frontend view may not be fully possible, depending on what it was built from.

## Next steps (when resumed)

1. Install/connect the Claude in Chrome extension, logged into the same
   claude.ai account as this session (https://claude.ai/chrome), restart
   Chrome if just installed.
2. Re-open `https://claude.ai/artifact/YGYXTzJRD5iYQEJrFNBFyH` in Chrome,
   inspect via dev tools (Elements, Sources, Network, Console) to find how
   the data is structured and sourced.
3. If the artifact owner is reachable, consider just asking them to share the
   artifact for edit/read access directly — likely faster and more complete
   than reverse-engineering it from the rendered page.
4. Extract/reconstruct whatever data is recoverable into a proper database
   schema here in `sales_funnel/`.
