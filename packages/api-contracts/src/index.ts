export interface FoundationHealth {
  status: 'ok'
}

export function isFoundationHealth(value: unknown): value is FoundationHealth {
  return typeof value === 'object' && value !== null && (value as { status?: unknown }).status === 'ok'
}
