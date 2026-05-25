---
name: project-acme-app
description: What the Acme App is, who uses it, what stage it's in
metadata:
  type: project
---

Acme App is a B2B billing reconciliation tool. Customers are finance teams at SaaS companies with $10M+ ARR.

**Why this matters now:** We're cutting a v2 release in {{YYYY-MM-DD}} that ships invoice-line-level dispute handling. Until that ships, anything touching `invoices.lines[]` is a hot path — treat changes there with extra care.

**How to apply:** When suggesting refactors in the invoices module, confirm with me first. For all other modules, normal autonomy applies.
