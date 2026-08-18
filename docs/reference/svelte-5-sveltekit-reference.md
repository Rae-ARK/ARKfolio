# Svelte 5 & SvelteKit Reference

> A consolidated, quick-reference version of the Svelte 5 runes changelog context and the abridged Svelte/SvelteKit developer docs. Built for fast lookup — jump to a section via the index below.

---

## Index

- [1. Background: Why Runes Exist](#1-background-why-runes-exist)
- [2. Svelte 5 Runes — Quick Cheatsheet](#2-svelte-5-runes--quick-cheatsheet)
- [3. Svelte 5 Runes — Full Reference](#3-svelte-5-runes--full-reference)
  - [3.1 `$state`](#31-state)
  - [3.2 `$state.raw`](#32-stateraw)
  - [3.3 `$state.snapshot`](#33-statesnapshot)
  - [3.4 Passing state into functions](#34-passing-state-into-functions)
  - [3.5 `$derived` / `$derived.by`](#35-derived--derivedby)
  - [3.6 `$effect` (and `.pre`, `.tracking`, `.root`)](#36-effect-and-pre-tracking-root)
  - [3.7 `$props` / `$props.id()`](#37-props--propsid)
  - [3.8 `$bindable`](#38-bindable)
  - [3.9 `$host`](#39-host)
  - [3.10 `await` in Svelte (experimental)](#310-await-in-svelte-experimental)
- [4. Snippets & Rendering](#4-snippets--rendering)
  - [4.1 `{#snippet}`](#41-snippet)
  - [4.2 Snippet scope](#42-snippet-scope)
  - [4.3 Passing snippets to components](#43-passing-snippets-to-components)
  - [4.4 Typing snippets](#44-typing-snippets)
  - [4.5 `{@render}`](#45-render)
  - [4.6 `<svelte:boundary>`](#46-svelteboundary)
  - [4.7 Class objects](#47-class-objects)
- [5. SvelteKit Project Basics](#5-sveltekit-project-basics)
  - [5.1 Setup & minimal config](#51-setup--minimal-config)
  - [5.2 Project structure](#52-project-structure)
- [6. Routing](#6-routing)
  - [6.1 Route files (`+page`, `+layout`, `+server`, `+error`)](#61-route-files-page-layout-server-error)
  - [6.2 `$types`](#62-types)
  - [6.3 Advanced routing (rest/optional params, matchers)](#63-advanced-routing-restoptional-params-matchers)
  - [6.4 Advanced layouts (groups, `@` resets)](#64-advanced-layouts-groups--resets)
- [7. Loading Data](#7-loading-data)
  - [7.1 Page & layout data](#71-page--layout-data)
  - [7.2 `page.data`](#72-pagedata)
  - [7.3 Universal vs. server loads](#73-universal-vs-server-loads)
  - [7.4 Load function arguments](#74-load-function-arguments)
  - [7.5 Fetch, headers, cookies](#75-fetch-headers-cookies)
  - [7.6 Parent data](#76-parent-data)
  - [7.7 Errors & redirects](#77-errors--redirects)
  - [7.8 Streaming with promises](#78-streaming-with-promises)
  - [7.9 Rerunning / invalidating loads](#79-rerunning--invalidating-loads)
  - [7.10 Auth implications](#710-auth-implications)
- [8. Forms](#8-forms)
  - [8.1 Form actions](#81-form-actions)
  - [8.2 Validation errors (`fail`)](#82-validation-errors-fail)
  - [8.3 Redirects in actions](#83-redirects-in-actions)
  - [8.4 Reloading after actions](#84-reloading-after-actions)
  - [8.5 Progressive enhancement (`use:enhance`)](#85-progressive-enhancement-useenhance)
- [9. Remote Functions (experimental)](#9-remote-functions-experimental)
  - [9.1 `query`](#91-query)
  - [9.2 `form`](#92-form)
  - [9.3 `command`](#93-command)
  - [9.4 `prerender`](#94-prerender)
  - [9.5 Validation, security, `getRequestEvent`, redirects](#95-validation-security-getrequestevent-redirects)
- [10. Page Options](#10-page-options)
- [11. State Management Rules](#11-state-management-rules)
- [12. Building, Adapters & SPA Mode](#12-building-adapters--spa-mode)
- [13. Hooks](#13-hooks)
- [14. Errors](#14-errors)
- [15. Link Options (`data-sveltekit-*`)](#15-link-options-data-sveltekit-)
- [16. Server-Only Modules](#16-server-only-modules)
- [17. Shallow Routing](#17-shallow-routing)
- [18. Images](#18-images)
- [19. Import Cheat Sheet](#19-import-cheat-sheet)

---

## 1. Background: Why Runes Exist

_Context from a Fireship "Code Report" episode (Oct 24, 2024), condensed._

A year prior, the creator had claimed the `$` syntax was Svelte's most powerful abstraction — a take that aged poorly once Svelte announced **runes**, a feature that replaced the `$`-based reactivity syntax. Runes became official with the **Svelte 5** release.

**Why the change?** In Svelte 4:

- `let` looked like plain JavaScript but secretly behaved like a reactive signal via compiler magic — implicit and only worked inside `.svelte` files.
- Sharing reactive logic across plain `.js`/`.ts` files required a separate API (**stores**), fragmenting the mental model.

**Runes fix this by:**

1. Making reactivity **explicit** (`$state`, `$derived`, `$effect`, `$props` are visibly "doing something special").
2. Creating a **universal reactivity system** usable in `.svelte` files _and_ plain JS/TS — no separate stores API needed.

**The four core runes** (roughly 90% of what you need to know):

| Rune       | Replaces             | Analogous to                     |
| ---------- | -------------------- | -------------------------------- |
| `$state`   | `let`                | React `useState` / Vue `ref`     |
| `$derived` | `$: computed = ...`  | React `useMemo` / Vue `computed` |
| `$effect`  | `$: sideEffect(...)` | React `useEffect`                |
| `$props`   | `export let`         | React props / Vue `defineProps`  |

**Industry framing:** Svelte 5 now looks more "React-like" (explicit reactivity), while React is trending toward Svelte-like ergonomics (React 19 compiler removing the need for `useMemo` in Next.js 15). Angular is adopting signals (influenced by SolidJS); Vue and the older Knockout.js pioneered similar reactive-signal ideas without getting much credit. Takeaway: most major frameworks are converging on the same reactive-signal model.

[↑ Back to Index](#index)

---

## 2. Svelte 5 Runes — Quick Cheatsheet

| Svelte 4                                 | Svelte 5                                  |
| ---------------------------------------- | ----------------------------------------- |
| `let count = 0`                          | `let count = $state(0)`                   |
| `$: double = count * 2`                  | `const double = $derived(count * 2)`      |
| `$: console.log(double)`                 | `$effect(() => console.log(double))`      |
| `export let foo = true; export let bar;` | `let { foo = true, bar } = $props();`     |
| `<button on:click={...}>`                | `<button onclick={...}>`                  |
| Slots (`<slot name="x" let:y>`)          | Snippets (`{#snippet x(y)}...{/snippet}`) |
| `$app/stores`                            | `$app/state`                              |

**Golden rule:** Runes are compiler keywords, not functions — never import them.

[↑ Back to Index](#index)

---

## 3. Svelte 5 Runes — Full Reference

### 3.1 `$state`

Creates a reactive variable that auto-updates the UI.

```svelte
<script>
	let count = $state(0);
</script>

<button onclick={() => count++}>Clicked: {count}</button>
```

- Arrays/objects become **deeply reactive proxies**:
  ```js
  let todos = $state([{ done: false, text: 'add more todos' }]);
  todos[0].done = !todos[0].done;
  ```
- ❌ Don't destructure reactive proxies (`let { done } = todos[0]`) — breaks reactivity.
- ❌ Don't wrap state in custom objects unnecessarily.
- Works in class fields:
  ```js
  class Todo {
  	done = $state(false);
  	text = $state('');
  	reset = () => {
  		this.text = '';
  		this.done = false;
  	};
  }
  ```

### 3.2 `$state.raw`

Shallow state — mutations are **not** tracked; reassign the whole object instead.

```js
let person = $state.raw({ name: 'Heraclitus', age: 49 });
// person.age += 1;  // ❌ no effect
person = { name: 'Heraclitus', age: 50 }; // ✅ correct
```

### 3.3 `$state.snapshot`

Produces a plain (non-proxy) object copy of reactive state — use only when passing state to external APIs that choke on proxies.

```js
console.log($state.snapshot(counter));
```

### 3.4 Passing state into functions

Reactive variables don't stay "live" when passed by value — pass **getter functions** instead.

```js
function add(getA, getB) {
	return () => getA() + getB();
}
let a = 1,
	b = 2;
let total = add(
	() => a,
	() => b
);
console.log(total());
```

### 3.5 `$derived` / `$derived.by`

Computes a memoized value from dependencies; re-runs only when deps change.

```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
</script>
```

- No side effects inside `$derived` — keep it pure.
- For multi-line/complex logic use `$derived.by`:
  ```svelte
  let total = $derived.by(() => {
    let sum = 0;
    for (const n of numbers) sum += n;
    return sum;
  });
  ```
- **Overriding derived values** (e.g. optimistic UI) — reassign directly, it reverts once a dependency updates:
  ```svelte
  let likes = $derived(post.likes);
  async function onclick() {
    likes += 1;
    try { await post.like(); } catch { likes -= 1; }
  }
  ```
  ❌ Don't try to override derived state via `$effect`.

### 3.6 `$effect` (and `.pre`, `.tracking`, `.root`)

Runs code when its dependencies change (side effects only — not for state sync).

```svelte
$effect(() => { console.log('Size changed:', size); });
```

- Runs **after** DOM updates; return a teardown function for cleanup:
  ```js
  $effect(() => {
  	const interval = setInterval(() => (count += 1), 1000);
  	return () => clearInterval(interval);
  });
  ```
- **`$effect.pre`** — same as `$effect` but runs **before** DOM updates (e.g. autoscroll).
- **`$effect.tracking()`** — returns whether current code runs inside a reactive context (debugging).
- **`$effect.root`** — creates a non-tracked scope for nested effects with **manual** cleanup (no auto-cleanup):
  ```js
  const cleanup = $effect.root(() => {
  	$effect(() => console.log('Count is:', count));
  	return () => console.log('Root effect cleaned up');
  });
  ```

### 3.7 `$props` / `$props.id()`

```svelte
<script>
	let { adjective } = $props();
</script>
```

- Default values: `let { adjective = 'happy' } = $props();`
- Rename reserved words: `let { super: trouper } = $props();`
- Rest/remaining props: `let { a, b, ...others } = $props();`
- ❌ Don't mutate props directly — use callbacks or `$bindable`.
- **`$props.id()`** — unique, stable ID for the component instance (for `<label for>` etc.):
  ```svelte
  const uid = $props.id();
  <label for="{uid}-firstname">First Name:</label>
  ```

### 3.8 `$bindable`

Marks a prop as two-way bindable (explicit opt-in, unlike Svelte 4 where all props were implicitly bindable).

```svelte
<!-- FancyInput.svelte -->
<script>
	let { value = $bindable() } = $props();
</script>

<input bind:value />
```

Default to one-way data flow unless bidirectionality is genuinely needed.

### 3.9 `$host`

Only inside **custom elements** — accesses the host element for dispatching custom events.

```svelte
<script>
	function dispatch(type) {
		$host().dispatchEvent(new CustomEvent(type));
	}
</script>
```

### 3.10 `await` in Svelte (experimental)

Usable at top-level `<script>`, inside `$derived(...)`, and inline in markup.

```svelte
<script>
	let double = $derived(await makeDouble(count));
</script>

<p>{await getNumber(count)} * 2 = {double}</p>
{#if await isEven(id)}<p>even</p>{/if}
```

- **Enable:** in `svelte.config.js` →
  ```js
  export default { compilerOptions: { experimental: { async: true } } };
  ```
  (Experimental since 5.36; will be removed in Svelte 6 once stabilized.)
- **Must** be wrapped in a `<svelte:boundary>` with a `pending` snippet:
  ```svelte
  <svelte:boundary>
  	<MyApp />
  	{#snippet pending()}<p>loading...</p>{/snippet}
  </svelte:boundary>
  ```
- **Behavior notes:**
  - UI reads of state that an `await` depends on are deferred until the async work resolves.
  - Faster updates can overtake slower ones — results reflect the latest completed work.
  - Script-level `await`s run sequentially like normal JS (parallelize yourself if needed).
  - `$derived` awaits run sequentially first, then update independently.
  - Watch for `await_waterfall` warnings (accidental serialization of independent work).
  - Use `$effect.pending()` to detect in-flight async work.
  - Errors bubble to the nearest `<svelte:boundary>`.

[↑ Back to Index](#index)

---

## 4. Snippets & Rendering

### 4.1 `{#snippet}`

Reusable, parameterized chunks of markup.

```svelte
{#snippet figure(image)}
	<figure>
		<img src={image.src} alt={image.caption} width={image.width} height={image.height} />
		<figcaption>{image.caption}</figcaption>
	</figure>
{/snippet}
```

Params can have defaults/destructuring; **no rest parameters** allowed.

### 4.2 Snippet scope

Snippets see variables from their outer lexical scope (script, block-level).

```svelte
<script>
	let { message = "it's great to see you!" } = $props();
</script>

{#snippet hello(name)}<p>hello {name}! {message}!</p>{/snippet}
{@render hello('alice')}
```

❌ Can't render a snippet outside its declared lexical scope.

### 4.3 Passing snippets to components

Snippets are first-class values — pass as props:

```svelte
{#snippet header()}<th>fruit</th>...{/snippet}
{#snippet row(d)}<td>{d.name}</td>...{/snippet}
<Table data={fruits} {header} {row} />
```

- Content **not** wrapped in a snippet tag becomes the implicit `children` snippet (fallback content):
  ```svelte
  <!-- Button.svelte -->
  <script>
  	let { children } = $props();
  </script>

  <button>{@render children()}</button>
  ```
- Replaces Svelte 4 slots (`<slot name="x" let:y>` → `{#snippet x(y)}`).

### 4.4 Typing snippets

```svelte
<script lang="ts">
	import type { Snippet } from 'svelte';
	interface Props {
		data: any[];
		children: Snippet;
		row: Snippet<[any]>;
	}
	let { data, children, row }: Props = $props();
</script>
```

### 4.5 `{@render}`

Invokes a snippet.

```svelte
{#snippet sum(a, b)}<p>{a} + {b} = {a + b}</p>{/snippet}
{@render sum(1, 2)}
```

Always call with parentheses when the snippet expects params (replaces `<slot name="sum" {a} {b} />`).

### 4.6 `<svelte:boundary>`

Prevents render errors in a subtree from crashing the whole app.

```svelte
<svelte:boundary onerror={(error, reset) => console.error(error)}>
	<FlakyComponent />
</svelte:boundary>
```

Optional `failed` snippet renders fallback UI with a `reset()` function:

```svelte
<svelte:boundary>
	<FlakyComponent />
	{#snippet failed(error, reset)}
		<button onclick={reset}>Oops! Try again</button>
	{/snippet}
</svelte:boundary>
```

### 4.7 Class objects

Conditional classes via object syntax (like `clsx`):

```svelte
<div class={{ cool, lame: !cool }}>Content</div>
```

[↑ Back to Index](#index)

---

## 5. SvelteKit Project Basics

### 5.1 Setup & minimal config

Scaffold: `npx sv create` (do **not** use the deprecated `npm create svelte`).

Minimum `package.json`:

```json
{
	"devDependencies": {
		"@sveltejs/adapter-auto": "^6.0.0",
		"@sveltejs/kit": "^2.0.0",
		"@sveltejs/vite-plugin-svelte": "^5.0.0",
		"svelte": "^5.0.0",
		"vite": "^6.0.0"
	}
}
```

Keep all of these in `devDependencies` — never move to `dependencies`.

Minimum `vite.config.js`:

```js
import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';
export default defineConfig({ plugins: [sveltekit()] });
```

Minimum `svelte.config.js`:

```js
import adapter from '@sveltejs/adapter-auto';
export default { kit: { adapter: adapter() } };
```

SvelteKit supports **SPA, SSR, and SSG** — mixable within a single project.

### 5.2 Project structure

- `src/lib/` → shared code, aliased as `$lib`
- `src/lib/server/` → server-only modules, aliased as `$lib/server` (never import into client files)
- `src/params/` → param matchers
- `src/routes/` → pages/components
- `src/app.html`, `src/error.html`, `src/hooks.client.js`, `src/hooks.server.js`, `src/service-worker.js`
- `static/` → public assets
- `tests/` → Playwright tests (if used)
- Config: `package.json`, `svelte.config.js`, `tsconfig.json`/`jsconfig.json` (extends `.svelte-kit/tsconfig.json`), `vite.config.js`
- `.svelte-kit/` → auto-generated build output; **do not commit**, safe to delete (regenerated on `dev`/`build`)
- Remember `"type": "module"` in `package.json` if using ESM.

[↑ Back to Index](#index)

---

## 6. Routing

Filesystem router: `src/routes` maps directories → URL paths. A `+page.svelte` inside a folder makes that folder a visitable route (e.g. `src/routes/hello/+page.svelte` → `/hello`). `[param]` folders define dynamic segments.

❌ `src/routes/hello.svelte` does **not** become `/hello` — only the `+`-prefixed file convention works. Never hard-code routes; rely on the filesystem convention.

### 6.1 Route files (`+page`, `+layout`, `+server`, `+error`)

| File                               | Purpose                                                                                                                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `+page.svelte`                     | UI for a route. SSR on first load, CSR after. Don't fetch data inside — use `load` in `+page.js`/`+page.server.js`; access via `let { data } = $props()` (typed `PageProps`).        |
| `+page.js`                         | `export function load({ params })` (typed `PageLoad`). Can export `prerender`, `ssr`, `csr`. No private/DB logic, no `actions`.                                                      |
| `+page.server.js`                  | `export async function load(...)` (typed `PageServerLoad`) — DB/private env OK, must return serializable data. Can export `actions` for `<form>` handling.                           |
| `+error.svelte`                    | Error page for the route folder; use `page.status` / `page.error.message` from `$app/state`. SvelteKit walks up the tree for the nearest boundary, falling back to `src/error.html`. |
| `+layout.svelte`                   | Persistent UI (nav/footer); must include `{@render children()}`. Nest in subfolders to scope layouts; child layouts inherit parents.                                                 |
| `+layout.js` / `+layout.server.js` | `load()` (typed `LayoutLoad`/`LayoutServerLoad`) supplies `data` to the layout + its children. Server-only ops belong in `+layout.server.js`.                                        |
| `+server.js`                       | Exports HTTP handlers (`GET`, `POST`, etc.) receiving `RequestEvent`; return `Response` or use `json()`/`error()`/`redirect()`. Export `fallback` to catch other methods.            |

`+page.svelte` example:

```svelte
<script lang="ts">
	import type { PageProps } from './$types';
	let { data }: PageProps = $props();
</script>

<h1>{data.title}</h1>
```

`+page.js` example:

```ts
import type { PageLoad } from './$types';
export const load: PageLoad = () => ({ title: 'Hello world!' });
```

`+layout.svelte` example:

```svelte
<script>
	let { children, data } = $props();
</script>

<p>Some Content that is shared for all pages below this layout</p>
{@render children()}
```

`+server.js` example:

```ts
import type { RequestHandler } from './$types';
export const GET: RequestHandler = ({ url }) => new Response('hello world');
```

Non-`+` files in route folders are ignored by the router — use to colocate utilities/components. For cross-route imports, put modules in `src/lib` and import via `$lib`.

### 6.2 `$types`

SvelteKit auto-generates `$types.d.ts` (`PageProps`, `LayoutProps`, `RequestHandler`, `PageLoad`, `PageServerLoad`, `LayoutLoad`, `LayoutServerLoad`) — import from `./$types` in the corresponding route file for type-safe props/loaders.

### 6.3 Advanced routing (rest/optional params, matchers)

- **Rest params:** `[...file]` captures unknown-length segments as a single string (e.g. `src/routes/hello/[...path]` catches everything under `/hello`). Pair with a catch-all `+error.svelte` for custom 404s.
- **Optional params:** `[[lang]]` makes a segment optional (`[[lang]]/home` matches both `/home` and `/en/home`). Cannot follow a rest parameter.
- **Matchers:** `src/params/type.js` constrains `[param=type]` (e.g. only specific string values); falls back to other routes or 404 if the test fails.

### 6.4 Advanced layouts (groups & `@` resets)

- Group folders `(app)` / `(marketing)` apply a shared layout **without** affecting the URL.
- Break out of the inherited layout chain: `+page@segment.svelte` (e.g. `+page@(app).svelte`) per page, or `+layout@.svelte` per layout.
- Use sparingly — overuse complicates nesting; simple composition/wrapper components are often better.

[↑ Back to Index](#index)

---

## 7. Loading Data

### 7.1 Page & layout data

`+page.js`'s `load` return value is available in `+page.svelte` via `let { data } = $props()`.

```js
// src/routes/foo/+page.js
export async function load({ fetch }) {
	const result = await fetch('/data/from/somewhere').then((r) => r.json());
	return { result };
}
```

```svelte
<!-- src/routes/foo/+page.svelte -->
<script>
	let { data } = $props();
</script>

{data.result}
```

Universal loads (`+*.js`) run on SSR **and** CSR; private/DB-backed loads go in `+page.server.js`. Layout data flows **downward** — pages/child layouts see parent `data`.

### 7.2 `page.data`

`$app/state`'s `page` object exposes all `load` data anywhere via `page.data` (types from `App.PageData`). Good for `<svelte:head><title>{page.data.title}</title></svelte:head>`.

⚠️ Don't use `$app/stores` anymore (superseded by `$app/state`) unless explicitly required.

### 7.3 Universal vs. server loads

- **Universal** (`+*.js`): runs server first, then browser; use for public APIs or returning complex values.
- **Server** (`+*.server.js`): always server-side; can use secrets, cookies, DB.
- Both get: `params`, `route`, `url`, `fetch`, `setHeaders`, `parent`, `depends`.
- Server loads additionally get: `cookies`, `locals`, `platform`, `request`.

### 7.4 Load function arguments

- `url` — `URL` object (no `hash` server-side)
- `route.id` — route pattern
- `params` — path segment values
- `url.searchParams` changes trigger reruns

### 7.5 Fetch, headers, cookies

Enhanced `fetch` in load functions:

```js
export async function load({ fetch, params }) {
	const res = await fetch(`/api/items/${params.id}`);
	return { item: await res.json() };
}
```

Set response headers:

```js
export async function load({ fetch, setHeaders }) {
	const response = await fetch(url);
	setHeaders({
		age: response.headers.get('age'),
		'cache-control': response.headers.get('cache-control')
	});
	return response.json();
}
```

Read cookies (server loads only):

```js
export async function load({ cookies }) {
	const sessionid = cookies.get('sessionid');
	return { user: await db.getUser(sessionid) };
}
```

❌ Don't set `set-cookie` via `setHeaders` — use `cookies.set()`.

### 7.6 Parent data

```js
export async function load({ parent }) {
	const { a } = await parent();
	return { b: a + 1 };
}
```

### 7.7 Errors & redirects

```js
import { redirect } from '@sveltejs/kit';
export function load({ locals }) {
	if (!locals.user) redirect(307, '/login');
}
```

```js
import { error } from '@sveltejs/kit';
export function load({ locals }) {
	if (!locals.user) error(401, 'not logged in');
}
```

Unexpected exceptions trigger the `handleError` hook → 500 response.

### 7.8 Streaming with promises

Server load functions can return unresolved promises to stream data:

```js
export async function load({ params }) {
	return { comments: loadComments(params.slug), post: await loadPost(params.slug) };
}
```

```svelte
<h1>{data.post.title}</h1>
{#await data.comments}
	Loading comments...
{:then comments}
	{#each comments as comment}<p>{comment.content}</p>{/each}
{:catch error}
	<p>error loading comments: {error.message}</p>
{/await}
```

### 7.9 Rerunning / invalidating loads

Load functions rerun when:

- Referenced `params`/URL properties change
- A parent load reran and `await parent()` was called
- A dependency was invalidated via `invalidate(url)` or `invalidateAll()`

```js
// in load function
export async function load({ fetch, depends }) {
	depends('app:random');
}
```

```js
// in component
import { invalidate } from '$app/navigation';
function rerunLoadFunction() {
	invalidate('app:random');
}
```

Exclude from dependency tracking with `untrack`:

```js
export async function load({ untrack, url }) {
	if (untrack(() => url.pathname === '/')) return { message: 'Welcome!' };
}
```

### 7.10 Auth implications

Layout loads don't automatically rerun on CSR — guards in `+layout.server.js` require child pages to `await parent()`. To avoid missed checks/waterfalls, prefer the `handle` hook for global protection, or per-page server loads. Use `getRequestEvent()` inside shared functions (e.g. `requireLogin()`) to access `locals`, `url`, etc. without threading params manually.

[↑ Back to Index](#index)

---

## 8. Forms

### 8.1 Form actions

`+page.server.js` exports `actions`; a plain `<form method="POST">` posts to the default action with zero JS. **Only** `+page.server.js` can export `actions` (not `+page.js`/`+layout.js`/`+layout.server.js`).

```ts
// src/routes/login/+page.server.js
import type { Actions } from './$types';
export const actions: Actions = {
	default: async (event) => {
		/* log the user in */
	}
};
```

```svelte
<!-- src/routes/login/+page.svelte -->
<form method="POST">
	<label>Email <input name="email" type="email" /></label>
	<label>Password <input name="password" type="password" /></label>
	<button>Log in</button>
</form>
```

Named actions: `actions = { login: ..., register: ... }` invoked via `action="?/register"` or `formaction="?/register"` (don't use `default` name when using named actions).

### 8.2 Validation errors (`fail`)

```js
return fail(400, { field, error: true });
```

Display via `form?.field`; repopulate inputs with `value={form?.field ?? ''}`. Use `fail` (not `throw`) so the nearest `+error.svelte` isn't invoked. Payload must be JSON-serializable.

### 8.3 Redirects in actions

`redirect(status, location)` throws a 3xx redirect (bypasses re-render). Client-side, use `goto()` from `$app/navigation` for programmatic redirects.

### 8.4 Reloading after actions

After an action completes (no redirect), SvelteKit reruns `load` and re-renders, merging the action's return value into `form`. The `handle` hook runs **once before** the action — if cookies change inside the action, also update `event.locals` there (it doesn't persist automatically).

### 8.5 Progressive enhancement (`use:enhance`)

```svelte
<script>
	import { enhance } from '$app/forms';
	let { form } = $props();
</script>

<form method="POST" use:enhance>
	<!-- form content -->
</form>
```

`use:enhance` intercepts submission, prevents full reload, updates `form`/`page.form`/`page.status`, resets the form, invalidates data, handles redirects/errors, restores focus. ❌ Don't use a plain `onsubmit` handler for this — customize via a callback passed to `enhance` (`update()` for defaults, or `applyAction(result)`), or roll your own with `fetch` + `deserialize` (never `JSON.parse` on action responses).

[↑ Back to Index](#index)

---

## 9. Remote Functions (experimental)

Type-safe, server-only functions callable from the client — can replace `load` and form actions. Pairs well with async Svelte (`await` in `$derived`/markup).

**Enable:**

```js
// svelte.config.js
export default { kit: { experimental: { remoteFunctions: true } } };
```

Place `.remote.js`/`.remote.ts` files in `src/lib` or `src/routes`; export via `query`, `form`, `command`, or `prerender` from `$app/server`. Client imports become fetch-wrappers to generated endpoints. Args/returns serialize via devalue (Date, Map, custom transport supported).

### 9.1 `query`

Read dynamic data.

```js
// src/routes/blog/data.remote.js
import { query } from '$app/server';
import * as db from '#lib/server/database';
export const getPosts = query(async () => db.posts());
```

```svelte
<script>
	import { getPosts } from './data.remote';
</script>

<ul>
	{#each await getPosts() as { title, slug }}
		<li><a href="/blog/{slug}">{title}</a></li>
	{/each}
</ul>
```

- **Args + validation:** pass a Standard Schema (Valibot/Zod) as first param: `query(v.string(), async (slug) => {...})`.
- **Caching:** calls are cached per-page (`getPosts() === getPosts()`); refresh via `getPosts().refresh()`.
- Non-`await` usage exposes `loading`, `error`, `current` props.

### 9.2 `form`

Mutations via `<form>`.

```js
import { form } from '$app/server';
export const createPost = form(async (data) => {
	const user = await auth.getUser();
	if (!user) error(401, 'Unauthorized');
	const title = data.get('title');
	db.insertPost(title, data.get('content'));
	redirect(303, `/blog/${title}`);
});
```

```svelte
<form {...createPost}>
	<input name="title" />
	<textarea name="content" />
	<button>Publish</button>
</form>
```

- Works without JS (regular `method`/`action`); with JS, submits without full reload.
- **Single-flight mutations:** server-driven → `await getPosts().refresh()` inside the handler; client-driven → `createPost.enhance(async ({ submit }) => { await submit().updates(getPosts()); })`.
- **Optimistic UI:** `submit().updates(getPosts().withOverride((posts) => [newPost, ...posts]))`.
- Return data instead of redirecting → read via `createPost.result`.
- **`buttonProps`** for per-button `formaction`: `<button {...register.buttonProps}>register</button>`.

### 9.3 `command`

Programmatic writes (not tied to a `<form>`); **cannot** be called during render.

```js
import { command, query } from '$app/server';
export const getLikes = query(v.string(), async (id) => db.likes.get(id));
export const addLike = command(v.string(), async (id) => {
	await db.likes.add(id);
});
```

```svelte
<button onclick={() => addLike(item.id)}>add like</button><p>likes: {await getLikes(item.id)}</p>
```

Update related queries: server-side `getLikes(id).refresh()`; client-side `await addLike(item.id).updates(getLikes(item.id))`; optimistic via `.withOverride((n) => n + 1)`.

### 9.4 `prerender`

Build-time reads for static-ish data, usable even on dynamic pages for partial prerendering.

```js
import { prerender } from '$app/server';
export const getPosts = prerender(
	async () => db.sql`SELECT title, slug FROM post ORDER BY published_at DESC`
);
```

- Same Standard Schema arg validation as `query`.
- **Seed inputs** for crawling: `prerender(v.string(), async (slug) => {...}, { inputs: () => ['first-post', 'second-post'] })`.
- Excluded from the server bundle by default; set `{ dynamic: true }` to allow calling with non-prerendered args.
- If a page has `export const prerender = true`, you cannot use dynamic `query`s on it.

### 9.5 Validation, security, `getRequestEvent`, redirects

- `query`, `command`, `prerender` accept a Standard Schema for arg validation; failures return 400.
- Customize the failure message via the `handleValidationError` hook (`src/hooks.server.ts`):
  ```ts
  export function handleValidationError() {
  	return { message: 'Nice try, hacker!' };
  }
  ```
- `form` has no schema arg — validate `FormData` manually.
- **`getRequestEvent()`** inside remote functions gives access to `cookies`, `locals`, etc. — but **no** `params`/`route.id`, cannot set headers (except cookies, and only in `form`/`command`), and `url.pathname` is always `/`.
- **Redirects:** allowed in `query`, `form`, `prerender` via `redirect(...)`. **Not allowed** in `command` — return `{ redirect }` and handle it client-side if truly necessary.

[↑ Back to Index](#index)

---

## 10. Page Options

| Option      | Where                                              | Effect                                                                                                                                                                                                                                                                                                    |
| ----------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prerender` | page/layout modules, also `+server.js`             | `true` → static HTML at build; `false` → skip; `'auto'` → include in SSR manifest. Inherits from parent. Dynamic routes need `entries()` (or `config.kit.prerender.entries`) to tell the crawler which params to generate. ❌ Don't prerender pages using form actions or server-side `url.searchParams`. |
| `entries`   | dynamic route's `+page(.server).js` / `+server.js` | `export function entries(): Array<Record<string,string>>` (can be async) — lists param sets to prerender. Pair with `prerender = true`.                                                                                                                                                                   |
| `ssr`       | page/layout module                                 | `false` disables server rendering → HTML shell only, client-only SPA. Don't set both `ssr` and `csr` to `false`.                                                                                                                                                                                          |
| `csr`       | page/layout module                                 | `false` disables hydration — no JS bundle, no client routing/HMR/form-enhancement. Good for purely static pages; avoid on interactive ones.                                                                                                                                                               |

[↑ Back to Index](#index)

---

## 11. State Management Rules

- Servers are stateless & shared across users — **never** store per-user data in shared server variables. Authenticate via cookies, persist to a database.
- Keep `load` functions **pure**: no side effects, no global store writes. Return data via `data`/`page.data`.
- For shared client-only state: use Svelte's context API (`setContext`/`getContext`) or URL params for persistent filters; use snapshots for ephemeral UI state tied to navigation history.

[↑ Back to Index](#index)

---

## 12. Building, Adapters & SPA Mode

**Build:** two phases — Vite compiles (+ prerenders if enabled), then an **adapter** tailors output for the deployment target. Guard build-time-unsafe code:

```js
import { building } from '$app/env';
if (!building) {
	/* ... */
}
```

Preview locally: `npm run preview` (Node-only, no adapter hooks).

**Adapters:** configured in `svelte.config.js` under `kit.adapter = adapter(opts)` (Cloudflare, Netlify, Node, static, Vercel, community adapters). Some expose a `platform` object (e.g. Cloudflare's `env`) accessible via `event.platform`.

**Single-page apps:** set `export const ssr = false;` in the root `+layout.js` for full CSR. For static hosting, use `@sveltejs/adapter-static` with a fallback HTML (e.g. `200.html`) so client routing handles unknown paths. Individual pages can still opt back into `prerender = true` / `ssr = true`.

[↑ Back to Index](#index)

---

## 13. Hooks

**Server hooks:**

- `handle({ event, resolve })` — runs on every request; mutate `event.locals`, bypass routing, or call `resolve(event, { transformPageChunk, filterSerializedResponseHeaders, preload })`.
- `handleFetch({ event, request, fetch })` — intercepts server-side `fetch` (rewrite URLs, forward cookies cross-origin, route internally).
- `init()` — runs once at server startup (async setup, e.g. DB connections).

**Shared hooks:**

- `handleError({ error, event, status, message })` — catches unexpected runtime errors; log (e.g. Sentry) and return a safe object for `page.error`.

**Universal hooks:**

- `reroute({ url, fetch? })` — maps `url.pathname` to a different route ID without changing the address bar (can be async).
- `transport` — defines `encode`/`decode` for custom types (e.g. class instances) across server/client boundaries.

[↑ Back to Index](#index)

---

## 14. Errors

- **Expected:** `error(status, message|object)` sets the response code, renders the nearest `+error.svelte` (`page.error`), can carry extra props (e.g. `{ code: 'NOT_FOUND' }`).
- **Unexpected:** exceptions invoke `handleError`, get logged internally, expose a generic `{ message: 'Internal Error' }`; customize via `handleError`.
- Errors in server handlers / `handle` return JSON or `src/error.html` based on `Accept` headers; errors in `load` render component error boundaries.
- Type-safe error shapes via a global `App.Error` interface.

[↑ Back to Index](#index)

---

## 15. Link Options (`data-sveltekit-*`)

HTML attributes usable on any element:

| Attribute                                                                     | Effect                                                                                            |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `data-sveltekit-preload-data="hover"` \| `"tap"`                              | Preload `load` data on hover (or `touchstart`/immediate tap). Use `"tap"` for fast-changing data. |
| `data-sveltekit-preload-code="eager"` \| `"viewport"` \| `"hover"` \| `"tap"` | Preload JS/CSS more or less aggressively.                                                         |
| `data-sveltekit-reload`                                                       | Force a full-page reload.                                                                         |
| `data-sveltekit-replacestate`                                                 | Use `replaceState` instead of pushing history.                                                    |
| `data-sveltekit-keepfocus`                                                    | Retain focus after navigation.                                                                    |
| `data-sveltekit-noscroll`                                                     | Preserve scroll position.                                                                         |

Disable any of these by setting the value to `"false"`.

[↑ Back to Index](#index)

---

## 16. Server-Only Modules

- `$env/static/private` and `$env/dynamic/private` — importable **only** in server-only files (`hooks.server.js`, `+page.server.js`) — prevents leaking secrets client-side.
- `$app/server` (e.g. `read()`) is likewise server-only.
- Make your own modules server-only by naming them `*.server.js` or placing them under `src/lib/server/` — any client-reachable import chain into these triggers a build error.

[↑ Back to Index](#index)

---

## 17. Shallow Routing

Create history entries without a full navigation using `pushState(path, state)` or `replaceState('', state)` from `$app/navigation`; read/write via `page.state` from `$app/state`.

```js
if (page.state.showModal) {
	/* <Modal/> */
}
// dismiss with history.back()
```

To embed a route's page component without navigating: `preloadData(href)` → `pushState` (fallback to `goto`). Note: SSR and initial load have empty `page.state`, and shallow routing requires JS.

[↑ Back to Index](#index)

---

## 18. Images

- Vite inlines small assets, adds content hashes: `import logo from '...png'` → `<img src={logo}>`.
- **`@sveltejs/enhanced-img`** — add `enhancedImages()` to Vite config; use `<enhanced:img src="...jpg" alt="…"/>` to auto-generate `<picture>` with AVIF/WebP, responsive `srcset`/`sizes`, intrinsic dimensions.
- For CMS/dynamic images, use a CDN + library like `@unpic/svelte`. Best practices: supply 2× resolution originals, set `sizes` for LCP images, `fetchpriority="high"` on hero images, constrain layout via CSS to avoid CLS, always include meaningful `alt` text.

[↑ Back to Index](#index)

---

## 19. Import Cheat Sheet

### `@sveltejs/kit`

| Import                         | Use                                      |
| ------------------------------ | ---------------------------------------- |
| `error(status, message)`       | Throw an HTTP error, halt request        |
| `fail(status, data)`           | Return a form action failure (no throw)  |
| `isActionFailure(result)`      | Type-guard for `fail` results            |
| `isHttpError(e, status?)`      | Type-guard for `error` results           |
| `isRedirect(e)`                | Type-guard for `redirect` results        |
| `json(data)`                   | Build a JSON `Response`                  |
| `normalizeUrl(url)` _(v2.18+)_ | Strip internal suffixes/trailing slashes |
| `redirect(status, location)`   | Throw a redirect response                |
| `text(str)`                    | Build a plain-text `Response`            |

### `@sveltejs/kit/hooks`

| Import                  | Use                                      |
| ----------------------- | ---------------------------------------- |
| `sequence(...handlers)` | Compose multiple `handle` hooks into one |

### `$app/forms`

| Import                | Use                                                    |
| --------------------- | ------------------------------------------------------ |
| `applyAction(result)` | Apply an `ActionResult` to `page.form`/`page.status`   |
| `deserialize(text)`   | Parse a serialized action response into `ActionResult` |
| `enhance`             | `use:enhance` — progressive `<form>` enhancement       |

### `$app/navigation`

| Import                      | Use                                          |
| --------------------------- | -------------------------------------------- |
| `afterNavigate(cb)`         | Run code after every client-side navigation  |
| `beforeNavigate(cb)`        | Intercept/cancel upcoming navigation         |
| `disableScrollHandling()`   | Disable auto scroll-reset after navigation   |
| `goto(url, opts)`           | Programmatic navigation                      |
| `invalidate(urlOrKey)`      | Rerun loads depending on a URL/key           |
| `invalidateAll()`           | Rerun every load for current page            |
| `onNavigate(cb)`            | Hook before client-side navigation           |
| `preloadCode(route)`        | Import route modules ahead of time (no data) |
| `preloadData(route)`        | Load code + data ahead of navigation         |
| `pushState(path, state)`    | Shallow-routing history entry                |
| `replaceState(path, state)` | Replace current history entry's state        |

### `$app/paths`

| Import                     | Use                                                |
| -------------------------- | -------------------------------------------------- |
| `assets`                   | Absolute URL prefix for static assets              |
| `base`                     | App base path                                      |
| `resolveRoute(id, params)` | Interpolate a route ID with params into a pathname |

### `$app/server`

| Import                         | Use                                               |
| ------------------------------ | ------------------------------------------------- |
| `getRequestEvent()` _(v2.20+)_ | Current server `RequestEvent`                     |
| `read(fileUrl)` _(v2.4+)_      | Read a Vite-imported static asset as a `Response` |

### `$app/state`

| Import       | Use                                                            |
| ------------ | -------------------------------------------------------------- |
| `page`       | Reactive current-page info (`url`, `params`, `data`, etc.)     |
| `navigating` | Read-only in-flight navigation info (or `null`)                |
| `updated`    | Reactive new-version flag; `updated.check()` polls immediately |

### `$env/*`

| Import                 | Use                                                |
| ---------------------- | -------------------------------------------------- |
| `$env/static/private`  | Compile-time private vars, dead-code eliminated    |
| `$env/static/public`   | Compile-time public vars (`PUBLIC_…`), client-safe |
| `$env/dynamic/private` | Runtime private vars (`process.env…`), server-only |
| `$env/dynamic/public`  | Runtime public vars (`PUBLIC_…`), client-safe      |

### `$lib`

Alias for `src/lib`. `import Button from '$lib/Button.svelte'` → `src/lib/Button.svelte`.

[↑ Back to Index](#index)
