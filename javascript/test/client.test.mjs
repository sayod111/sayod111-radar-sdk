import test from "node:test";
import assert from "node:assert/strict";
import { RadarClient } from "../index.mjs";

test("requires API key on paid route", async () => {
  const c = new RadarClient();
  await assert.rejects(() => c.me(), /requires apiKey/);
});

test("live public health, riaSearch, and biotechSearch", async () => {
  const c = new RadarClient();
  const h = await c.health();
  assert.equal(h.ok, true);
  const r = await c.riaSearch({ q: "vanguard", limit: 3 });
  assert.equal(r.ok, true);
  const b = await c.biotechSearch({ limit: 3 });
  assert.equal(b.ok, true);
});
