# OVERTIME — Commerce Seam Decision Brief

**Date:** 16 Sep 2026 · **Decision owner:** Jono (build) / cousin (business) · **Status:** platform unconfirmed, design work starting now

---

## 0. The one-line answer

Build the site as **your own front-end (path c) behind a `StorefrontAdapter` interface**, ship v1 on a **local-JSON adapter** (path d behaviour: cart permalinks / Buy Button if he wants to take money before the platform is confirmed), and swap in a **Shopify adapter** when the platform is confirmed. The catalogue should live in Shopify admin as early as possible *regardless of path*, because that admin is the thing the non-technical cousin actually operates. Full reasoning in §6.

---

## 1. The four real paths

### Comparison

| Dimension | **a. Custom Liquid theme** | **b. Hydrogen + Oxygen** | **c. Headless own front-end** | **d. Marketing site + Buy Button / cart permalinks** |
|---|---|---|---|---|
| **Design freedom** | High but inside Liquid's template model + theme-editor section contract. Glass nav, scroll video, WebGL all fine. Friction: build tooling, component model, page transitions. | Very high. React + your own components. But framework is chosen for you. | **Total.** Any framework, any renderer, any scroll/video rig, real page transitions. | High for the *marketing* pages; **zero** for PDP/cart if you use the widget — that UI is Shopify's iframe/JS, styled only within its options. |
| **Build cost now** | Medium. Learning Liquid + sections/blocks schema is real work. Can't start until the store exists. | Medium-high. Must learn Hydrogen conventions + Shopify data model on day one. **Blocks design work on a platform decision that hasn't been made.** | Medium. Highest design velocity, but you build cart/PDP logic yourself. | **Lowest.** Static site + a script tag or `/cart/<variantId>:1` links. |
| **Cost to switch platform later** | **Very high.** Templates are ~100% loss; only CSS/JS/media survive. | **Very high.** Oxygen-specific deploy, Shopify session/cart primitives, `@shopify/hydrogen` hooks all through the tree. Plus Shopify-internal framework churn (v1 React Server Components → Remix → React Router). | **Low** with the adapter: rewrite one module (~1–3 days) + re-point content. Front-end survives intact. | **Trivial.** Swap the embed. But you'll then have to *build* the commerce UX you skipped. |
| **Hosting** | Shopify (included). No DNS/CDN work. | Oxygen, included with paid Shopify plans, edge-deployed, GitHub CI/CD (secondary sources; not confirmed on a Shopify pricing page). | Netlify/Vercel/Cloudflare. Free tier realistically fine at launch. You own DNS, redirects, caching. | Wherever the static site lives. |
| **SEO** | Best defaults out of the box: sitemap, canonicals, product structured data (theme-dependent), Shopify's crawl handling. | Good, but you own sitemap/canonical/JSON-LD. | Good **if you SSR/SSG product pages.** A client-only SPA is an SEO own-goal. You own sitemap.xml, robots, canonicals, `Product` JSON-LD, and must stop the `.myshopify.com` domain duplicating you (password/noindex). | **Weakest for products.** Products rendered by a JS widget are not proper indexable product pages. Cart permalinks are better than nothing but you get no PDP. |
| **Ongoing fees** | Shopify plan only. | Shopify plan only (Oxygen included). | Shopify plan **plus** host (£0–~£16/mo) **plus** possibly a CMS (£0 on Sanity free / £0 with Shopify metaobjects). Headless does **not** save the Shopify fee. | Host (~£0) + Shopify plan. Note the £5 Starter plan is **no longer available to new stores**, so Basic is the floor. |
| **Who edits content after** | **Best.** Cousin edits products *and page layout* in the theme editor, drag-and-drop, no developer. | Products in admin; **no theme editor** — page layout needs a developer or a metaobject/CMS layer you build. | Same as (b): products in admin; site content only as editable as the `ContentAdapter` you build for him. | Products in admin; marketing pages need a developer (or a small CMS). |
| **Quarterly maintenance** | Shopify handles API versions for you. | You bump the API version each quarter. | You bump the API version each quarter — but in **one file** if the adapter is done right. | Near zero. |

### Honest notes per path

**a. Liquid theme.** The "Liquid can't look bespoke" claim is false — the design ceiling is much higher than people say, and this is genuinely the lowest-risk option *for the owner*. What you actually give up: framework choice, build DX, view transitions, and the fact that the artefact only exists inside Shopify. It also **cannot be started before the platform is confirmed**, which is disqualifying right now.

