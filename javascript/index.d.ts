export declare const DEFAULT_BASE_URL: string;
export declare class RadarClient {
  constructor(opts?: { apiKey?: string | null; baseUrl?: string });
  health(): Promise<any>;
  freshness(): Promise<unknown>;
  liveAudit(domain: string, mode?: "shopify" | "trust" | "dmarc"): Promise<any>;
  riaSearch(opts?: { q?: string; state?: string; mismatchOnly?: boolean; limit?: number }): Promise<any>;
  biotechSearch(opts?: { q?: string; state?: string; agency?: string; limit?: number }): Promise<any>;
  sample(vertical: "ecom_radar" | "cyber_grc" | "ria_wealth" | "biotech_radar", format?: "json" | "csv"): Promise<any>;
  me(): Promise<any>;
  radar(vertical: "ecom_radar" | "cyber_grc" | "ria_wealth" | "biotech_radar", opts?: { limit?: number; minScore?: number; deltaOnly?: boolean; cursor?: string | number | null }): Promise<any>;
  createAlert(opts: { feedType: string; targetEndpoint: string; cadence?: "weekly" | "daily" }): Promise<any>;
}
