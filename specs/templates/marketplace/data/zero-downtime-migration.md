---
template_id: zero-downtime-migration
template_name: Zero-Downtime Database Migration
category: data
difficulty: expert
estimated_time: 12-16 hours
tags: [database, migration, postgresql, mongodb, schema, blue-green]
author: claude-oak-agents
version: 1.0.0
last_updated: 2025-11-08
popularity: 88
dependencies: [database-client, migration-tool]
related_templates: [rest-crud-api, cdk-serverless-api]
---

# Zero-Downtime Database Migration

Execute complex database schema changes without downtime using expand-contract pattern and dual-write strategy.

## Overview

This template provides a systematic approach to database migrations that require zero downtime, including:
- Column additions, renames, and deletions
- Table splits and merges
- Data type changes
- Index modifications
- Cross-database migrations (PostgreSQL ↔ MongoDB)

**Key Principle**: Expand-Contract pattern - expand schema to support both old and new, transition gradually, then contract by removing old schema.

## Use Cases

- **Production Schema Changes**: Modify critical database schema without service interruption
- **Database Technology Migration**: Move from one database to another (e.g., MongoDB → PostgreSQL)
- **Data Model Refactoring**: Restructure data models while maintaining service availability
- **Multi-Region Data Sync**: Gradual migration from single-region to multi-region database

## Requirements

### Technical Prerequisites
- Database with transaction support (PostgreSQL, MySQL) or atomic operations (MongoDB)
- Migration tool (Flyway, Liquibase, or custom)
- Monitoring and observability (track migration progress)
- Rollback capability (data backups, migration reversibility)

### Operational Prerequisites
- Read/write traffic monitoring
- Feature flags for gradual rollout
- Ability to deploy application code independently
- Database connection pooling and retry logic

## Implementation Plan

### Phase 1: Analysis and Planning (2 hours)

**1.1 Current State Assessment**
- Document current schema
- Identify all code paths reading/writing affected data
- Estimate data volume and growth rate
- Measure baseline query performance

**1.2 Migration Strategy Selection**

**Expand-Contract Pattern** (column rename example):
1. Expand: Add new column, dual-write to both old and new
2. Backfill: Copy data from old to new column
3. Transition: Switch reads from old to new column
4. Contract: Remove old column

**Dual-Write Strategy** (cross-database migration):
1. Setup: Deploy new database, configure dual-write
2. Backfill: Bulk copy existing data to new database
3. Validation: Verify data consistency
4. Cutover: Switch reads to new database
5. Cleanup: Remove old database

### Phase 2: Schema Changes (4 hours)

**2.1 Column Addition (Expand Phase)**
```sql
-- Migration 001: Add new column (nullable initially)
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Create index in background (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_full_name ON users(full_name);
```

**2.2 Dual-Write Implementation**
```typescript
// Application code: Write to both old and new columns
async function updateUser(userId: string, firstName: string, lastName: string) {
  await db.query(`
    UPDATE users
    SET first_name = $1,
        last_name = $2,
        full_name = $3  -- New column
    WHERE id = $4
  `, [firstName, lastName, `${firstName} ${lastName}`, userId]);
}
```

**2.3 Data Backfill**
```sql
-- Migration 002: Backfill data in batches to avoid locks
DO $$
DECLARE
  batch_size INTEGER := 10000;
  affected_rows INTEGER;
BEGIN
  LOOP
    UPDATE users
    SET full_name = CONCAT(first_name, ' ', last_name)
    WHERE full_name IS NULL
    LIMIT batch_size;

    GET DIAGNOSTICS affected_rows = ROW_COUNT;
    EXIT WHEN affected_rows = 0;

    -- Pause between batches to avoid overwhelming database
    PERFORM pg_sleep(0.5);
  END LOOP;
END $$;
```

**2.4 NOT NULL Constraint (After Backfill)**
```sql
-- Migration 003: Make column NOT NULL after backfill complete
ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;
```

### Phase 3: Application Code Transition (3 hours)

**3.1 Feature Flag for Read Transition**
```typescript
// Phase 1: Dual-write, read from old column
if (featureFlags.readFullNameFromNewColumn) {
  return user.full_name;  // New column
} else {
  return `${user.first_name} ${user.last_name}`;  // Old columns
}
```