**b. Hydrogen + Oxygen.** Buys you almost nothing that (c) doesn't, and costs you the ability to leave. It is the *most* coupled option — more coupled than a Liquid theme in one sense, because it's coupled to Shopify's framework *and* Shopify's hosting *and* Shopify's opinions about all three. Its history of forced rewrites is the tell. Only sensible if Shopify were locked in **and** you wanted Shopify-supported defaults.

**c. Headless.** The cost is real and should be stated: you build PDP state, variant selection, cart drawer, error states, empty states, loading states, SEO plumbing and the content-editing story yourself. That's not nothing. But it is exactly the work you'd do anyway for an art-directed site, and none of it is platform-specific if the seam is drawn properly.

**d. Marketing + embedded checkout.** The right *interim*, not the destination. Cart permalink format is `https://<shop>.myshopify.com/cart/<variantId>:1` (Buy Button channel generates these), which means you can have a fully bespoke PDP of your own and still hand off to a real Shopify cart with one link — no SDK, no token, no API version. That is a genuinely underrated launch mode.

### Non-Shopify alternatives (one line each)

- **Stripe Checkout / Payment Links + a headless CMS** — cheapest running cost (no monthly platform fee; UK standard domestic cards 1.5% + 20p, Checkout and Payment Links included at no extra fee), total design freedom, but *you* now own inventory, variants, orders, fulfilment, returns, tax logic and the emails. Fine for a 6-SKU drop model; painful the moment he wants an operations dashboard.
- **Squarespace** — Core £17/mo annual (£24 monthly), 0% transaction fee on physical products; a good self-serve store for a non-technical owner, but the bespoke front-end would have to be abandoned or bolted on awkwardly. Not compatible with this brief.
- **Big Cartel** — free for 5 products, ~$15/mo for 50, 0% of sales; built precisely for small independent clothing labels. Genuinely the cheapest credible "real store" day one, but a thin API and a low ceiling — plan to migrate.
- **Fourthwall / print-on-demand** — no monthly fee, flat per-product base cost, card processing ~2.9% + $0.30. Removes inventory risk entirely. But OVERTIME is a *garment-dyed, washed, heavyweight* brand — POD blanks will not deliver that product, so this is a merch channel, not the brand.

> Reality check on the fee: on Shopify Basic, £19/mo annual (£25 monthly) is roughly **one tee per month**. The monthly fee is not the reason to avoid Shopify. The reason to delay Shopify is that it isn't confirmed — not that it's expensive.

---

## 2. The seam: what to build now so the front-end is genuinely portable

Two seams, not one. The site is mostly *not* commerce.

```
components/  ──▶  useCommerce()  ──▶  StorefrontAdapter  ──▶  local-json | shopify | stripe
             ──▶  useContent()   ──▶  ContentAdapter     ──▶  local-json | metaobjects | sanity
```

**Non-negotiable rules that keep the seam real:**

1. No Shopify type, and no `gid://shopify/...` string, ever appears in a component. IDs are opaque branded strings.
2. Money is never a JS `number` in the UI. One `formatMoney()`.
3. URLs are keyed on **handle**, never on ID.
4. The front-end never computes tax, shipping or final totals. It renders what the cart returns.
5. Exactly one file knows the API version string.
6. Adapters return typed results for user-visible failures; they throw only for programmer errors.
7. Both adapters pass the same conformance test suite.

### `src/commerce/domain.ts`

