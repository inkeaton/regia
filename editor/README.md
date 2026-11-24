# Regia Visual Editor

A browser-based visual editor for the Regia language. It combines a Monaco code editor with a ReactFlow graph view to let designers write Regia source code and immediately see the resulting AST as an interactive, auto-laid-out node graph.

## Prerequisites

- **Node.js 24** (with npm), pinned in `.nvmrc`
- **Python backend** – the editor calls the transpiler through a FastAPI server, started with `regia serve` (the `regia` package with its `server` extra; see [`language/README.md`](../language/README.md)).

## Installation

```bash
cd editor
npm ci
```

## Running

The editor requires two processes running simultaneously:

### 1. Start the API Server

From the repository root:

```bash
make serve
```

The server starts at `http://127.0.0.1:8000` and exposes a `/parse` endpoint that compiles Regia source code and returns the AST as JSON.

### 2. Start the Frontend

```bash
cd editor
npm run dev
```

Open http://localhost:5173 in your browser.

## Usage

1. Write or paste Regia code in the left-hand Monaco editor panel.
2. The code is sent to the Python backend, which parses it and returns the AST.
3. The right-hand panel renders the AST as a node graph, with automatic layout provided by [dagre](https://github.com/dagrejs/dagre).
4. Compilation errors are displayed inline in the editor.

## Build for Production

From the repository root:

```bash
make editor
```

This installs the locked dependencies and builds. The output is placed in `dist/` and can be served by any static file server.

## Changing Ports

The editor and its API server communicate over HTTP. If you need to change the default ports:

| What | Default | Where to change |
|---|---|---|
| API server | `127.0.0.1:8000` | `regia serve --host <host> --port <number>` |
| Frontend → API URL | `http://127.0.0.1:8000` | `src/services/transport.ts` — update the `HTTP_API_BASE_URL` constant |
| Vite dev server | `localhost:5173` | `vite.config.ts` — add a `server: { port: <number> }` block |

> **Note:** If you change the API server port, you **must** also update `HTTP_API_BASE_URL` in the frontend so the editor can reach the server.

## Tech Stack

| Concern | Library |
|---|---|
| UI Framework | React 19 |
| Build Tool | Vite |
| Code Editor | Monaco Editor (`@monaco-editor/react`) |
| Graph View | ReactFlow + dagre (auto-layout) |
| State Management | Zustand |
| Export | html-to-image |
| Linting | Oxlint |

## Project Structure

```text
editor/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── src/
    ├── main.tsx              App entry point
    ├── App.tsx               Root component
    ├── index.css             Global styles
    ├── api/                  Backend API client
    ├── components/           React components (editor, graph nodes)
    ├── hooks/                Custom React hooks
    ├── layout/               Layout components
    ├── services/             Graph layout and transform services
    ├── store/                Zustand state stores
    ├── types/                TypeScript type definitions
    └── export/               Image export utilities
```