**3.2 Gradual Rollout**
- Enable feature flag for 1% of traffic
- Monitor error rates and query performance
- Gradually increase to 10%, 50%, 100%
- Rollback capability at each step

**3.3 Remove Dual-Write (Contract Phase)**
```typescript
// Phase 2: Remove dual-write after all reads switched
async function updateUser(userId: string, fullName: string) {
  await db.query(`
    UPDATE users
    SET full_name = $1
    WHERE id = $2
  `, [fullName, userId]);
}
```

### Phase 4: Schema Cleanup (1 hour)

**4.1 Drop Old Columns**
```sql
-- Migration 004: Remove old columns after transition complete
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```

### Phase 5: Cross-Database Migration (8 hours)

**5.1 Setup New Database**
- Deploy new database (e.g., PostgreSQL)
- Create schema matching old database structure
- Configure connection pools

**5.2 Dual-Write Implementation**
```typescript
async function createUser(userData: UserData) {
  // Write to both databases
  const mongoUser = await mongoClient.users.insertOne(userData);
  const pgUser = await pgClient.query(
    'INSERT INTO users (id, email, name) VALUES ($1, $2, $3)',
    [userData.id, userData.email, userData.name]
  );

  // Use feature flag to determine which result to return
  return featureFlags.readFromPostgres ? pgUser : mongoUser;
}
```

**5.3 Data Backfill**
```typescript
// Bulk copy data in batches
async function backfillUsers() {
  const batchSize = 10000;
  let offset = 0;

  while (true) {
    const users = await mongoClient.users.find()
      .skip(offset)
      .limit(batchSize)
      .toArray();

    if (users.length === 0) break;

    // Bulk insert to PostgreSQL
    await pgClient.query(
      'INSERT INTO users (id, email, name) VALUES ' +
      users.map((u, i) => `($${i*3+1}, $${i*3+2}, $${i*3+3})`).join(','),
      users.flatMap(u => [u.id, u.email, u.name])
    );

    offset += batchSize;
    console.log(`Backfilled ${offset} users`);

    // Pause between batches
    await sleep(1000);
  }
}
```

**5.4 Data Validation**
```typescript
// Compare data between databases
async function validateMigration() {
  const mongoCount = await mongoClient.users.countDocuments();
  const pgCount = await pgClient.query('SELECT COUNT(*) FROM users');

  console.log(`MongoDB: ${mongoCount}, PostgreSQL: ${pgCount.rows[0].count}`);

  // Sample validation
  const sampleSize = 1000;
  const mongoUsers = await mongoClient.users.aggregate([
    { $sample: { size: sampleSize } }
  ]).toArray();

  for (const mongoUser of mongoUsers) {
    const pgUser = await pgClient.query(
      'SELECT * FROM users WHERE id = $1',
      [mongoUser.id]
    );

    if (!deepEqual(mongoUser, pgUser.rows[0])) {
      console.error(`Mismatch for user ${mongoUser.id}`);
    }
  }
}
```

**5.5 Cutover**
- Enable feature flag to read from PostgreSQL (1% traffic)
- Monitor query performance and error rates
- Gradually increase to 100%
- Keep dual-write for safety window (7 days)

**5.6 Cleanup**
- Remove MongoDB dual-write after safety window
- Archive MongoDB data
- Decommission MongoDB cluster

## Agent Workflow

```yaml
agent_sequence:
  phase_1_planning:
    - agent: design-simplicity-advisor
      task: "Evaluate migration complexity and recommend simplest approach"
      output: "Strategy recommendation: expand-contract vs dual-write"

    - agent: backend-architect
      task: "Design migration phases with rollback points"
      output: "Migration plan with 5 phases, each reversible"

  phase_2_implementation:
    - agent: backend-architect
      task: "Implement schema changes (expand phase)"
      duration: "2 hours"

    - agent: backend-architect
      task: "Implement dual-write in application code"
      duration: "2 hours"

    - agent: backend-architect
      task: "Create data backfill scripts with batching"
      duration: "2 hours"

  phase_3_validation:
    - agent: qa-specialist
      task: "Create validation scripts and monitoring"
      output: "Data consistency checks, performance baselines"

    - agent: unit-test-expert
      task: "Tests for dual-write correctness"
      coverage: ">90%"

  phase_4_execution:
    - agent: backend-architect
      task: "Execute migration phases with gradual rollout"
      duration: "4 hours"

    - agent: infrastructure-specialist
      task: "Monitor database performance and rollback if needed"

  phase_5_cleanup:
    - agent: backend-architect
      task: "Remove old schema and code paths (contract phase)"
      duration: "1 hour"

    - agent: git-workflow-manager
      task: "Create PR with migration implementation"
```

