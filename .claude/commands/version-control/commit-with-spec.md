# Commit with Spec Reference

Create a git commit that includes a reference to the relevant specification file.

## Usage
/commit-with-spec [spec-id]

## What This Does
1. Locates the specification file by ID (e.g., spec-20251108-auth-flow)
2. Extracts spec metadata (title, objectives, acceptance criteria)
3. Formats a commit message that references the spec
4. Invokes git-workflow-manager to create the commit with proper attribution

## Example
/commit-with-spec spec-20251108-oauth2-implementation

## Agent Coordination
1. **Main LLM**: Locates spec file in specs/active/ or specs/completed/
2. **Main LLM**: Extracts spec_id and relevant metadata
3. **git-workflow-manager**: Creates commit with format:

```
feat: Implement OAuth2 authentication endpoints

- Add authorization code flow implementation
- Configure JWT token generation
- Set up refresh token rotation

Spec: spec-20251108-oauth2-implementation
Acceptance Criteria: AC-1, AC-2, AC-3 satisfied

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Output
- Git commit created with spec reference in commit body
- Commit hash returned
- Changes staged automatically if not already staged

## See Also
For related commands, see [Git Commands](../shared/related-git-commands.md)
