# JR Captures website manager

Open `/admin` and sign in as `reegancaptures@gmail.com`. The owner creates the first password using a private, single-use setup code (or setup link). No password or setup secret is committed to this repository.

The panel supports products, categories, size options, pricing, courier charges, dispatch, display order, image upload, hide/show, removal and restoration. Product removals are recoverable through the Removed products filter. A hidden category hides its products too. All edits use optimistic version checks to prevent overwriting another browser's changes.

## Hosting and data

Cloudflare Pages advanced mode runs `_worker.js`. Bind a D1 database as `DB` in **production** and store a random 256-bit `ADMIN_SETUP_TOKEN` as an encrypted environment variable. Keep preview environments separate from production data. Set `fail_open=false` for the production function configuration.

Initialize a new database with `scripts/schema.sql`. `scripts/extract-catalog.py` creates the one-time migration input from the original HTML catalog. The initial import contains 127 grouped products, 14 categories and 140 legacy product routes. Do not re-import over an existing database: products edited through the panel live in D1, not in the old static HTML.

Image uploads are optimized in the browser to WebP, capped at 1 MiB, and stored in D1. JPG/PNG/WebP signatures are checked server-side. Existing photoshoot sheets remain unchanged. Public product/category pages and the gifts grid read the live catalog; existing product URLs keep working.

## Login and recovery

Passwords use salted PBKDF2-SHA256 (100,000 iterations). Sessions use random tokens stored only as hashes, expire after eight hours and use Secure, HttpOnly, SameSite=Strict cookies. Mutations require same-origin requests. Auth attempts are rate-limited. Changing a password revokes other sessions.

The setup endpoint is permanently disabled once the owner creates their login. Losing the private setup link before activation requires rotating `ADMIN_SETUP_TOKEN`. After activation, change the password in Account settings; owner-verified recovery must be performed through the hosting account.

Run `npm test` to check migration integrity, authentication, authorization, CSRF, persistence, variants, archival/restoration, uploads, password changes and rate limiting. Development tests use an isolated in-memory SQLite database and never alter the live catalog.
