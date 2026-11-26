export const DEFAULT_BASE_URL = "https://api.sayod111.com";

export class RadarClient {
  constructor({ apiKey = null, baseUrl = DEFAULT_BASE_URL } = {}) {
    this.apiKey = apiKey ? String(apiKey).trim() : null;
    this.baseUrl = String(baseUrl).replace(/\/+$/, "");
  }

  async _req(method, path, { params = null, body = null, auth = false } = {}) {
    if (auth && !this.apiKey) throw new Error("Paid endpoint requires apiKey (dp_live_...).");
    let url = this.baseUrl + path;
    if (params) {
      const sp = new URLSearchParams();
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null && v !== "") sp.set(k, String(v));
      }
      const qs = sp.toString();
      if (qs) url += "?" + qs;
    }
    const headers = { Accept: "application/json" };
    if (this.apiKey) headers.Authorization = `Bearer ${this.apiKey}`;
    const opts = { method, headers };
    if (body !== null) {
      headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    const res = await fetch(url, opts);
    const ct = res.headers.get("content-type") || "";
    const parsed = ct.includes("application/json") ? await res.json() : await res.text();
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${JSON.stringify(parsed)}`);
    return parsed;
  }

  freshness() { return this._req("GET", "/v1/freshness"); }
  health() { return this._req("GET", "/v1/health"); }
  liveAudit(domain, mode = "shopify") { return this._req("POST", "/v1/public/live-audit", { body: { domain, mode } }); }
  riaSearch({ q = "", state = "", mismatchOnly = false, limit = 15 } = {}) {
    return this._req("GET", "/v1/public/ria-search", { params: { q, state, mismatch_only: mismatchOnly ? 1 : 0, limit } });
  }
  biotechSearch({ q = "", state = "", agency = "", limit = 15 } = {}) {
    return this._req("GET", "/v1/public/biotech-search", { params: { q, state, agency, limit } });
  }
  sample(vertical, format = "json") { return this._req("GET", `/v1/public/sample/${vertical}`, { params: { format } }); }
  me() { return this._req("GET", "/v1/me", { auth: true }); }
  radar(vertical, { limit = 50, minScore = 0, deltaOnly = false, cursor = null } = {}) {
    const params = { limit, min_score: minScore, delta_only: deltaOnly ? 1 : 0 };
    if (cursor !== null) params[vertical === "ria_wealth" ? "after_crd" : "after_id"] = cursor;
    return this._req("GET", `/v1/radar/${vertical}`, { params, auth: true });
  }
  createAlert({ feedType, targetEndpoint, cadence = "weekly" }) {
    return this._req("POST", "/v1/alerts", { body: { feed_type: feedType, delivery_channel: "webhook", target_endpoint: targetEndpoint, cadence }, auth: true });
  }
}
