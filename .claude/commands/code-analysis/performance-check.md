# Performance Check

Analyze code for performance bottlenecks and optimization opportunities.

## Usage
/performance-check [path] [--profile] [--focus api|database|rendering]

## What This Does
1. Identifies performance bottlenecks in code
2. Analyzes algorithmic complexity (Big O)
3. Detects inefficient database queries (N+1 problems)
4. Flags unnecessary re-renders (React/Vue)
5. Identifies memory leaks and resource issues
6. Suggests performance optimizations

## Example
/performance-check src/api --focus database

## Agent Coordination
1. **Main LLM**: Static code analysis for performance patterns
   - Algorithm complexity analysis
   - Resource usage patterns
   - Inefficient loops and operations
2. **backend-architect** (for API/database focus):
   - Database query optimization
   - API endpoint performance
   - Caching opportunities
3. **frontend-developer** (for rendering focus):
   - React/Vue render optimization
   - Bundle size analysis
   - Lazy loading opportunities

## Output
Performance Analysis Report:
```markdown
## Performance Check Report

### Overview
- Files analyzed: 18
- Bottlenecks found: 4 critical, 7 high, 15 medium
- Estimated performance gain: 60% reduction in response time
- Critical path issues: 3

### Critical Bottlenecks

1. **N+1 Query Problem** - src/api/users.ts:67
   - Severity: CRITICAL
   - Current: 1 + 500 queries for user list endpoint
   - Impact: 2000ms response time at 500 users
   - Optimization: Use JOIN or eager loading
   - Expected gain: 2000ms → 50ms (40x faster)
   ```typescript
   // Current (BAD)
   const users = await User.find();
   for (const user of users) {
     user.posts = await Post.find({ userId: user.id });
   }

   // Optimized (GOOD)
   const users = await User.find().populate('posts');
   ```

2. **Inefficient Algorithm** - src/utils/search.ts:34
   - Severity: CRITICAL
   - Current: O(n²) nested loops for search
   - Impact: 5000ms for 1000 items
   - Optimization: Use Map/Set for O(n) complexity
   - Expected gain: 5000ms → 100ms (50x faster)

3. **Synchronous File Operations** - src/workers/export.ts:45
   - Severity: CRITICAL
   - Current: Blocking file writes in request handler
   - Impact: Request queue buildup, 503 errors
   - Optimization: Use async file operations or queue
   - Expected gain: Eliminate blocking, prevent timeouts

### High Priority Issues

4. **Missing Database Indexes** - users table
   - Queries: SELECT WHERE email, SELECT WHERE created_at
   - Impact: Full table scans on 50K+ rows
   - Optimization: Add indexes on email, created_at
   - Expected gain: 800ms → 5ms per query

5. **Unnecessary Re-renders** - src/components/UserList.tsx
   - Impact: 500 components re-render on single state change
   - Optimization: React.memo, useMemo, useCallback
   - Expected gain: 300ms → 20ms render time

6. **Large Bundle Size** - frontend app
   - Current: 2.5MB JavaScript bundle
   - Impact: 8s load time on 3G
   - Optimization: Code splitting, tree shaking, lazy loading
   - Expected gain: 2.5MB → 800KB (60% reduction)

### Medium Priority Opportunities

7. **Cache Miss Rate High** - API endpoints (85% miss rate)
8. **Inefficient JSON Serialization** - Large object responses
9. **Memory Leak** - Event listeners not cleaned up
10. **Unoptimized Images** - Serving full-size assets

### Recommendations by Priority

**Immediate (Critical Path)**:
1. Fix N+1 queries in user endpoints
2. Optimize search algorithm complexity
3. Make file operations async

**Short-term (High Impact)**:
4. Add database indexes
5. Implement React.memo for large lists
6. Enable code splitting

**Long-term (Incremental Gains)**:
7. Implement better caching strategy
8. Optimize JSON serialization
9. Add monitoring for memory leaks
10. Set up image optimization pipeline

### Performance Budget
- API Response Time: Target <200ms (currently 2000ms) ❌
- Bundle Size: Target <1MB (currently 2.5MB) ❌
- Time to Interactive: Target <3s (currently 8s) ❌
- Database Query Time: Target <50ms (currently 800ms) ❌

### Estimated ROI
- Development time: 16 hours
- Performance improvement: 60% faster
- User experience impact: HIGH
- Cost savings: Reduced server load by 40%
```

Returns: Actionable performance optimization roadmap
