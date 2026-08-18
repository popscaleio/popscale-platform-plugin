# Security policy

## Reporting a vulnerability

Use GitHub's private vulnerability reporting for this repository. Do not open a
public issue containing exploit details, credentials, customer information, or
tenant identifiers.

For an active incident involving customer data or production access, contact
Popscale through the established customer support or security channel in your
agreement and revoke the affected MCP connection in Popscale immediately.

## Security boundary

This repository contains no credentials or server implementation. It packages:

- a public, unauthenticated, read-only documentation MCP;
- a separate OAuth-protected, company-scoped product MCP; and
- skills that instruct supported hosts not to cross that boundary.

The product service remains responsible for authorization, scopes, tenant
isolation, confirmation requirements, and audit behavior. A plugin skill is
defense in depth and is never an authorization control.

## Supported versions

Security fixes are applied to the latest published major version. Users should
upgrade the marketplace and reinstall the latest plugin before reporting an
issue that is already fixed there.