```ts
/** ---------- primitives ---------- */
export type CurrencyCode = "GBP" | "EUR" | "USD";

/** Integer minor units. 4500 === £45.00. Never a float, never a string in the UI. */
export interface Money {
  readonly amountMinor: number;
  readonly currencyCode: CurrencyCode;
}

type Brand<T, B> = T & { readonly __brand: B };
export type ProductId   = Brand<string, "ProductId">;
export type VariantId   = Brand<string, "VariantId">;
export type CartId      = Brand<string, "CartId">;
export type CartLineId  = Brand<string, "CartLineId">;
export type Cursor      = Brand<string, "Cursor">;
export type Handle      = Brand<string, "Handle">;   // URL key: "washed-sweat-short"

/** ---------- media (matters a lot for this brand) ---------- */
export interface VideoSource {
  url: string; mimeType: string; width: number; height: number;
}
export type MediaAsset =
  | { kind: "image";   id: string; url: string; width: number; height: number; alt: string }
  | { kind: "video";   id: string; sources: VideoSource[]; poster?: string;
      width: number; height: number; alt: string; loop?: boolean }
  | { kind: "model3d"; id: string; url: string; poster?: string; alt: string };

/** ---------- catalogue ---------- */
export interface OptionValue {
  value: string;                                   // "M" | "Washed Navy"
  swatch?: { hex?: string; image?: MediaAsset };   // colour chips, day one
}
export interface ProductOption {
  name: string;                                    // "Size" | "Colour"
  values: OptionValue[];                           // ORDERED — S,M,L,XL not alphabetical
}

export interface Variant {
  id: VariantId;
  sku: string | null;
  title: string;                                   // "M / Washed Navy"
  selectedOptions: ReadonlyArray<{ name: string; value: string }>;
  price: Money;
  compareAtPrice: Money | null;                    // non-null ⇒ render strike-through
  availableForSale: boolean;
  /** null = inventory not tracked or not exposed. null !== 0. */
  quantityAvailable: number | null;
  media: MediaAsset | null;                        // variant-specific shot
}

export interface Product {
  id: ProductId;
  handle: Handle;
  title: string;
  descriptionHtml: string;
  vendor: string | null;
  tags: ReadonlyArray<string>;
  media: ReadonlyArray<MediaAsset>;                // gallery, in display order
  options: ReadonlyArray<ProductOption>;
  variants: ReadonlyArray<Variant>;
  priceRange: { min: Money; max: Money };
  availableForSale: boolean;                       // any variant available
  seo: { title: string; description: string };
  publishedAt: string | null;                      // ISO
}

export interface Collection {
  id: string;
  handle: Handle;
  title: string;
  descriptionHtml: string;
  image: MediaAsset | null;
  seo: { title: string; description: string };
}

export interface Page<T> {
  items: ReadonlyArray<T>;
  nextCursor: Cursor | null;                       // cursor paging, not offsets
}

/** ---------- cart ---------- */
export interface CartLineInput {
  variantId: VariantId;
  quantity: number;
  /** line-item attributes: gift note, size-run, drop id, "runs large" ack */
  attributes?: Readonly<Record<string, string>>;
}
export interface CartLine {
  id: CartLineId;
  variantId: VariantId;
  productHandle: Handle;
  title: string;
  variantTitle: string;
  image: MediaAsset | null;
  quantity: number;
  attributes: Readonly<Record<string, string>>;
  unitPrice: Money;
  lineTotal: Money;
  compareAtUnitPrice: Money | null;
}
export interface AppliedDiscount { code: string; applicable: boolean }

export interface Cart {
  id: CartId;
  lines: ReadonlyArray<CartLine>;
  totalQuantity: number;
  cost: {
    subtotal: Money;
    /** null until the platform knows — do NOT invent these client-side */
    tax: Money | null;
    shipping: Money | null;
    total: Money;
  };
  discountCodes: ReadonlyArray<AppliedDiscount>;
  attributes: Readonly<Record<string, string>>;
  /** Present only when a real hosted checkout exists. */
  checkoutUrl: string | null;
}

/** ---------- results & errors ---------- */
export type CommerceErrorCode =
  | "OUT_OF_STOCK" | "QUANTITY_UNAVAILABLE" | "DISCOUNT_INVALID"
  | "LINE_NOT_FOUND" | "CART_EXPIRED" | "NETWORK" | "UNKNOWN";

export interface CommerceError {
  code: CommerceErrorCode;
  message: string;      // safe to show a customer
  field?: string;
}

export type CartResult =
  | { ok: true;  cart: Cart }
  | { ok: false; cart: Cart; errors: ReadonlyArray<CommerceError> };

/** Checkout is ALWAYS a handoff. Model it as one from day one. */
export type CheckoutHandoff =
  | { kind: "redirect"; url: string }
  | { kind: "unavailable"; reason: "not-launched" | "no-payment-provider" | "cart-empty";
      message: string };

/** Lets the UI be honest instead of faking features the current backend lacks. */
export interface Capabilities {
  realInventory: boolean;
  discountCodes: boolean;
  search: boolean;
  customerAccounts: boolean;
  checkout: "redirect" | "none";
}
```

### `src/commerce/adapter.ts`

