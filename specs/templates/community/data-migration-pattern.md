# Pattern: Zero-Downtime Database Migrations

```yaml
pattern_metadata:
  name: "zero-downtime-database-migration"
  category: "data"
  difficulty: "advanced"
  tech_stack: ["PostgreSQL", "MySQL", "MongoDB", "Node.js", "TypeScript"]
  tags: ["database", "migration", "zero-downtime", "production", "deployment"]
  version: "1.0.0"
  status: "stable"
  author: "claude-oak-agents"
  last_updated: "2025-11-08"
```

## Problem Statement

### What Challenge Does This Solve?

Production database migrations require schema changes without service interruption:
- Add/remove columns without downtime
- Change data types safely
- Migrate data between tables
- Handle rollback scenarios
- Maintain referential integrity
- Support concurrent deployments

### When Should You Use This Pattern?

Use this pattern when:
- ✅ Production database with high availability requirements
- ✅ Schema changes needed without downtime
- ✅ Data migration between existing tables/columns
- ✅ Need rollback capability for safety
- ✅ Blue-green or rolling deployments

Don't use this pattern when:
- ❌ Development/staging environment (can afford downtime)
- ❌ Database is empty or very small
- ❌ Can schedule maintenance windows

### Prerequisites

- Database supports transactional DDL (PostgreSQL, MySQL 8+)
- Migration tool (Knex, TypeORM, Flyway, Liquibase)
- Database backup and restore procedures
- Rollback plan and testing

## Solution Overview

### High-Level Approach

```
Phase 1: Expand Schema (Backward Compatible)
┌──────────────────────────────────────┐
│  Old Code       →     Database        │
│  (still works)        + New Column    │
│                       (nullable)      │
└──────────────────────────────────────┘

Phase 2: Dual-Write (Transition)
┌──────────────────────────────────────┐
│  New Code       →     Database        │
│  (writes both)        + New Column    │
│                       + Old Column    │
└──────────────────────────────────────┘

Phase 3: Migrate Data (Background)
┌──────────────────────────────────────┐
│  Background Job   →   Copy Data       │
│  (batched)            Old → New       │
└──────────────────────────────────────┘

Phase 4: Switch Reads (Code Deployment)
┌──────────────────────────────────────┐
│  New Code       →     Database        │
│  (reads new)          + New Column    │
└──────────────────────────────────────┘

Phase 5: Contract Schema (Cleanup)
┌──────────────────────────────────────┐
│  New Code       →     Database        │
│  (new only)           - Old Column    │
└──────────────────────────────────────┘
```

### Key Design Decisions

**1. Expand-Contract Pattern**
- Expand: Add new schema elements (backward compatible)
- Transition: Dual-write to old and new structures
- Contract: Remove old schema elements after migration

**2. Batched Data Migration**
- Process data in small batches (1000-10000 rows)
- Pause between batches to avoid lock contention
- Track migration progress for resumability

**3. Feature Flags for Rollback**
- Toggle between old and new code paths
- Instant rollback without database changes
- Gradual rollout to production instances

**4. Immutable Migrations**
- Never modify existing migrations
- Always create new migration for changes
- Maintain migration history for audit trail

## Technical Design

### 5-Phase Migration Strategy

#### Phase 1: Expand (Add New Column)

**Migration 001**:
```sql
-- Add new column as nullable (backward compatible)
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT NULL;

-- Add index for performance (CONCURRENT to avoid locks)
CREATE INDEX CONCURRENTLY idx_users_email_verified 
ON users(email_verified);
```

**Code**: No changes (old code continues working)

**Rollback**: Drop column and index

#### Phase 2: Dual-Write (Write to Both Old and New)

**Migration 002**: None (code-only change)

**Code**:
```typescript
// Update user model to write to both columns
async function updateUser(userId: string, data: any) {
  // Write to new column
  data.email_verified = data.is_verified;
  
  // Still write to old column (dual-write)
  data.is_verified = data.is_verified;
  
  await db.query(
    'UPDATE users SET email_verified = $1, is_verified = $2 WHERE id = $3',
    [data.email_verified, data.is_verified, userId]
  );
}
```

**Rollback**: Revert code deployment (database unchanged)

#### Phase 3: Backfill Data (Background Job)

**Migration 003**: Create migration tracking table

```sql
CREATE TABLE migration_progress (
  id SERIAL PRIMARY KEY,
  migration_name VARCHAR(255) UNIQUE NOT NULL,
  last_processed_id BIGINT,
  completed BOOLEAN DEFAULT FALSE,
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);
```

