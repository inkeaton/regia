import { ImportError } from './errors'

export interface Token {
  type:  string
  value: string
  line:  number
  col:   number
}

const KEYWORDS = new Set([
  'STORY', 'DEFAULT', 'PRIORITY', 'PHASE', 'AGENT', 'ACTION', 'EVENT',
  'CONDITION', 'DURING', 'ALWAYS', 'WHEN', 'IF', 'AND', 'OR', 'NOT',
  'DO', 'BELIEVE', 'FORGET', 'ENVIRONMENT', 'DIRECTOR', 'MYSELF',
  'PLAYER', 'TIMER', 'TRANSITION', 'TO', 'END',
])

const PUNCT: Record<string, string> = {
  '.': 'PERIOD', ':': 'COLON', ',': 'COMMA', '(': 'LPAREN', ')': 'RPAREN',
}

const ID_START = /[a-zA-Z_]/
const ID_CONT  = /[a-zA-Z0-9_]/
const DIGIT    = /[0-9]/

export function tokenize(source: string): Token[] {
  const tokens: Token[] = []
  let i = 0
  let line = 1
  let col  = 1
  const n = source.length

  const adv = (): string => {
    const c = source[i++]
    if (c === '\n') { line++; col = 1 } else { col++ }
    return c
  }

  while (i < n) {
    const c = source[i]

    // Whitespace
    if (c === ' ' || c === '\t' || c === '\r' || c === '\n') {
      adv()
      continue
    }

    // Comments — doc comment vs plain comment
    if (c === '#') {
      let k = i + 1
      while (k < n && (source[k] === ' ' || source[k] === '\t')) k++
      if (source[k] === '@') {
        const startLine = line, startCol = col
        let lineEnd = i
        while (lineEnd < n && source[lineEnd] !== '\n') lineEnd++
        const text = source.slice(i + 1, lineEnd)
        while (i < lineEnd) adv()
        tokens.push({ type: 'DOC_COMMENT', value: text, line: startLine, col: startCol })
      } else {
        while (i < n && source[i] !== '\n') adv()
      }
      continue
    }

    const startLine = line, startCol = col

    // Identifiers and keywords
    if (ID_START.test(c)) {
      let j = i
      while (j < n && ID_CONT.test(source[j])) j++
      const text = source.slice(i, j)
      while (i < j) adv()
      const type = KEYWORDS.has(text) ? text : 'ID'
      tokens.push({ type, value: text, line: startLine, col: startCol })
      continue
    }

    // Numbers
    if (DIGIT.test(c)) {
      let j = i
      while (j < n && DIGIT.test(source[j])) j++
      const text = source.slice(i, j)
      while (i < j) adv()
      tokens.push({ type: 'NUMBER', value: text, line: startLine, col: startCol })
      continue
    }

    // Punctuation
    if (PUNCT[c]) {
      adv()
      tokens.push({ type: PUNCT[c], value: c, line: startLine, col: startCol })
      continue
    }

    throw new ImportError(`Unexpected character '${c}'`, startLine, startCol)
  }

  tokens.push({ type: 'EOF', value: '', line, col })
  return tokens
}