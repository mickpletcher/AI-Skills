# Design

Photo candidates load a file-operation safety reference and include an optional Python standard-library copy helper. Review first, then explicit approval; sources are never deleted. Exclusive destination creation prevents overwrite; preflight and per-file checks reject linked paths and stale plans, reserve names case-insensitively, and verify bytes. Trusted quiescent folders are a precondition, not a claim of hostile concurrency resistance. In-place rename remains unsupported by the helper rather than silently using overwriting filesystem APIs.

Resume candidates separate editorial length estimates from artifact pagination evidence. Actual renderer/output identity, page count, and limitations travel with the report; unsupported render paths remain unverified. Supporting-resource hashes and generated candidates retain migration provenance. No shipped skill is promoted.