## Testing Strategy

### Pre-Migration Tests
- Backup verification (restore test)
- Rollback script validation
- Performance baseline (query latency, throughput)

### During Migration Tests
- Dual-write correctness (data written to both locations)
- Data consistency checks (old vs new)
- Query performance (no regression)
- Error rate monitoring (no increase)

### Post-Migration Tests
- Data integrity validation (full scan)
- Query correctness (results match old schema)
- Performance regression tests
- Rollback test (verify migration is reversible)

## Rollback Strategy

### Rollback Triggers
- Data inconsistency detected (>1% mismatch)
- Query performance degradation (>50% latency increase)
- Error rate spike (>5% increase)
- Critical bug discovered

### Rollback Procedure

**Phase 1-2 (Expand, Dual-Write)**: Simple rollback
- Disable feature flag (revert reads to old column)
- Remove new column (if no data written)

**Phase 3 (Backfill)**: Partial rollback
- Stop backfill process
- Verify data written so far
- Decision: continue or revert

**Phase 4 (Transition)**: Gradual rollback
- Reduce feature flag percentage
- Monitor for stability
- Full revert if issues persist

**Phase 5 (Contract)**: Point of no return
- Old columns deleted - cannot rollback
- Must fix forward (migration to correct new schema)

## Monitoring and Observability

### Key Metrics
- Migration progress (% of data backfilled)
- Dual-write lag (time between old and new write)
- Data consistency (% match between old and new)
- Query latency (p50, p99 before and after)
- Error rates (database errors, application errors)

### Dashboards
- Migration progress over time
- Query performance comparison (old vs new)
- Data volume trends
- Error rate trends

### Alerts
- Data inconsistency threshold (>100 mismatches)
- Performance degradation (p99 latency >2x baseline)
- Error rate spike (>5% increase)
- Migration stalled (no progress for 1 hour)

## Common Pitfalls

### 1. Locking During Schema Changes
**Problem**: ALTER TABLE locks table, blocking reads/writes
**Solution**: Use non-blocking operations (PostgreSQL: CREATE INDEX CONCURRENTLY, ADD COLUMN with default)

### 2. Backfill Performance Impact
**Problem**: Large batch updates cause replication lag
**Solution**: Small batches (10k rows), pauses between batches, monitor replication lag

### 3. Insufficient Testing
**Problem**: Rollback script untested until needed
**Solution**: Test rollback in staging before production, include rollback in migration plan

### 4. Data Type Mismatches
**Problem**: Cross-database migration loses precision (MongoDB Number → PostgreSQL INTEGER)
**Solution**: Validate data types, use appropriate PostgreSQL types (BIGINT, NUMERIC)

### 5. Missing Indexes
**Problem**: New column performs poorly without index
**Solution**: Create indexes concurrently before cutover, monitor query plans

### 6. Race Conditions
**Problem**: Dual-write can have inconsistent order
**Solution**: Use timestamps or version numbers, implement conflict resolution

## Success Criteria

- [ ] Zero service downtime during migration
- [ ] 100% data consistency validated
- [ ] No query performance regression (p99 latency within 10% of baseline)
- [ ] Error rate unchanged (<1% difference)
- [ ] Rollback tested and verified
- [ ] All code paths updated (no references to old schema)
- [ ] Monitoring dashboards show green status
- [ ] Documentation updated with new schema

## Timeline Example (Column Rename)

**Week 1**: Planning and dual-write implementation
- Day 1-2: Analysis and strategy
- Day 3-5: Implement dual-write and deploy

**Week 2**: Backfill and validation
- Day 1-3: Run backfill scripts
- Day 4-5: Validate data consistency

**Week 3**: Transition reads
- Day 1: Enable feature flag for 1% traffic
- Day 2-3: Gradually increase to 50%
- Day 4-5: Increase to 100%

**Week 4**: Cleanup
- Day 1-3: Monitor for issues
- Day 4: Remove dual-write code
- Day 5: Drop old columns

**Safety Window**: 1 week between each phase for monitoring