```ts
import type * as D from "./domain";

export type ProductSort = "manual" | "newest" | "price-asc" | "price-desc" | "best-selling";

export interface StorefrontAdapter {
  readonly id: string;                       // "local" | "shopify" | "stripe"
  readonly capabilities: D.Capabilities;

  /* catalogue */
  listProducts(opts?: {
    first?: number; after?: D.Cursor | null;
    collection?: D.Handle; sort?: ProductSort;
  }): Promise<D.Page<D.Product>>;
  getProduct(handle: D.Handle): Promise<D.Product | null>;
  listCollections(opts?: { first?: number; after?: D.Cursor | null }): Promise<D.Page<D.Collection>>;
  getCollection(handle: D.Handle): Promise<D.Collection | null>;
  search(query: string, opts?: { first?: number }): Promise<D.Page<D.Product>>;

  /* cart — always adapter-owned, never reconstructed client-side */
  createCart(lines?: ReadonlyArray<D.CartLineInput>): Promise<D.CartResult>;
  getCart(id: D.CartId): Promise<D.Cart | null>;
  addLines(id: D.CartId, lines: ReadonlyArray<D.CartLineInput>): Promise<D.CartResult>;
  updateLines(id: D.CartId,
    updates: ReadonlyArray<{ lineId: D.CartLineId; quantity: number }>): Promise<D.CartResult>;
  removeLines(id: D.CartId, lineIds: ReadonlyArray<D.CartLineId>): Promise<D.CartResult>;
  applyDiscountCodes(id: D.CartId, codes: ReadonlyArray<string>): Promise<D.CartResult>;
  updateCartAttributes(id: D.CartId, attrs: Record<string, string>): Promise<D.CartResult>;

  /* handoff */
  beginCheckout(id: D.CartId): Promise<D.CheckoutHandoff>;
}

/** Where the cart id lives. Swappable: httpOnly cookie (SSR) or localStorage (static). */
export interface CartStore {
  read(): Promise<D.CartId | null>;
  write(id: D.CartId): Promise<void>;
  clear(): Promise<void>;
}
```

### `src/commerce/adapters/local.ts` (today)

```ts
import catalogue from "../../../content/catalogue.json";   // same shape the Shopify adapter emits
import type { StorefrontAdapter } from "../adapter";
import type * as D from "../domain";

const carts = new Map<D.CartId, D.Cart>();   // swap for KV/Redis if you want it to survive reloads

export function createLocalAdapter(opts: { checkout?: "permalink" | "none" } = {}): StorefrontAdapter {
  const products = catalogue.products as unknown as D.Product[];
  const byHandle = new Map(products.map(p => [p.handle, p]));

  return {
    id: "local",
    capabilities: {
      realInventory: false,          // stock flags in JSON are fiction, and the UI says so
      discountCodes: false,
      search: true,
      customerAccounts: false,
      checkout: opts.checkout === "permalink" ? "redirect" : "none",
    },

    async getProduct(handle) { return byHandle.get(handle) ?? null; },

    async listProducts({ first = 24, collection, sort = "manual" } = {}) {
      let items = collection
        ? products.filter(p => p.tags.includes(`collection:${collection}`))
        : products;
      items = sortProducts(items, sort).slice(0, first);
      return { items, nextCursor: null };
    },

    // …collections / search elided…

    async createCart(lines = []) {
      const cart = emptyCart(newId());
      carts.set(cart.id, cart);
      return this.addLines(cart.id, lines);
    },

    async addLines(id, lines) {
      const cart = carts.get(id);
      if (!cart) return fail(emptyCart(id), "CART_EXPIRED", "Your bag expired. Start again.");
      const next = recompute({ ...cart, lines: mergeLines(cart.lines, lines, byHandle) });
      carts.set(id, next);
      return { ok: true, cart: next };
    },

    async applyDiscountCodes(id, _codes) {
      const cart = carts.get(id)!;
      return fail(cart, "DISCOUNT_INVALID", "Discount codes go live with the store.");
    },

    async beginCheckout(id) {
      const cart = carts.get(id);
      if (!cart || cart.lines.length === 0)
        return { kind: "unavailable", reason: "cart-empty", message: "Your bag is empty." };
      if (opts.checkout !== "permalink")
        return { kind: "unavailable", reason: "not-launched",
                 message: "OVERTIME opens soon. Join the list for the drop." };
      // interim path (d): real Shopify cart, zero SDK, zero token
      const pairs = cart.lines.map(l => `${l.variantId}:${l.quantity}`).join(",");
      return { kind: "redirect",
               url: `https://${import.meta.env.PUBLIC_SHOP_DOMAIN}/cart/${pairs}` };
    },

    // …getCart / updateLines / removeLines / updateCartAttributes…
  } as StorefrontAdapter;
}
```

Note what this buys you: **the "sold out" state, the discount-code failure state, the empty-bag state and the checkout-unavailable state are all exercised in the real UI before Shopify exists.** Those are exactly the states that get skipped and then blow up on launch day.

### `src/commerce/adapters/shopify.ts` (later — sketch)

```ts
export const SHOPIFY_API_VERSION = "2026-07";   // the ONLY place this string exists

const ENDPOINT = (domain: string) =>
  `https://${domain}/api/${SHOPIFY_API_VERSION}/graphql.json`;

