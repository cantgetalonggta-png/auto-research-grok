/**
 * Server-only: resolve xAI/Grok API token via Vercel Connect.
 */
import { getToken } from '@vercel/connect';

const CANDIDATES = [
  process.env.CONNECT_GROK_UID || '',
  'grok/acme-grok',
  'api.x.ai/xai-sdk-key',
  'xai_sdk_key/ma-os-12-console',
].filter(Boolean);

export async function getGrokApiToken(opts?: {
  vercelToken?: string;
  connectorUid?: string;
}): Promise<{ token: string; connector: string }> {
  const uids = opts?.connectorUid ? [opts.connectorUid] : CANDIDATES;
  let lastErr: unknown;
  for (const uid of uids) {
    try {
      const token = await getToken(
        uid,
        { subject: { type: 'app' } },
        opts?.vercelToken ? { vercelToken: opts.vercelToken } : undefined,
      );
      return { token, connector: uid };
    } catch (e) {
      lastErr = e;
    }
  }
  throw lastErr ?? new Error('No Connect Grok connector resolved');
}

export function createGrokBearerHeaders(token: string): HeadersInit {
  return {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
}
