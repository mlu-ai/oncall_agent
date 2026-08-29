import { copyFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

const root = resolve(import.meta.dirname, '..')
const config = resolve(root, 'config')

for (const name of ['project', 'user.project']) {
  const target = resolve(config, `${name}.json`)
  if (!existsSync(target)) {
    copyFileSync(resolve(config, `${name}.template.json`), target)
  }
}
