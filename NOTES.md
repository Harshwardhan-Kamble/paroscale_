# Project Notes

## What this project is about

This project is a solution to the Niova Systems package indexing challenge.

The goal is to build a TCP server that maintains an in-memory package index while tracking dependencies between packages.

Clients connect to the server on port 8080 and send commands to:

* Index a package
* Remove a package
* Query whether a package is indexed

The server must ensure that:

* A package cannot be indexed until all of its dependencies are already indexed.
* A package cannot be removed if another indexed package depends on it.
* Multiple clients can interact with the server concurrently.
* Invalid messages are handled gracefully.

---

## Commands Supported

### INDEX

Format:

```text
INDEX|package|dep1,dep2
```

Example:

```text
INDEX|nginx|openssl,pcre
```

Returns:

* OK if all dependencies are already indexed
* FAIL if any dependency is missing

### QUERY

Format:

```text
QUERY|package|
```

Returns:

* OK if the package exists
* FAIL otherwise

### REMOVE

Format:

```text
REMOVE|package|
```

Returns:

* OK if the package can be removed
* FAIL if another indexed package depends on it

---

## Implementation

The server is implemented in Python using only the standard library.

Main components:

* socket module for TCP networking
* threading module for concurrent clients
* global lock for thread-safe access to shared state

Data structures used:

### indexed_packages

Stores all currently indexed packages.

### dependencies

Dictionary mapping:

```python
package -> set(dependencies)
```

Example:

```python
{
    "nginx": {"openssl", "pcre"},
    "postgresql": {"openssl"}
}
```

---

## Concurrency

Each incoming client connection is handled in a separate thread.

A global lock protects shared package data to ensure correctness when multiple clients issue commands simultaneously.

---

## Error Handling

The server returns:

```text
ERROR
```

for:

* malformed messages
* invalid commands
* missing package names

---

## How to Run

From the repository root:

```bash
make run
```

or directly:

```bash
python3 solution/server.py
```

The server listens on:

```text
localhost:8080
```

---

## Testing

Run the supplied test harness:

```bash
./test-driver-bin/niova-candidate-test-driver_linux
```

Additional stress testing:

```bash
./test-driver-bin/niova-candidate-test-driver_linux -concurrency 100
```

---

## What was implemented

Completed features:

* TCP server on port 8080
* INDEX command
* QUERY command
* REMOVE command
* Dependency validation
* Dependency-aware package removal
* Concurrent client handling
* Thread-safe shared state
* Invalid message handling
* Makefile support
* LLM usage disclosure

---

## Known Limitations

* Package data is stored only in memory.
* State is lost when the server exits.
* No persistence layer is implemented since it was not required for the challenge.
