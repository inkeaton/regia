export class ImportError extends Error {
  line: number
  col:  number

  constructor(message: string, line: number, col: number) {
    super(`Line ${line}, column ${col}: ${message}`)
    this.line = line
    this.col  = col
  }
}