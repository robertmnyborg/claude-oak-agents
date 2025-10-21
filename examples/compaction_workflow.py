#!/usr/bin/env python3
"""
Example: Context Compression in Multi-Agent Workflow

Demonstrates how compaction reduces context size in agent handoffs.
"""

import sys
sys.path.insert(0, '/Users/robertnyborg/Projects/claude-oak-agents/core')

from compaction import compact_output


def simulate_multi_agent_workflow():
    """
    Simulate a 3-agent workflow with context compression.
    
    Workflow: Research Agent → Planning Agent → Implementation Agent
    """
    
    # AGENT 1: Research Agent (produces verbose output)
    research_output = """
# Authentication System Research

## Current State Analysis
The existing authentication system was implemented 3 years ago using basic JWT tokens.
Security best practices have evolved significantly since then.

## Security Vulnerabilities
- JWT tokens lack refresh mechanism
- bcrypt rounds=10 (should be 12-14)
- No rate limiting on login endpoints
- Tokens stored in localStorage (XSS vulnerable)
- No account lockout after failed attempts

## Performance Bottlenecks  
- Auth middleware runs on every request
- No caching of token validation
- Database queries for user lookup not indexed
- Average auth latency: 45ms (target: <10ms)

## Architecture Issues
- Monolithic auth service
- No separation of authentication vs authorization
- Hard dependency on single database
- No horizontal scaling capability

## Files Analyzed
- `src/auth/jwt-handler.ts` - Token generation
- `src/auth/password-hasher.ts` - Password utilities
- `src/middleware/auth-middleware.ts` - Request auth
- `src/models/user.model.ts` - User model

## Recommendations
### Immediate (Week 1-2)
- Implement refresh token rotation
- Increase bcrypt rounds to 12
- Add rate limiting (100 req/15min)
- Move tokens to httpOnly cookies
- Add database indexes

### Medium-term (Month 1-2)
- Separate auth service
- Implement Redis caching
- Add OAuth2/OIDC support
- Create authorization service

### Long-term (Quarter 1-2)
- Migrate to Auth0/Cognito
- Zero-trust architecture
- Biometric support

## Next Steps
- Security audit by external team
- Performance benchmarking
- Migration planning
- Stakeholder approval
"""

    print("="*80)
    print("AGENT 1: RESEARCH")
    print("="*80)
    print(f"Full output: {len(research_output.split(chr(10)))} lines")
    
    # Compress for next agent
    research_summary = compact_output(research_output, "research")
    print(f"Compressed: {len(research_summary.split(chr(10)))} lines")
    print(f"Compression ratio: {len(research_output) / len(research_summary):.1f}x")
    print("\nCOMPRESSED SUMMARY:")
    print("-"*80)
    print(research_summary)
    
    
    # AGENT 2: Planning Agent (receives summary, produces plan)
    # In real workflow: planning_agent.execute(context=research_summary)
    planning_output = """
# Authentication System Modernization Plan

## Executive Summary
Based on research findings, we will modernize the auth system in 3 phases over 6 weeks.
Phase 1 addresses critical security issues. Phase 2 improves performance. Phase 3 adds scalability.

## Phase 1: Security Hardening (Week 1-2)
### Tasks
- Task 1.1: Implement refresh token rotation
  - Estimate: 3 days
  - Owner: Backend team
  - Files: `src/auth/jwt-handler.ts`, `src/auth/refresh-handler.ts`
  
- Task 1.2: Increase bcrypt rounds
  - Estimate: 1 day
  - Owner: Backend team
  - Files: `src/auth/password-hasher.ts`
  
- Task 1.3: Add rate limiting
  - Estimate: 2 days
  - Owner: Backend team
  - Files: `src/middleware/rate-limiter.ts`

## Phase 2: Performance Optimization (Week 3-4)
### Tasks
- Task 2.1: Implement Redis caching
  - Estimate: 5 days
  - Owner: Infrastructure team
  - Files: `src/cache/redis-client.ts`, `src/auth/cached-validator.ts`
  
- Task 2.2: Add database indexes
  - Estimate: 2 days
  - Owner: Database team
  - Files: `migrations/add-auth-indexes.sql`

## Phase 3: Architecture Updates (Week 5-6)
### Tasks
- Task 3.1: Separate auth service
  - Estimate: 7 days
  - Owner: Backend + Infrastructure
  - Files: `services/auth-service/`, `configs/auth-service.yaml`

## Files to Create
- `src/auth/refresh-handler.ts`
- `src/middleware/rate-limiter.ts`
- `src/cache/redis-client.ts`
- `src/auth/cached-validator.ts`
- `migrations/add-auth-indexes.sql`
- `services/auth-service/`

## Dependencies
- Redis server setup (Infrastructure)
- Database migration approval (DBA)
- Security audit (External team)

## Success Metrics
- Auth latency < 10ms (currently 45ms)
- Zero security vulnerabilities
- Support 10,000 concurrent users

## Next Steps
- Get stakeholder approval
- Assign task owners
- Begin Phase 1 implementation
"""

    print("\n\n" + "="*80)
    print("AGENT 2: PLANNING")
    print("="*80)
    print(f"Full output: {len(planning_output.split(chr(10)))} lines")
    
    planning_summary = compact_output(planning_output, "plan")
    print(f"Compressed: {len(planning_summary.split(chr(10)))} lines")
    print(f"Compression ratio: {len(planning_output) / len(planning_summary):.1f}x")
    print("\nCOMPRESSED SUMMARY:")
    print("-"*80)
    print(planning_summary)
    
    
    # AGENT 3: Implementation Agent (receives summary)
    # In real workflow: implementation_agent.execute(context=planning_summary)
    print("\n\n" + "="*80)
    print("AGENT 3: IMPLEMENTATION (receives compressed plan)")
    print("="*80)
    print("Implementation agent receives only the planning summary:")
    print(f"Context size: {len(planning_summary.split(chr(10)))} lines instead of {len(planning_output.split(chr(10)))} lines")
    print("\nContext savings in multi-agent workflow:")
    
    total_original = len(research_output) + len(planning_output)
    total_compressed = len(research_summary) + len(planning_summary)
    
    print(f"- Without compression: {total_original:,} characters")
    print(f"- With compression: {total_compressed:,} characters")
    print(f"- Savings: {total_original - total_compressed:,} characters ({100 * (1 - total_compressed/total_original):.1f}% reduction)")
    print(f"- Token savings estimate: ~{(total_original - total_compressed) // 4:,} tokens")


if __name__ == "__main__":
    simulate_multi_agent_workflow()
