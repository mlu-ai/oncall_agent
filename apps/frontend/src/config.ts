export interface PublicConfig {
  title: string
  apiBaseUrl: string
  analyticsPublicKey: string
}

export const publicConfig: PublicConfig = __PUBLIC_PROJECT_CONFIG__
