# Template — Unit Test com Jest / Vitest (JavaScript / TypeScript)

> **[TEMPLATE] Como usar este arquivo**
>
> Copie para `src/__tests__/<nome>.test.ts` ou `<nome>.spec.ts` no seu projeto.
> Substitua todos os blocos `[PREENCHA]` com o conteúdo real.
> Spec de referência: `[PREENCHA: caminho do spec em docs/specs/]`
>
> Compatível com Jest e Vitest — a API é idêntica.

---

```typescript
/**
 * Testes unitários para [PREENCHA: nome do módulo/função].
 * Spec de referência: docs/specs/[PREENCHA: nome-do-spec.md]
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
// ou: import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals'

// [PREENCHA: importe o módulo sendo testado]
// import { AuthService } from '../services/auth'


// ─────────────────────────────────────────────
// SETUP / TEARDOWN
// ─────────────────────────────────────────────

let [PREENCHA_instancia]: [PREENCHA_Tipo]

beforeEach(() => {
  // Arrange global — executado antes de cada teste
  [PREENCHA_instancia] = new [PREENCHA_Classe]()
})

afterEach(() => {
  // Limpa mocks entre testes
  vi.clearAllMocks()
})


// ─────────────────────────────────────────────
// CASO FELIZ
// ─────────────────────────────────────────────

describe('[PREENCHA: nome do comportamento sendo testado]', () => {

  it('[PREENCHA: descreva o comportamento esperado em linguagem natural]', async () => {
    /**
     * CA: [PREENCHA: cole o critério de aceite do spec]
     */
    // Arrange
    const [PREENCHA_entrada] = [PREENCHA]

    // Act
    const resultado = await [PREENCHA_instancia].[PREENCHA_metodo]([PREENCHA_entrada])

    // Assert
    expect(resultado).toEqual([PREENCHA_valor_esperado])
  })


  // ─────────────────────────────────────────────
  // CASOS DE ERRO
  // ─────────────────────────────────────────────

  it('deve lançar erro quando [PREENCHA: condição de erro]', async () => {
    /**
     * CA: [PREENCHA: critério de aceite de falha do spec]
     */
    // Arrange
    const [PREENCHA_entrada_invalida] = [PREENCHA]

    // Act + Assert
    await expect(
      [PREENCHA_instancia].[PREENCHA_metodo]([PREENCHA_entrada_invalida])
    ).rejects.toThrow('[PREENCHA: mensagem de erro esperada]')
  })


  it('deve retornar [PREENCHA: status] quando [PREENCHA: condição]', async () => {
    /**
     * CA: [PREENCHA: critério de aceite]
     */
    // Arrange
    const [PREENCHA] = [PREENCHA]

    // Act
    const resultado = await [PREENCHA]

    // Assert
    expect(resultado.status).toBe([PREENCHA])
    expect(resultado.message).toBe('[PREENCHA]')
  })


  // ─────────────────────────────────────────────
  // CASOS DE BORDA
  // ─────────────────────────────────────────────

  it('deve [PREENCHA: comportamento de borda] quando [PREENCHA: condição de borda]', async () => {
    /**
     * Caso de borda: [PREENCHA: descreva]
     */
    // Arrange
    const [PREENCHA] = [PREENCHA]

    // Act
    const resultado = await [PREENCHA]

    // Assert
    expect([PREENCHA]).toBe([PREENCHA])
  })
})


// ─────────────────────────────────────────────
// TESTES COM MOCK
// ─────────────────────────────────────────────

describe('[PREENCHA: nome do comportamento com dependência mockada]', () => {

  it('[PREENCHA: comportamento]', async () => {
    /**
     * CA: [PREENCHA]
     * Dependência mockada: [PREENCHA: qual e por quê]
     */
    // Arrange
    const mock[PREENCHA] = vi.fn().mockResolvedValue([PREENCHA])
    // ou para jest: const mock[PREENCHA] = jest.fn().mockResolvedValue([PREENCHA])

    // Act
    const resultado = await [PREENCHA_instancia].[PREENCHA_metodo](mock[PREENCHA])

    // Assert
    expect(resultado).toEqual([PREENCHA])
    expect(mock[PREENCHA]).toHaveBeenCalledWith([PREENCHA])
    expect(mock[PREENCHA]).toHaveBeenCalledTimes(1)
  })
})


// ─────────────────────────────────────────────
// TEST.EACH — múltiplos cenários
// ─────────────────────────────────────────────

describe('[PREENCHA: comportamento com múltiplos cenários]', () => {

  it.each([
    { entrada: [PREENCHA], esperado: [PREENCHA], descricao: '[PREENCHA]' },
    { entrada: [PREENCHA], esperado: [PREENCHA], descricao: '[PREENCHA]' },
    { entrada: [PREENCHA], esperado: [PREENCHA], descricao: '[PREENCHA]' },
  ])('$descricao', async ({ entrada, esperado }) => {
    /**
     * CA: [PREENCHA: critério de aceite que cobre múltiplos cenários]
     */
    // Act
    const resultado = await [PREENCHA_instancia].[PREENCHA_metodo](entrada)

    // Assert
    expect(resultado).toEqual(esperado)
  })
})
```

---

## Checklist antes de passar para Green

- [ ] Cada CA do spec tem pelo menos um `it(...)` correspondente
- [ ] Casos de borda do spec têm testes próprios
- [ ] Todos os testes falham ao rodar (`npm test` ou `npx vitest run`)
- [ ] `beforeEach` / `afterEach` garantem isolamento entre testes
- [ ] Mocks são limpos em `afterEach` com `vi.clearAllMocks()` ou equivalente
