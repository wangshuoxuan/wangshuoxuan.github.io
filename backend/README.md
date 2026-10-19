# Private services activation

Status: **not connected**. The published configuration has `enabled: false`.
No visitor events or private messages are collected while disabled. No demo counts are shown.

## Activation

1. Sign in at https://supabase.com/dashboard using the owner's account. Create a **free** project; do not enter a payment method or upgrade. The owner chooses and stores the database password.
2. Run `setup.sql` once in a fresh project's SQL editor. Existing database objects are not deleted by this script. It is intentionally not a rerunnable migration.
3. Enable email sign-in. Configure the Auth site URL as `https://wangshuoxuan.github.io` and allow the precise post and `/admin/insights.html` redirect URLs. Use Supabase's documented implicit magic-link flow, or configure a tested custom SMTP provider before inviting readers. Built-in email delivery has strict rate limits and is not suitable for an unrestricted public launch.
4. Place only the project URL and its browser-safe **legacy anon JWT** in `docs/services-config.js`. This client uses the anon JWT as the anonymous Authorization bearer; do not substitute a secret or service-role key. Do not enable yet.
5. Temporarily test the configured service on an isolated local copy with allowed local redirect URLs. Sign in as the owner. From Supabase Auth > Users, verify the owner's UUID. Add that UUID to `private.site_admins` in the SQL editor. Never make an email supplied by a reader or an editable profile field confer administrator access.
6. Create two separate reader test accounts A and B, and the owner account. Use the API directly as well as the UI: A must see only A's messages and replies; B must see only B's; anonymous access must return no messages; no reader may set ownership, timestamps, or replies; A/B/anonymous may not read `site_visits` or `site_dashboard`; the owner must see both readers' messages and the dashboard. Attempt requests without the UI's post-path filter too. **Do not enable unless all pass.** Record outcomes without saving tokens.
7. Verify magic-link sign-in, expired-token handling, owner replies, analytics updates, and cross-origin access against the actual site. Add a brief public privacy notice about anonymous aggregate analytics, active-time estimation, third-party storage, and message visibility before enabling. Leave message text/email out of all analytics events.
8. Set `enabled: true`, rebuild, and publish only after these checks. Current disabled code is preparatory, not a live privacy guarantee for a configured project that has not passed testing.

## Access model

Messages live in Supabase, never GitHub. PostgreSQL RLS restricts SELECT to the authenticated author or the allowlisted owner. Column grants prevent readers inserting an owner UUID, reply, or timestamp, and prevent them updating reply fields. Admin replies use a separate owner-only UPDATE policy. Owner allowlist is in a non-exposed schema. All statistics SELECT operations and the aggregate RPC require owner authorization at the database.

The administration page's HTML/JavaScript is public, as on any static site. Its **data** is private. No owner password, token, or service-role key belongs in the repository. Authentication sessions are tab-scoped, expire, and are not analytics identifiers. Clear sessions when using a shared computer.

## Measurements and limits

Prepared dashboard: whole-site page views, estimated sessions, per-page views/sessions, active visible time, maximum scroll depth, 90%-scroll completion, Beijing-date daily traffic, referrer hostname, and broad device type. Active time stops when hidden, unfocused, or idle for 90 seconds; a five-second timer and thirty-second upload make it approximate. No keystroke values, text content, query strings, full referrer URLs, precise locations, session replay, or IP addresses are stored by this application. Hosting providers can maintain their own infrastructure logs.

An anonymous session is tab-scoped and reused for up to thirty minutes between page visits. It is **not** a count of verified people. Reopening tabs, blockers, dropped final uploads, browser throttling, and spam can change estimates. The event endpoint is public and bounded but not abuse-proof; a public launch needs provider limits, monitoring, a retention/deletion schedule, and anti-spam measures appropriate to traffic. Supabase free-tier database/email quotas and regional accessibility must be checked live.

Reader message retrieval currently shows the latest 100 messages for the article. Owner inbox paginates 50 at a time. The dashboard aggregates on the server for 7/30/90-day ranges. Reading counts are not shown to public visitors. Readers can only see their own messages and owner replies after signing in; changing browsers requires signing in to the same account.

## Current blocker

The Supabase registration page did not load in the user's Edge session; a direct local HTTPS check also failed to establish SSL. No project or accounts have been provisioned, and no multi-account database isolation tests have run. Do not claim analytics or private messaging are active.
