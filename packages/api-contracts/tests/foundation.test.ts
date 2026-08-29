import { isFoundationHealth } from '../src/index'

describe('isFoundationHealth', () => {
  it('accepts the minimum health payload', () => {
    expect(isFoundationHealth({ status: 'ok' })).toBe(true)
  })

  it('rejects unknown payloads', () => {
    expect(isFoundationHealth({ status: 'down' })).toBe(false)
  })
})
