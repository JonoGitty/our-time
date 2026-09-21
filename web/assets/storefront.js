/**
 * The commerce seam.
 *
 * No Shopify store exists yet, so the whole front end talks to this interface
 * and nothing else. Swapping in Shopify later means writing one more file that
 * implements the same five methods — no page, component or template changes.
 *
 * The shapes below are deliberately Shopify-shaped, because these are the
 * things that leak into a UI and are expensive to retrofit:
 *   - variants as an option set (size x colour), not a flat list
 *   - TRI-STATE inventory: a null quantity means "not tracked" => available.
 *     Treating null as 0 is the classic bug that hides your whole catalogue.
 *   - checkout is always a redirect OUT to hosted checkout. Every platform at
 *     this tier works this way; it is a constraint, not a limitation to design
 *     around.
 */
import { CATALOGUE, SIZES } from './catalogue.js';

const money = (pence) => '£' + (pence / 100).toFixed(2).replace(/\.00$/, '');

/** Deterministic pseudo-random so "sold out" states are stable across reloads. */
function seeded(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return ((h >>> 0) % 1000) / 1000;
}

function buildVariants(p) {
  return SIZES.map((size) => {
    const soldOut = p.sold.includes(size);
    return {
      id: `${p.handle}--${size}`,
      size,
      available: p.status === 'live' && !soldOut,
      // null = untracked. Renders as available with no count, never as zero.
      quantityAvailable: p.status !== 'live' ? null : soldOut ? 0 : Math.round(2 + seeded(p.handle + size) * 14),
      soldOutAt: soldOut ? soldOutStamp(p.handle + size) : null,
    };
  });
}

/* Stock written as a time, not a grey badge — it tells a returning customer how
   fast it went, which is the most persuasive social proof a small brand has. */
const DAYS = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
function soldOutStamp(seed) {
  const r = seeded(seed);
  const hh = String(18 + Math.floor(r * 6)).padStart(2, '0');
  const mm = String(Math.floor(seeded(seed + 'm') * 60)).padStart(2, '0');
  const d = Math.floor(seeded(seed + 'd') * 7);
  return `${hh}:${mm}, ${DAYS[d]} 12 OCT`;
}

const PRODUCTS = CATALOGUE.map((p, i) => ({
  ...p,
  priceFormatted: money(p.price * 100),
  priceMinor: p.price * 100,
  variants: buildVariants(p),
  // Chronological is the default sort on /shop: the collection is a ledger
  // first and a category grid second. Newest drop first.
  madeAt: 2026_09_01 - i,
}));

export class LocalAdapter {
  constructor() {
    this.cart = { id: 'local-cart', lines: [] };
    try {
      const raw = localStorage.getItem('ot.cart');
      if (raw) this.cart = JSON.parse(raw);
    } catch { /* private window, blocked storage — carry on with an empty bag */ }
  }

  #persist() {
    try { localStorage.setItem('ot.cart', JSON.stringify(this.cart)); } catch { /* non-fatal */ }
  }

  async listProducts(filter = {}) {
    let out = PRODUCTS.slice();
    if (filter.type) out = out.filter((p) => p.type === filter.type);
    if (filter.hour) out = out.filter((p) => p.hour === filter.hour);
    if (filter.status) out = out.filter((p) => p.status === filter.status);
    if (filter.sort === 'price') out.sort((a, b) => a.priceMinor - b.priceMinor);
    else out.sort((a, b) => b.madeAt - a.madeAt);   // the ledger default
    return out;
  }

  async getProduct(handle) {
    return PRODUCTS.find((p) => p.handle === handle) || null;
  }

  async addLine(variantId, qty = 1) {
    const [handle, size] = variantId.split('--');
    const product = await this.getProduct(handle);
    if (!product) throw new Error('No such product');
    const variant = product.variants.find((v) => v.size === size);
    if (!variant || !variant.available) throw new Error('That size has gone');
    const existing = this.cart.lines.find((l) => l.variantId === variantId);
    if (existing) existing.qty += qty;
    else this.cart.lines.push({ variantId, handle, size, qty, name: product.name, colour: product.colour, price: product.priceMinor, img: product.img });
    this.#persist();
    return this.cart;
  }

  async setQty(variantId, qty) {
    const line = this.cart.lines.find((l) => l.variantId === variantId);
    if (!line) return this.cart;
    if (qty <= 0) this.cart.lines = this.cart.lines.filter((l) => l.variantId !== variantId);
    else line.qty = qty;
    this.#persist();
    return this.cart;
  }

  async getCart() { return this.cart; }

  async checkoutUrl() {
    // A real adapter returns the hosted checkout URL here and the browser leaves.
    return null;
  }

  static subtotal(cart) { return cart.lines.reduce((n, l) => n + l.price * l.qty, 0); }
  static count(cart) { return cart.lines.reduce((n, l) => n + l.qty, 0); }
  static money = money;
}

export const FREE_SHIPPING_AT = 10000;   // £100, in minor units
