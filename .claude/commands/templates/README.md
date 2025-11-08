# Command Templates

This directory contains reusable templates for slash commands to reduce redundancy and maintain consistency.

## Available Templates

### base-command-template.md
Generic template for all slash commands with standard sections:
- Title
- Usage
- What This Does
- Example
- Agent Coordination
- Output

### analysis-command-template.md
Specialized template for code analysis commands (complexity, security, performance, dependencies).

## Usage

When creating new commands, copy the appropriate template and fill in placeholders:
- `{{COMMAND_NAME}}` - Human-readable command name
- `{{COMMAND_SLUG}}` - Slash command name (/command-name)
- `{{DESCRIPTION}}` - Brief description of what the command does
- `{{AGENT}}` - Primary agent responsible
- `{{STEPS}}` - Numbered list of what happens
- `{{OUTPUT}}` - Description of command output

## Benefits

- Consistent structure across all commands
- Reduced duplication
- Easier maintenance
- Faster command creation
