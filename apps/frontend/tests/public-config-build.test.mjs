import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { readFileSync, readdirSync } from 'node:fs'
import { join } from 'node:path'
import test from 'node:test'

const frontendRoot = new URL('..', import.meta.url).pathname
const distRoot = join(frontendRoot, 'dist')
const sentinels = [
  'FOUNDATION_SENTINEL_SECRET_DO_NOT_BUNDLE',
  'FOUNDATION_SENTINEL_CLS_SECRET',
  'FOUNDATION_SENTINEL_MCP_SECRET',
  'FOUNDATION_SENTINEL_MINIO_SECRET',
]

function allFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name)
    return entry.isDirectory() ? allFiles(path) : [path]
  })
}

test('sentinel secret is absent from the production browser bundle', () => {
  execFileSync('npm', ['run', 'build', '--', '--mode', 'sentinel'], {
    cwd: frontendRoot,
    stdio: 'inherit',
  })

  const bundle = allFiles(distRoot).map((file) => readFileSync(file, 'utf8')).join('\n')
  for (const sentinel of sentinels) {
    assert.equal(bundle.includes(sentinel), false)
  }
  assert.equal(bundle.includes('public-analytics-key'), true)
})
