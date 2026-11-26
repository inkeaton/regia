# Print a file

Type: implementation
Status: open
Assignee:
Blocked by: 09

## Goal

`regia <path>` prints the file unchanged.

## Spec

Chapter 23: the CLI gathers files, the core does no I/O. The bare `regia <path>` is scaffolding until the commands of M8.

## Rust

Book ch 12.1–12.2, ahead of its place: arguments and `fs::read_to_string`. New concept: calling the standard library; `Result` is met only as `expect`, and is covered in ch 9.

## Test first

An integration test runs the binary on `docs/showcase/playbooks/courtesy.regia` and compares the output with the file, byte for byte.

## Done when

The test passes, and running it on a showcase file shows the file.

## Not here

Any error handling.
