import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue }
type JsonObject = { [key: string]: JsonValue }

const frontendRoot = fileURLToPath(new URL('.', import.meta.url))
const repositoryRoot = resolve(frontendRoot, '../..')

function asObject(value: JsonValue): JsonObject {
  return typeof value === 'object' && value !== null && !Array.isArray(value) ? value : {}
}

function readObject(path: string): JsonObject {
  return asObject(JSON.parse(readFileSync(path, 'utf8')) as JsonValue)
}

function deepMerge(base: JsonObject, override: JsonObject): JsonObject {
  const merged: JsonObject = { ...base }
  for (const [key, overrideValue] of Object.entries(override)) {
    const baseValue = merged[key]
    merged[key] =
      typeof baseValue === 'object' &&
      baseValue !== null &&
      !Array.isArray(baseValue) &&
      typeof overrideValue === 'object' &&
      overrideValue !== null &&
      !Array.isArray(overrideValue)
        ? deepMerge(asObject(baseValue), asObject(overrideValue))
        : overrideValue
  }
  return merged
}

function publicConfigFor(mode: string): { title: string; apiBaseUrl: string; analyticsPublicKey: string } {
  const configDir =
    mode === 'test' || mode === 'sentinel'
      ? resolve(frontendRoot, 'tests/fixtures/sentinel-config')
      : resolve(repositoryRoot, 'config')
  const project = readObject(resolve(configDir, 'project.json'))
  let merged = project
  try {
    merged = deepMerge(project, readObject(resolve(configDir, 'user.project.json')))
  } catch (error) {
    if (!(error instanceof Error) || !error.message.includes('ENOENT')) {
      throw error
    }
  }
  const frontend = asObject(merged.frontend ?? {})
  const analytics = asObject(frontend.analytics ?? {})
  return {
    title: typeof frontend.title === 'string' ? frontend.title : '',
    apiBaseUrl: typeof frontend.apiBaseUrl === 'string' ? frontend.apiBaseUrl : '',
    analyticsPublicKey: typeof analytics.publicKey === 'string' ? analytics.publicKey : '',
  }
}

export default defineConfig(({ mode }) => ({
  plugins: [vue()],
  define: {
    __PUBLIC_PROJECT_CONFIG__: JSON.stringify(publicConfigFor(mode)),
  },
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['src/**/*.test.ts'],
  },
}))