async function sf<T>(q: string, variables: Record<string, unknown>): Promise<T> {
  const res = await fetch(ENDPOINT(SHOP_DOMAIN), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // PUBLIC token → safe in the browser. Private token → server only,
      // and then you MUST also send "Shopify-Storefront-Buyer-IP".
      "X-Shopify-Storefront-Access-Token": PUBLIC_STOREFRONT_TOKEN,
    },
    body: JSON.stringify({ query: q, variables }),
  });
  const json = await res.json();
  if (json.errors?.length) throw new Error(json.errors[0].message);
  return json.data as T;
}

/** Shopify Money: { amount: "45.00", currencyCode: "GBP" } → minor units. */
const toMoney = (m: { amount: string; currencyCode: string }): Money => ({
  amountMinor: Math.round(parseFloat(m.amount) * 100),
  currencyCode: m.currencyCode as CurrencyCode,
});

// Every gid:// is cast to a branded id HERE and nowhere else:
const pid = (gid: string) => gid as ProductId;

async function beginCheckout(id: CartId): Promise<CheckoutHandoff> {
  const { cart } = await sf<{ cart: { checkoutUrl: string } | null }>(CART_QUERY, { id });
  return cart
    ? { kind: "redirect", url: cart.checkoutUrl }     // hosted checkout. Always.
    : { kind: "unavailable", reason: "cart-empty", message: "Your bag is empty." };
}
```

### The thing that makes the seam true rather than aspirational

```ts
// src/commerce/conformance.ts — run against EVERY adapter in CI
export function runAdapterConformance(name: string, make: () => Promise<StorefrontAdapter>) {
  describe(`StorefrontAdapter conformance: ${name}`, () => {
    it("every product has ≥1 variant and every variant covers every option", async () => { /* … */ });
    it("option values are display-ordered, not alphabetical", async () => { /* … */ });
    it("compareAtPrice is null or strictly greater than price", async () => { /* … */ });
    it("adding an unavailable variant returns ok:false, not a throw", async () => { /* … */ });
    it("quantity 0 removes the line", async () => { /* … */ });
    it("line attributes survive a round trip", async () => { /* … */ });
    it("cost.total is never a number the UI computed", async () => { /* … */ });
    it("beginCheckout on an empty cart returns kind:'unavailable'", async () => { /* … */ });
  });
}
```

When the Shopify adapter passes this suite, the swap is done. That is the whole insurance policy, and it costs about a day to write.

### Second seam: `ContentAdapter`

```ts
export interface ContentAdapter {
  getPage(slug: string): Promise<PageContent | null>;         // /about, /returns
  getHomeSections(): Promise<Section[]>;                      // hero video, lookbook, marquee
  getLookbook(handle: string): Promise<Lookbook | null>;      // AI model shots
  getSiteSettings(): Promise<SiteSettings>;                   // announcement bar, nav, socials
}
```
Today: `content/*.json` in the repo. Later: Shopify **metaobjects** (available on all plans, editable by a non-technical merchant in admin) or Sanity (free tier is generous enough for this). This is what gives the cousin self-serve control over the homepage without a theme editor — see §5.

---

## 3. Shopify concepts that leak into the front-end (model them now, on fake data)

These are the things that, if you fake them wrongly today, force a redesign later:

1. **Variants are the sellable unit, not products.** Every "add to bag" targets a `VariantId`. Size × Colour = a variant matrix, and **the matrix is sparse** — Washed Navy may exist in M/L/XL but not S. Your size selector must handle "this combination does not exist" as distinct from "sold out". Build the option → variant resolver now.
2. **Option ordering is editorial.** S/M/L/XL is not alphabetical and Shopify preserves merchant order. Never sort option values in the UI.
3. **Inventory tri-state.** `availableForSale: false` (sold out) vs `quantityAvailable: 3` (low stock, drives "3 left" urgency copy) vs `quantityAvailable: null` (not tracked). Treating null as 0 is the classic bug.
4. **`compareAtPrice`** drives every strike-through / "was £X" badge. If you didn't model it, sale layout has nowhere to go.
5. **Media galleries are a union, in merchant order, with variant association.** Image, video (multiple sources + poster) and 3D model. For OVERTIME specifically, the AI-generated model videos and the flat-lays live in the same gallery — the gallery component must be video-native from the first commit, not retrofitted.
6. **Collections are the navigation.** "Shop All", "Tees", "Shorts", "The Time Drop" are collections with their own handle, title, description, image and SEO. Fake them as collections, not as tag filters, or the nav rebuilds later.
7. **Cart lines ≠ variants.** A line has its own `CartLineId` and its own **attributes** (key/value). Line-item attributes are how you carry a gift note, a drop id, or a "runs oversized — acknowledged" flag through to the order. Also cart-level attributes. Cheap now, invasive later.
8. **Discount codes are server-validated and can fail.** The UI needs an "invalid code" state and an "applied but not applicable" state (`applicable: false`) from day one.
9. **Checkout is always a redirect.** `cart.checkoutUrl` hands the buyer to Shopify's hosted checkout. On Basic/Grow/Advanced you can change checkout logo/colours/fonts in the checkout editor and add app blocks on the thank-you and order-status pages — **you cannot add fields or logic to the information/shipping/payment steps.** The Checkout Branding API and inner-checkout app blocks are **Plus-only**. Design accordingly: the last fully-branded surface you control is the cart drawer. Make it count, and make the visual handoff to Shopify checkout as soft as possible (matching type, colours, logo in the checkout editor).
10. **Prices are money objects with a currency**, not numbers — and if he ever sells outside the UK, Shopify Markets changes prices per buyer context. Currency on every `Money` today costs nothing.

---

## 4. Storefront API practicalities (2026)

- **Token safety.** The **public access token** is designed to be visible to buyers and is safe in client-side code, sent as `X-Shopify-Storefront-Access-Token`. It has a limited feature set — products, collections, cart, search, pages. The **private access token** (`Shopify-Storefront-Private-Token`) is a secret, **server-only**, and unlocks metaobjects, menus and customer data; when you proxy buyer traffic with it you must also send the case-sensitive `Shopify-Storefront-Buyer-IP` header or you'll trip bot protection. Max 100 active private tokens per shop. ([auth docs](https://shopify.dev/docs/api/storefront))
  - **Architectural consequence:** if site content lives in **metaobjects**, the front-end needs a server/edge runtime. That rules out a purely static, token-in-the-browser build. Decide this before choosing Astro-static vs Astro-SSR/Next.
- **Cart API, not Checkout API.** The Checkout APIs (Storefront checkout mutations + REST checkout endpoints) were deprecated in 2024-04 and **shut down on 1 April 2025**. The replacement is the Storefront **Cart API**, and the `Cart` object's required `checkoutUrl` field is the documented way to "direct buyers to Shopify's web checkout to complete their purchase." Do not write `checkoutCreate`. ([changelog](https://shopify.dev/changelog/checkout-apis-will-be-shut-down-april-1-2025), [Cart object](https://shopify.dev/docs/api/storefront/latest/objects/Cart))
- **Rate limits.** The Storefront API is *not* request-per-minute limited for real buyer traffic; it rate-limits automated traffic (bots/crawlers), with the strictest limits for unsigned anonymous bots — operators can request higher limits via Web Bot Auth. Tokenless access carries a **query complexity limit of 1,000** (same cost model as the Admin GraphQL API), and exceeding it returns `MAX_COMPLEXITY_EXCEEDED`. Public-token capacity scales with buyer count **by IP**. There is a separate **checkout-level throttle** on checkouts created per minute (returns `200 Throttled`). Malicious requests get `430 Shopify Security Rejection`. ([limits](https://shopify.dev/docs/api/usage/limits))
  - Practical upshot for a drop-based streetwear brand: a drop spike is a **checkout-creation** spike, not a query spike. Cache product/collection queries hard at the edge; do not cache cart.
- **Versioning cadence.** New API version **every three months**, 5pm UTC on the first day of the quarter, date-named (`2026-07`). Each stable version is supported **at least 12 months**, with **≥9 months overlap**. Latest stable is **2026-07**; **2026-10** lands 1 Oct 2026. Shopify recommends updating each quarter and always pinning a version explicitly. ([versioning](https://shopify.dev/docs/api/usage/versioning)) → This is a recurring ~1 hour/quarter job that the cousin cannot do. Keeping it to one constant in one file is the mitigation.
- **Customer accounts.** The Customer Account API (OAuth + PKCE) is Shopify's **recommended** route for customer data since Jan 2024. Secondary sources claim the Storefront API's password-based `customerAccessTokenCreate` was removed in 2026-01 — **UNVERIFIED and contradicted** by Shopify's own customer-accounts guide, which still documents it. Either way: **don't build customer accounts in v1.** A clothing drop needs guest checkout and an email list, not a login.

---

## 5. UK practicalities for a new clothing label

**VAT.** Registration threshold is **£90,000** taxable turnover over a rolling 12 months (or if you expect to exceed it in the next 30 days). Below that, don't register — for a B2C brand, voluntary registration means either adding 20% to the price or eating it. Adult clothing is **standard-rated at 20%**; young children's clothing and footwear is **zero-rated** under VAT Notice 714 (relevant only if OVERTIME ever does kids' sizes — and the size thresholds are specific, so check before assuming an XS youth tee qualifies). Set Shopify to **tax-inclusive display** for the UK: £45 must mean £45 at the checkout, or conversion dies.

**Shopify plan cost (UK, from shopify.com/uk/pricing):**

| Plan | Monthly billing | Annual billing | UK online card rate | 3rd-party gateway fee |
|---|---|---|---|---|
| Basic | £25/mo | £19/mo | 2% + 25p | 2% |
| Grow | £65/mo | £49/mo | 1.7% + 25p | 1% |
| Advanced | £344/mo | £259/mo | 1.5% + 25p | 0.6% |
| Plus | from £1,800/mo | — | 1.3% + 25p | 0.2% |

Intro offer: 3 days free then **£1/month for 3 months**. The **£5 Starter plan is closed to new stores**, so Basic is the entry point. **Start on Basic, monthly** — don't lock a year in before the first drop sells.

**Payments.** If on Shopify, use **Shopify Payments** — the 2% third-party gateway penalty on Basic makes anything else uneconomic. Add PayPal (still meaningful for UK 18–30) and consider Klarna/Clearpay for a £45–£120 AOV streetwear basket (*rates UNVERIFIED*). If **not** on Shopify: Stripe direct is 1.5% + 20p UK standard domestic, 2.5% + 20p EEA, 3.15% + 20p international, +2% on currency conversion; Checkout and Payment Links included at no extra fee.

**Also needed and usually forgotten (general UK distance-selling requirements — specifics UNVERIFIED this session):** 14-day right-to-cancel / returns policy, trading name and contact address on the site, terms of sale, privacy policy and cookie consent for any analytics.

**What the cousin must be able to do without ringing you** — this list should drive the architecture, not the other way round:

| Task | Where it happens | Works headless? |
|---|---|---|
| Add a product, set price, upload photos/videos | Shopify admin | ✅ yes, identical |
| Create size/colour variants, set stock | Shopify admin | ✅ yes |
| Mark sold out / restock | Shopify admin | ✅ yes |
| Create a discount code | Shopify admin | ✅ yes |
| See orders, print labels, refund | Shopify admin | ✅ yes |
| Change the announcement bar / nav / homepage hero video | **theme editor (a) vs your ContentAdapter (b/c)** | ⚠️ only if you build it |
| Reorder homepage sections, add a new landing page | **theme editor only** | ❌ developer job |

**That table is the whole non-technical-owner question.** 90% of what he does daily is Shopify admin and is *path-independent*. The only real loss from going headless is page composition. Mitigate it deliberately: put the announcement bar, nav links, homepage section order, hero video, lookbook and drop countdown into **metaobjects** (all plans, admin-editable) behind the `ContentAdapter`, and write him a one-page "what you can change yourself, and what needs Jono" note. Don't pretend the loss isn't real — budget a day for it.

---

## 6. Recommendation

**Build path (c) — your own front-end behind a `StorefrontAdapter` — and launch on the local-JSON adapter with a (d)-style cart-permalink handoff if he wants to take money before the platform is confirmed.**

Reasoning, weighted against the actual constraints:

1. **The platform is unconfirmed, and paths (a) and (b) require confirming it before design starts.** That alone eliminates them for the work happening *now*. The adapter lets design and build start today with zero platform risk.
2. **The design is the product.** OVERTIME's differentiation is art direction — liquid-glass nav, AI-video scroll sequences, the time motif. That work is 80–90% of the effort and, behind the seam, **100% of it survives any platform decision.** The commerce integration is the small, replaceable part. Architect so the expensive thing is the portable thing.
3. **The AI video and "3D flair" push away from Shopify hosting.** Scroll-driven video, custom easing, view transitions and WebGL want your own build pipeline and your own CDN. Put hero/lookbook video on a proper video CDN (Cloudflare Stream / Mux / Bunny, or pre-encoded MP4+HLS on your host) rather than Shopify Files; keep *product* media in Shopify so the cousin can upload it. Blender is indeed overkill — the brief is image→video, which is an AI-video + compositing job, not a 3D job.
4. **The non-technical owner is handled by Shopify admin, not by the front-end.** Products, prices, photos, stock, discounts, orders and refunds all live in admin regardless of path. Get the catalogue into a Shopify store **early** — even on the £1/month intro — so he starts learning the admin while the site is being designed, and so your `catalogue.json` is generated from real data rather than invented.
5. **Switching cost is the asymmetry.** If Shopify is confirmed: write one adapter, ~1–3 days, front-end untouched. If he lands on Stripe + CMS, or Big Cartel, or wants a POD merch line alongside: write a different adapter, same cost. Compare that with a Liquid theme or a Hydrogen app, where a platform change is a rebuild. You are buying optionality for about two days of work.
6. **Hydrogen/Oxygen is rejected explicitly.** It is the maximum-lock-in option, its framework has been rewritten under its users twice, "free hosting" is worth ~£0–16/month, and it gives you nothing that (c) doesn't. Unless the cousin signs for Shopify *and* you want Shopify's support burden, it's the wrong trade.
7. **The one honest argument against this recommendation:** if the cousin turns out to want to re-lay-out pages himself weekly, a custom Liquid theme genuinely wins, and you'd be fighting the architecture forever. So set a decision gate.

### The plan, concretely

| Stage | Work | Gate |
|---|---|---|
| **Now** | Domain types + `StorefrontAdapter` + `ContentAdapter` + local-JSON adapter + conformance suite. ~2–3 days. Then all design/build work proceeds against fake-but-correctly-shaped data. | — |
| **Now+** | Open a Shopify store on the £1/3-month intro. Load real products, real variants, real photos. Generate `catalogue.json` from it. Cousin starts using the admin. | — |
| **Pre-launch** | Ship the bespoke site with the local adapter; `beginCheckout` returns either a **cart permalink** to the real Shopify cart (sell immediately, zero API surface) or an honest "opens soon + join the list". | **Gate 1:** does he actually want to re-lay-out pages himself? If yes → seriously re-cost a Liquid theme *before* building the ContentAdapter. |
| **Platform confirmed** | Write the Shopify adapter (Storefront API `2026-07`+, public token in the browser or private token server-side if you need metaobjects; Cart API; `cart.checkoutUrl`). Pass the conformance suite. Flip one factory function. | **Gate 2:** conformance green + a real £1 test order end-to-end. |
| **Ongoing** | Bump `SHOPIFY_API_VERSION` once a quarter. Brand the Shopify hosted checkout in the checkout editor to soften the handoff. | — |

### Explicit non-goals for v1
Customer accounts/login. Custom checkout UI (impossible below Plus anyway). Multi-currency/Markets. Subscriptions. Wishlist. Live inventory counters on the grid.

---

**Sources:** [Shopify UK pricing](https://www.shopify.com/uk/pricing) · [Shopify Starter plan (closed to new stores)](https://help.shopify.com/en/manual/intro-to-shopify/pricing-plans/plans-features/shopify-starter-plan) · [Storefront API auth & limits](https://shopify.dev/docs/api/storefront) · [Shopify API limits](https://shopify.dev/docs/api/usage/limits) · [API versioning](https://shopify.dev/docs/api/usage/versioning) · [Cart object / checkoutUrl](https://shopify.dev/docs/api/storefront/latest/objects/Cart) · [Checkout APIs shut down 1 Apr 2025](https://shopify.dev/changelog/checkout-apis-will-be-shut-down-april-1-2025) · [Customer accounts with the Storefront API](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api/customer-accounts) · [Cart permalinks](https://help.shopify.com/en/manual/checkout-settings/cart-permalink) · [Buy Button](https://help.shopify.com/en/manual/online-sales-channels/buy-button) · [UK VAT registration threshold](https://www.gov.uk/vat-registration/when-to-register) · [VAT Notice 714 (children's clothing)](https://www.gov.uk/guidance/vat-on-young-childrens-clothing-and-footwear-notice-714) · [Stripe UK pricing](https://stripe.com/gb/pricing) · [Squarespace pricing (secondary)](https://www.expertsure.com/uk/web-design/squarespace-pricing-uk/) · [Big Cartel pricing (secondary)](https://www.stylefactoryproductions.com/big-cartel-review) · [Fourthwall pricing (secondary)](https://fourthwall.com/pricing) · [Hydrogen/Oxygen inclusion & version (secondary)](https://www.charleagency.com/articles/shopify-hydrogen-oxygen/) · [Checkout customisation by plan (secondary)](https://www.shopify.com/enterprise/blog/customize-shopify-checkout) · [Metaobjects on all plans (secondary)](https://mgroupweb.com/blogs/shopify-metaobjects-guide/)

**UNVERIFIED flags:** Oxygen "free on all paid plans, unlimited bandwidth" and Hydrogen's React Router v7 basis (secondary sources only, not confirmed on a Shopify pricing/docs page); `checkout.liquid` sunset date of 28 Aug 2025 (secondary); the claim that `customerAccessTokenCreate` was removed in 2026-01 (secondary, and contradicted by Shopify's own docs); Klarna/Clearpay UK rates; UK distance-selling specifics (14-day cancellation etc.) stated from general knowledge, not checked this session.