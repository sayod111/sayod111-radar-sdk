import test from "node:test";
import assert from "node:assert/strict";
import { RadarClient } from "../index.mjs";

test("requires API key on paid route", async () => {
  const c = new RadarClient();
  await assert.rejects(() => c.me(), /requires apiKey/);
});

test("public request serialization and response", async (t) => {
  const transport = t.mock.method(globalThis, "fetch", async () => Response.json({ ok: true, data: [] }));
  const result = await new RadarClient().riaSearch({ q: "Vanguard", limit: 3 });
  const [address, options] = transport.mock.calls[0].arguments;
  const url = new URL(address);
  assert.equal(url.pathname, "/v1/public/ria-search");
  assert.equal(url.searchParams.get("q"), "Vanguard");
  assert.equal(url.searchParams.get("limit"), "3");
  assert.equal(options.method, "GET");
  assert.deepEqual(result.data, []);
});

test("live public health, riaSearch, and biotechSearch", {skip: process.env.SAYOD_LIVE_TESTS !== "1"}, async () => {
  const c = new RadarClient();
  const h = await c.health();
  assert.equal(h.ok, true);
  const r = await c.riaSearch({ q: "vanguard", limit: 3 });
  assert.equal(r.ok, true);
  const b = await c.biotechSearch({ limit: 3 });
  assert.equal(b.ok, true);
});
