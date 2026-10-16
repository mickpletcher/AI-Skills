# Plan and design

1. Inventory the unchanged Claude tree against existing masters and inspect host assumptions and dependencies.
2. Copy missing workflows with exact, recorded host-neutral substitutions and explicit capability fallbacks. Preserve supporting files byte-for-byte; pin provenance and original documentation.
3. Extend the generator with complete resource bundles and a hash ownership manifest. Preserve resources across Windows/Linux checkouts; retain canonical source companions where instruction filenames differ.
4. Add a separate candidate catalog and regression gates for coverage, source preservation, resource ownership and links.
5. Run local and CI validation; inspect the final diff, confirm AI Scan is disabled, and open a draft PR. Promotion, runtime evaluations, and merge require separate approval.

This is a preservation migration, not a rewrite of domain behavior. Existing foundational masters are retained. Old packages and maintenance documentation remain in the original platform tree; they are not relabeled as candidate distributions.