**Code**: Run background job to migrate existing data

```typescript
async function backfillEmailVerified() {
  const BATCH_SIZE = 5000;
  const PAUSE_MS = 1000; // 1 second between batches
  
  while (true) {
    // Get last processed ID
    const progress = await db.query(
      'SELECT last_processed_id FROM migration_progress WHERE migration_name = $1',
      ['backfill_email_verified']
    );
    
    const lastId = progress.rows[0]?.last_processed_id || 0;
    
    // Process next batch
    const result = await db.query(`
      UPDATE users
      SET email_verified = is_verified
      WHERE id > $1 
        AND email_verified IS NULL
        AND id IN (
          SELECT id FROM users 
          WHERE id > $1 AND email_verified IS NULL
          ORDER BY id
          LIMIT $2
        )
      RETURNING id
    `, [lastId, BATCH_SIZE]);
    
    if (result.rows.length === 0) {
      // Migration complete
      await db.query(
        'UPDATE migration_progress SET completed = TRUE, completed_at = NOW() WHERE migration_name = $1',
        ['backfill_email_verified']
      );
      break;
    }
    
    // Update progress
    const maxId = Math.max(...result.rows.map(r => r.id));
    await db.query(
      'UPDATE migration_progress SET last_processed_id = $1 WHERE migration_name = $2',
      [maxId, 'backfill_email_verified']
    );
    
    console.log(`Migrated batch: ${result.rows.length} rows, last ID: ${maxId}`);
    
    // Pause to avoid overwhelming database
    await new Promise(resolve => setTimeout(resolve, PAUSE_MS));
  }
}
```

**Rollback**: Stop background job (database has both old and new values)

#### Phase 4: Switch Reads (Read from New Column)

**Migration 004**: None (code-only change)

**Code**:
```typescript
// Feature flag for gradual rollout
const USE_NEW_EMAIL_VERIFIED = process.env.FEATURE_NEW_EMAIL_VERIFIED === 'true';

async function getUser(userId: string) {
  const result = await db.query(
    'SELECT *, email_verified, is_verified FROM users WHERE id = $1',
    [userId]
  );
  
  const user = result.rows[0];
  
  // Read from new column if feature enabled
  user.isVerified = USE_NEW_EMAIL_VERIFIED 
    ? user.email_verified 
    : user.is_verified;
  
  return user;
}
```

**Rollback**: Set feature flag to false (instant rollback)

#### Phase 5: Contract (Remove Old Column)

**Migration 005**: Drop old column (AFTER verifying migration success)

```sql
-- Wait 1-2 weeks in production before this step

-- Drop old column
ALTER TABLE users DROP COLUMN is_verified;
```

**Code**: Remove old column references

```typescript
// Clean up: Remove dual-write and feature flag
async function getUser(userId: string) {
  const result = await db.query(
    'SELECT *, email_verified FROM users WHERE id = $1',
    [userId]
  );
  return result.rows[0];
}
```

**Rollback**: Cannot rollback this phase (wait 1-2 weeks before executing)

### Security Considerations

**Migration Safety**:
- Test migrations on production-like data volume
- Run in transaction where possible
- Use `CONCURRENT` for index creation (PostgreSQL)
- Monitor database locks and performance

**Data Integrity**:
- Verify data consistency after backfill
- Use constraints to prevent invalid states
- Run checksums to validate migration

**Access Control**:
- Migration scripts require elevated database privileges
- Audit all migration executions
- Restrict who can run migrations

## Agent Workflow

### Agents Involved

1. **design-simplicity-advisor** - Migration complexity analysis
2. **backend-architect** - Migration strategy and DDL generation
3. **qa-specialist** - Migration testing and validation
4. **infrastructure-specialist** - Deployment coordination
5. **quality-gate** - Unified validation
6. **git-workflow-manager** - Commit and PR

### Execution Sequence

```
design-simplicity-advisor (analyze migration approach)
  ↓
backend-architect (generate 5-phase migration plan)
  ↓
qa-specialist (create migration tests)
  ↓
infrastructure-specialist (deployment runbook)
  ↓
quality-gate (unified validation)
  ↓
git-workflow-manager (commit and PR)
```

## Implementation Checklist

### Pre-Migration
- [ ] Backup production database
- [ ] Test migration on production-like dataset
- [ ] Verify rollback procedures work
- [ ] Document rollback decision points
- [ ] Prepare monitoring dashboards

