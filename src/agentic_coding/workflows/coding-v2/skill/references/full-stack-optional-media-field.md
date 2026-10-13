# Full-stack optional media/array field extension

Use this reference when adding optional media fields such as `photos: string[]` to an existing product model that already has API, persistence, fixtures, and UI consumers.

## Durable workflow

1. **Consequence scan before implementation**
   - Search backend models/schemas, service create/update methods, public serializers, API tests, persistence adapters, migrations, seed/fixture data, frontend types, form components, list/detail rendering, and search/recommendation renderers.
   - Look for an existing analogous field on a sibling model and copy that pattern rather than inventing a new storage/rendering path.

2. **Write tests first for the missing vertical path**
   - Backend service/API tests should assert create, update, list/public-response, and recommendation/search payloads preserve the optional field.
   - Frontend tests should assert accessible rendering (`role="img"`, meaningful `alt`) and that create/edit forms expose the field.

3. **Patch the model and serializers**
   - Add the optional field to backend domain/Pydantic models with a safe default (`Field(default_factory=list)` for arrays).
   - Add the frontend type field as optional when older API payloads may not include it.
   - Confirm public serializers redact only sensitive fields and do not accidentally drop media fields.

4. **Patch persistence deliberately**
   - Add DB columns or JSON serialization support wherever the current store actually writes normalized model rows.
   - For JSON arrays in SQL-backed normalized stores, use an explicit JSON column such as `photos_json TEXT NOT NULL DEFAULT '[]'` and round-trip through `json.dumps`/`json.loads` at adapter boundaries.

5. **Add upload/storage without breaking the existing URL-array contract when possible**
   - If models already persist `photos: string[]`, prefer a narrow upload endpoint that returns `{ url, key, storage_backend }`; then merge returned URLs into the existing create/update payload instead of changing every model serializer to accept binary data.
   - When the product requirement says uploads only / no arbitrary image URLs, keep the URL-array contract but make URLs *managed outputs*: add an `is_managed_url()`-style helper in the storage adapter and have create/update endpoints reject `photos` entries that did not come from the upload backend.
   - Put storage decisions behind an adapter/service (`store(...) -> StoredPhoto`) rather than in route handlers. Keep validation there too: allowed image MIME types, max bytes, safe filename slugging, tenant/kind-scoped keys, and deterministic URL construction.
   - Make S3 opt-in by complete configuration (bucket + credentials, plus optional endpoint/public base/ACL/region). If incomplete, fall back to local disk and mount a static URL prefix for served local files.
   - For S3 tests, inject or monkeypatch the S3 client/module and assert the `put_object` arguments (`Bucket`, `Key`, `Body`, `ContentType`, optional `ACL`) without requiring real credentials or network.
   - Add negative API tests for external URL rejection on create/update, invalid MIME types, oversize files, wrong upload kind, missing file parts, and unauthenticated upload attempts.
   - If a multipart dependency cannot be installed during the session, a small request-body parser may unblock a simple single-file upload endpoint; treat this as a scoped workaround and keep tests around invalid type/oversize behavior. Prefer framework-native `UploadFile` when the dependency is available.

6. **Patch UI in both input and output paths**
   - If the task is URL-optional, add create/edit form inputs that use the repo's existing tag/CSV helpers when media is represented as URL arrays.
   - If the task is upload-only, remove manual URL inputs entirely; use `<input type="file" accept="image/jpeg,image/png,image/webp,image/gif" multiple>` (or the product-approved MIME set) for create/edit flows and assert old URL labels are absent in UI tests.
   - For file uploads, upload selected files first, then save returned upload URLs in the existing create/update payload. Do not combine with manually entered URL strings when arbitrary URLs are no longer supported.
   - On edit forms, decide explicitly whether new uploads replace the existing photo set or append to it; make the label and payload behavior match that decision.
   - Render thumbnails in list/detail/search surfaces with stable sizing, `object-fit: cover`, and descriptive alt text.
   - If both parent and child models can have photos, prefer the most specific object photo first (unit photo before property photo) and fall back gracefully.

7. **Verify beyond targeted failures**
   - Run targeted tests that failed red first, then full backend tests, frontend tests, lint, typecheck/build, `git diff --check`, and a diff/stat review.
   - Include migration smoke checks when migration lists are generated programmatically.

## Migration pitfall: generated Postgres migration lists

When a project derives `POSTGRES_MIGRATIONS` from `SQLITE_MIGRATIONS` by slicing (for example, `SQLITE_MIGRATIONS[:-1]`) and then appending Postgres-specific replacements, adding a new SQLite migration can silently pull a previously SQLite-only migration into the Postgres path or duplicate versions.

Prefer selecting the shared prefix by migration name/version boundary rather than by list position, then append Postgres-specific versions explicitly. Add a tiny smoke check that prints/asserts migration version lists and duplicate counts for both SQLite and Postgres.
