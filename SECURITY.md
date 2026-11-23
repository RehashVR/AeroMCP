# Security Policy

## Responsible Vulnerability Reporting

AeroMCP is an open-source aerospace engineering computation project. If you
discover a security vulnerability, please report it responsibly.

- Do not open a public GitHub issue for security vulnerabilities.
- Contact the project maintainers through the repository's security advisory
  mechanism or by other agreed-upon channels.
- Include a clear description of the vulnerability, steps to reproduce, and
  any suggested remediation.
- Allow reasonable time for the maintainers to investigate and respond before
  public disclosure.

## Prohibited Credentials

To protect the integrity of the project and its users:

- **Do not commit API keys, passwords, access tokens, or personal credentials**
  to the repository under any circumstances.
- The `.gitignore` excludes `.env` files. Use environment variables or local
  configuration files for secrets, and never track them in version control.
- Do not include real authentication credentials in examples, documentation,
  or test files.

## Scope

This security policy covers the AeroMCP Python package and its associated
repository. It does not cover third-party services or AI clients that connect
to AeroMCP through the Model Context Protocol.
