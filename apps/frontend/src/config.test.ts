import { publicConfig } from './config'

describe('publicConfig', () => {
  it('exposes only approved browser configuration fields', () => {
    expect(publicConfig).toEqual({
      title: '哨兵前端',
      apiBaseUrl: 'https://api.example.test',
      analyticsPublicKey: 'public-analytics-key',
    })
  })
})