### Phase 1: Expand
- [ ] Write migration to add new column (nullable)
- [ ] Run migration in staging
- [ ] Verify old code still works
- [ ] Deploy to production
- [ ] Monitor for errors

### Phase 2: Dual-Write
- [ ] Update code to write to both columns
- [ ] Deploy code change
- [ ] Verify both columns being written
- [ ] Monitor for inconsistencies

### Phase 3: Backfill
- [ ] Create migration progress tracking table
- [ ] Write backfill script with batching
- [ ] Test backfill on staging
- [ ] Run backfill on production
- [ ] Verify 100% data migrated
- [ ] Compare checksums (old vs new)

### Phase 4: Switch Reads
- [ ] Add feature flag to code
- [ ] Deploy code with flag disabled
- [ ] Enable flag for 10% of traffic
- [ ] Monitor for errors
- [ ] Gradually increase to 100%

### Phase 5: Contract
- [ ] Wait 1-2 weeks with flag at 100%
- [ ] Verify no rollback needed
- [ ] Remove old column reference in code
- [ ] Deploy code changes
- [ ] Run migration to drop old column
- [ ] Clean up feature flag

## Validation Criteria

### Success Metrics
- [ ] Zero downtime during migration
- [ ] 100% data migrated successfully
- [ ] No data loss or corruption
- [ ] Old code works during expand phase
- [ ] New code works during contract phase
- [ ] Rollback procedures tested and verified

### Common Failure Modes

**1. Lock Contention During Index Creation**
- Use `CREATE INDEX CONCURRENTLY` (PostgreSQL)
- Use `ALGORITHM=INPLACE` (MySQL 8+)
- Avoid blocking operations during peak hours

**2. Backfill Too Slow**
- Increase batch size
- Reduce pause between batches
- Parallelize across multiple workers
- Add indexes before backfill

**3. Data Inconsistency**
- Verify dual-write is working
- Check for race conditions
- Run data validation queries

## Examples and Usage

### Example 1: Rename Column (users.name → users.full_name)

**Phase 1: Add new column**
```sql
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
```

**Phase 2: Dual-write**
```typescript
await db.query(
  'UPDATE users SET full_name = $1, name = $1 WHERE id = $2',
  [fullName, userId]
);
```

**Phase 3: Backfill**
```sql
UPDATE users SET full_name = name WHERE full_name IS NULL;
```

**Phase 4: Switch reads**
```typescript
const user = await db.query('SELECT full_name FROM users WHERE id = $1');
```

**Phase 5: Drop old column**
```sql
ALTER TABLE users DROP COLUMN name;
```

### Example 2: Change Data Type (users.age TEXT → INTEGER)

**Phase 1: Add new column**
```sql
ALTER TABLE users ADD COLUMN age_int INTEGER;
```

**Phase 2: Dual-write with conversion**
```typescript
const ageInt = parseInt(ageText, 10);
await db.query(
  'UPDATE users SET age = $1, age_int = $2 WHERE id = $3',
  [ageText, ageInt, userId]
);
```

**Phase 3: Backfill with validation**
```sql
UPDATE users 
SET age_int = CAST(age AS INTEGER)
WHERE age_int IS NULL
  AND age ~ '^[0-9]+$';  -- Only valid integers
```

**Phase 4: Switch reads**
```typescript
const user = await db.query('SELECT age_int AS age FROM users WHERE id = $1');
```

**Phase 5: Drop old column**
```sql
ALTER TABLE users DROP COLUMN age;
ALTER TABLE users RENAME COLUMN age_int TO age;
```

## Troubleshooting

### Migration Stuck/Slow
- Check for long-running transactions blocking migration
- Monitor database locks (`pg_locks` in PostgreSQL)
- Reduce batch size or increase pause duration

### Data Inconsistencies After Backfill
- Run validation query comparing old and new columns
- Check for race conditions in dual-write code
- Re-run backfill for inconsistent rows

### Cannot Rollback Safely
- If in Phase 1-4: Rollback code/feature flag
- If in Phase 5: Restore from backup (last resort)
- Always wait 1-2 weeks before Phase 5

## References

- [Expand-Contract Pattern](https://martinfowler.com/bliki/ParallelChange.html)
- [PostgreSQL Concurrent Indexes](https://www.postgresql.org/docs/current/sql-createindex.html)
- [MySQL Online DDL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl.html)
- [Database Migrations at Scale](https://stripe.com/blog/online-migrations)

---

**Pattern Version**: 1.0.0  
**Last Updated**: 2025-11-08  
**Maintained By**: claude-oak-agents community
