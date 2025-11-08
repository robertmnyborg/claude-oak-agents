---
domain: data
priority: 1
primary_agent: infrastructure-specialist
secondary_agents: [systems-architect, security-auditor, qa-specialist]
related_agents: [debug-specialist, dependency-scanner]
---

# Domain: Data Engineering & Database Management

## Tech Stack

### Databases (Top 10)
**Relational**: PostgreSQL 14+, MySQL 8.0+, Amazon Aurora, Amazon RDS
**NoSQL**: MongoDB 5.0+, DynamoDB, Redis, ElastiCache
[Database Selection Guide](https://aws.amazon.com/products/databases/)

### Data Warehouses (Top 3)
**Cloud Platforms**: Amazon Redshift, Snowflake, Google BigQuery
[Data Warehouse Comparison](https://aws.amazon.com/redshift/)

### Data Processing & ETL (Top 5)
**Orchestration**: Apache Airflow (MWAA), AWS Glue, dbt
**Processing**: Apache Spark (EMR), AWS Glue, dbt
[ETL Tools Comparison](https://www.getdbt.com/)

### Streaming & Events (Top 5)
**Real-Time**: Amazon Kinesis, Apache Kafka
**Change Capture**: DynamoDB Streams, Debezium
**Event Bus**: EventBridge, SNS/SQS
[Streaming Architecture Guide](https://aws.amazon.com/kinesis/)

### Storage & Migration (Top 5)
**Object Storage**: Amazon S3, S3 Glacier, EBS, EFS
**Migration**: AWS DMS, AWS DataSync, Change Data Capture
[Data Migration Best Practices](https://aws.amazon.com/dms/)

### Data Access Layers (Top 5)
**ORMs**: Prisma, TypeORM, Mongoose, Sequelize
**Query Tools**: SQL, Elasticsearch, OpenSearch, Athena
[ORM Comparison](https://www.prisma.io/docs/overview/why-prisma)

## Patterns & Conventions

### Database Design Patterns
1. **Normalization**: Reduce redundancy (3NF for OLTP)
2. **Denormalization**: Optimize reads (data warehouses)
3. **Sharding**: Horizontal partitioning for scale
4. **Replication**: Read replicas for high availability
5. **Indexing Strategy**: Balance read vs write performance

### Data Modeling Best Practices
1. **Entity-Relationship Modeling**: Clear relationships
2. **Schema Versioning**: Track schema changes
3. **Data Types**: Use appropriate types (avoid TEXT for everything)
4. **Constraints**: Foreign keys, unique, not null
5. **Audit Columns**: created_at, updated_at, deleted_at (soft delete)

### Migration Strategies
1. **Version Control**: All migrations in git
2. **Idempotent Migrations**: Safe to re-run
3. **Reversible Migrations**: Up and down scripts
4. **Zero-Downtime**: Backward-compatible changes
5. **Testing**: Test migrations on staging first

### Zero-Downtime Migration Pattern
```
Phase 1: Add new column (nullable)
Phase 2: Deploy code to write to both old and new
Phase 3: Backfill data
Phase 4: Deploy code to read from new column
Phase 5: Remove old column (after verification)
```

### Query Optimization
1. **Use Indexes**: On frequently queried columns
2. **Avoid N+1 Queries**: Use joins or eager loading
3. **Limit Result Sets**: Pagination, filtering
4. **Query Planning**: Use EXPLAIN to analyze
5. **Connection Pooling**: Reuse database connections

### Data Integrity
1. **Referential Integrity**: Foreign key constraints
2. **Data Validation**: Check constraints, triggers
3. **Transactions**: ACID properties for critical operations
4. **Backup Strategy**: Regular automated backups
5. **Disaster Recovery**: Point-in-time recovery

### Caching Strategies
1. **Cache-Aside**: Application manages cache
2. **Write-Through**: Write to cache and DB simultaneously
3. **Write-Behind**: Write to cache, async to DB
4. **Read-Through**: Cache handles DB reads
5. **TTL (Time-To-Live)**: Auto-expire cached data

### ETL/ELT Patterns
1. **Extract**: Pull data from sources (APIs, databases, files)
2. **Transform**: Clean, enrich, aggregate data
3. **Load**: Write to destination (data warehouse, database)
4. **Incremental Loading**: Only process new/changed data
5. **Idempotency**: Safe to re-run pipelines

## Data Architecture Patterns

### Lambda Architecture
```
Batch Layer (historical) + Speed Layer (real-time) + Serving Layer
├── Batch: S3 → Glue → Redshift (hourly/daily)
├── Speed: Kinesis → Lambda → DynamoDB (real-time)
└── Serving: Query both layers, merge results
```

### Data Lake Architecture
```
Raw Data (S3) → Processed Data (S3) → Curated Data (S3/Redshift)
├── Bronze Layer: Raw, unprocessed data
├── Silver Layer: Cleaned, validated data
└── Gold Layer: Business-ready, aggregated data
```

### Change Data Capture (CDC)
```
MongoDB → Change Stream → Lambda → S3/Kinesis → Analytics
DynamoDB → DynamoDB Streams → Lambda → Aggregation
```

### Medallion Architecture (dbt)
```
Source → Bronze (raw) → Silver (cleaned) → Gold (business metrics)
```

## File & Code Organization

### Database Project Structure
```
database/
├── migrations/
│   ├── 001_create_users_table.sql
│   ├── 002_add_email_index.sql
│   └── 003_add_roles_table.sql
├── seeds/
│   ├── dev/
│   │   └── users.sql
│   └── test/
│       └── test_data.sql
├── schemas/
│   ├── users.sql
│   ├── orders.sql
│   └── products.sql
├── indexes/
│   └── performance_indexes.sql
├── triggers/
│   └── audit_triggers.sql
└── README.md
```

### dbt Project Structure
```
dbt/
├── models/
│   ├── staging/         # Bronze layer (source data)
│   │   ├── stg_users.sql
│   │   └── stg_orders.sql
│   ├── intermediate/    # Silver layer (cleaned)
│   │   └── int_user_orders.sql
│   └── marts/           # Gold layer (business metrics)
│       ├── fct_orders.sql
│       └── dim_users.sql
├── tests/
│   └── assert_positive_amounts.sql
├── macros/
│   └── generate_schema_name.sql
└── dbt_project.yml
```

### ETL Project Structure
```
etl/
├── dags/                # Airflow DAGs
│   ├── daily_user_sync.py
│   └── hourly_metrics.py
├── tasks/               # Task definitions
│   ├── extract/
│   ├── transform/
│   └── load/
├── utils/
│   ├── connections.py
│   └── helpers.py
└── config/
    └── connections.yml
```

## Agent Workflows

### Database Schema Design
**Trigger**: "Design database schema for users", "Create ERD"
```
spec-manager → systems-architect → infrastructure-specialist → security-auditor → git-workflow-manager
```

### Database Migration
**Trigger**: "Add new column to users table", "Create migration for orders"
```
infrastructure-specialist → qa-specialist (staging test) → git-workflow-manager
```

### Query Optimization
**Trigger**: "Slow query on users table", "Optimize report generation"
```
debug-specialist (analyze query) → infrastructure-specialist (add indexes, rewrite query) → qa-specialist (verify performance)
```

### ETL Pipeline Development
**Trigger**: "Build daily data sync from MongoDB to Redshift"
```
spec-manager → systems-architect (design pipeline) → infrastructure-specialist (implement) → qa-specialist → git-workflow-manager
```

### Data Migration
**Trigger**: "Migrate from MySQL to PostgreSQL"
```
systems-architect (migration strategy) → infrastructure-specialist (implement) → qa-specialist (data validation) → git-workflow-manager
```

### Cache Implementation
**Trigger**: "Add Redis caching for user queries"
```
systems-architect → infrastructure-specialist → qa-specialist → git-workflow-manager
```

### Backup & Recovery
**Trigger**: "Set up automated backups", "Restore from backup"
```
infrastructure-specialist → security-auditor (verify encryption) → git-workflow-manager
```

## Triggers

### Keywords
- **Database**: database, DB, schema, table, query, SQL, NoSQL
- **Data operations**: migration, ETL, pipeline, sync, replication
- **MongoDB**: MongoDB, Mongoose, collection, document
- **PostgreSQL**: PostgreSQL, Postgres, psql, pgAdmin
- **DynamoDB**: DynamoDB, NoSQL, key-value
- **Data warehouse**: Redshift, Snowflake, warehouse, analytics
- **Caching**: Redis, cache, ElastiCache, Memcached
- **Performance**: slow query, optimization, index, performance
- **Data processing**: Airflow, Glue, dbt, transform, aggregate
- **Streaming**: Kinesis, Kafka, stream, real-time

### File Patterns
- `database/**/*`, `db/**/*`
- `migrations/**/*`
- `*.sql`, `*.ddl`
- `dbt/**/*`, `models/**/*`
- `airflow/**/*`, `dags/**/*`
- `*.model.ts`, `*.schema.ts`
- `*.repository.ts`

### Tech Stack Mentions
- PostgreSQL, MySQL, MongoDB, DynamoDB, Redis
- Mongoose, TypeORM, Prisma, Sequelize
- Airflow, Glue, dbt, Spark
- Kinesis, Kafka, EventBridge
- Redshift, Snowflake, Athena

## Quality Standards

### Schema Design Standards
- Use appropriate data types (INT, VARCHAR, TIMESTAMP)
- Primary keys on all tables
- Foreign keys for relationships
- Indexes on frequently queried columns
- NOT NULL where appropriate
- Default values where sensible
- Audit columns (created_at, updated_at)
- Soft delete (deleted_at) when needed

### Migration Standards
- Version-controlled migrations
- Test on staging before production
- Backward-compatible changes
- Include rollback script
- Document breaking changes
- No data loss in production

### Query Performance Standards
- Query execution time: < 100ms (OLTP)
- Use EXPLAIN ANALYZE for optimization
- Avoid SELECT *
- Use appropriate indexes
- Limit result sets (pagination)
- Connection pooling enabled

### Data Quality Standards
- No NULL in required fields
- Referential integrity maintained
- Data validation at write time
- Regular data quality checks
- Duplicate detection and removal
- Data type consistency

### Backup & Recovery Standards
- Daily automated backups
- Point-in-time recovery enabled
- Backup retention: 30 days minimum
- Monthly restore testing
- Backup encryption enabled
- Multi-region backups for critical data

## Common Data Tasks

### Creating a Database Migration
1. **Generate Migration File**:
   ```bash
   # Sequelize
   npx sequelize migration:generate --name add-email-to-users

   # TypeORM
   npm run migration:generate -- -n AddEmailToUsers

   # Prisma
   npx prisma migrate dev --name add-email-to-users
   ```

2. **Write Migration**:
   ```sql
   -- Up migration
   ALTER TABLE users ADD COLUMN email VARCHAR(255) UNIQUE;
   CREATE INDEX idx_users_email ON users(email);

   -- Down migration
   DROP INDEX idx_users_email;
   ALTER TABLE users DROP COLUMN email;
   ```

3. **Test Migration**:
   ```bash
   # Apply on staging
   npm run migrate:up

   # Verify schema
   # Test application

   # Rollback if needed
   npm run migrate:down
   ```

4. **Apply to Production**:
   ```bash
   # During maintenance window or as zero-downtime
   npm run migrate:up
   ```

### Optimizing a Slow Query
1. **Identify Slow Query**:
   ```sql
   -- PostgreSQL slow query log
   SELECT query, mean_exec_time, calls
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 10;
   ```

2. **Analyze Query Plan**:
   ```sql
   EXPLAIN ANALYZE
   SELECT u.*, o.total
   FROM users u
   JOIN orders o ON u.id = o.user_id
   WHERE u.created_at > '2024-01-01';
   ```

3. **Identify Issues**:
   - Sequential scan instead of index scan
   - N+1 query problem
   - Missing indexes
   - Inefficient joins

4. **Optimize**:
   ```sql
   -- Add index
   CREATE INDEX idx_users_created_at ON users(created_at);

   -- Rewrite query
   SELECT u.*, o.total
   FROM users u
   JOIN orders o ON u.id = o.user_id
   WHERE u.created_at > '2024-01-01'
   LIMIT 100;  -- Add pagination
   ```

5. **Verify Improvement**:
   ```sql
   EXPLAIN ANALYZE [optimized query]
   -- Compare execution time
   ```

### Setting Up MongoDB Change Streams
1. **Create Change Stream Listener**:
   ```typescript
   const changeStream = db.collection('users').watch();

   changeStream.on('change', async (change) => {
     console.log('Change detected:', change);

     switch (change.operationType) {
       case 'insert':
         await handleUserCreated(change.fullDocument);
         break;
       case 'update':
         await handleUserUpdated(change.documentKey, change.updateDescription);
         break;
       case 'delete':
         await handleUserDeleted(change.documentKey);
         break;
     }
   });
   ```

2. **Lambda Handler for Change Stream**:
   ```typescript
   export const handler = async (event: DynamoDBStreamEvent) => {
     for (const record of event.Records) {
       if (record.eventName === 'INSERT') {
         const newItem = unmarshall(record.dynamodb.NewImage);
         await publishEvent('user.created', newItem);
       }
     }
   };
   ```

### Creating dbt Models
1. **Staging Model** (Bronze):
   ```sql
   -- models/staging/stg_users.sql
   WITH source AS (
     SELECT * FROM {{ source('mongodb', 'users') }}
   )

   SELECT
     _id AS user_id,
     email,
     created_at,
     updated_at
   FROM source
   ```

2. **Intermediate Model** (Silver):
   ```sql
   -- models/intermediate/int_user_orders.sql
   SELECT
     u.user_id,
     u.email,
     COUNT(o.order_id) AS total_orders,
     SUM(o.amount) AS total_spent
   FROM {{ ref('stg_users') }} u
   LEFT JOIN {{ ref('stg_orders') }} o ON u.user_id = o.user_id
   GROUP BY u.user_id, u.email
   ```

3. **Mart Model** (Gold):
   ```sql
   -- models/marts/fct_user_metrics.sql
   SELECT
     user_id,
     email,
     total_orders,
     total_spent,
     CASE
       WHEN total_spent > 1000 THEN 'VIP'
       WHEN total_spent > 500 THEN 'Premium'
       ELSE 'Standard'
     END AS customer_tier
   FROM {{ ref('int_user_orders') }}
   ```

4. **Run dbt**:
   ```bash
   dbt run --models stg_users
   dbt run --models int_user_orders
   dbt run --models fct_user_metrics

   # Run all
   dbt run

   # Test
   dbt test
   ```

### Implementing Redis Caching
1. **Setup Redis Client**:
   ```typescript
   import Redis from 'ioredis';

   const redis = new Redis({
     host: process.env.REDIS_HOST,
     port: 6379,
     password: process.env.REDIS_PASSWORD,
   });
   ```

2. **Cache-Aside Pattern**:
   ```typescript
   async function getUser(userId: string) {
     // Try cache first
     const cached = await redis.get(`user:${userId}`);
     if (cached) {
       return JSON.parse(cached);
     }

     // Cache miss - fetch from DB
     const user = await User.findById(userId);

     // Store in cache (TTL: 1 hour)
     await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));

     return user;
   }
   ```

3. **Cache Invalidation**:
   ```typescript
   async function updateUser(userId: string, data: any) {
     // Update database
     const user = await User.findByIdAndUpdate(userId, data, { new: true });

     // Invalidate cache
     await redis.del(`user:${userId}`);

     return user;
   }
   ```

## Integration Points

### Frontend Integration
- **API Data Fetching**: REST/GraphQL endpoints serve data
- **Caching**: Client-side + server-side caching strategy
- **Pagination**: Cursor-based or offset pagination
- **Real-time**: WebSocket for live data updates

### Backend Integration
- **ORM/ODM**: Mongoose, TypeORM, Prisma for data access
- **Repository Pattern**: Abstract data layer
- **Query Builders**: Construct complex queries
- **Transactions**: ACID guarantees for critical operations

### Infrastructure Integration
- **RDS/DynamoDB**: Managed database services
- **Backup Automation**: Automated snapshots
- **Monitoring**: CloudWatch metrics, slow query logs
- **Secrets Management**: Database credentials in Secrets Manager

### Security Integration
- **Encryption at Rest**: KMS for RDS, DynamoDB
- **Encryption in Transit**: TLS for database connections
- **Access Control**: Database-level permissions, IAM
- **Audit Logging**: Track data access and modifications

## Domain-Specific Commands

### PostgreSQL
```bash
# Connect to database
psql -h hostname -U username -d database

# List databases
\l

# Connect to database
\c database_name

# List tables
\dt

# Describe table
\d table_name

# Run query
SELECT * FROM users LIMIT 10;

# Execute SQL file
psql -h hostname -U username -d database -f migration.sql

# Dump database
pg_dump -h hostname -U username database > backup.sql

# Restore database
psql -h hostname -U username database < backup.sql
```

### MongoDB
```bash
# Connect to MongoDB
mongosh "mongodb://host:27017/database"

# Show databases
show dbs

# Use database
use mydb

# Show collections
show collections

# Find documents
db.users.find({ email: "test@example.com" })

# Count documents
db.users.countDocuments()

# Create index
db.users.createIndex({ email: 1 }, { unique: true })

# Backup
mongodump --uri="mongodb://host:27017/database" --out=/backup

# Restore
mongorestore --uri="mongodb://host:27017/database" /backup/database
```

### Migrations
```bash
# Sequelize
npx sequelize migration:generate --name migration-name
npx sequelize db:migrate
npx sequelize db:migrate:undo

# TypeORM
npm run migration:generate -- -n MigrationName
npm run migration:run
npm run migration:revert

# Prisma
npx prisma migrate dev --name migration-name
npx prisma migrate deploy
npx prisma migrate reset
```

### dbt
```bash
# Run models
dbt run
dbt run --models model_name
dbt run --models staging.*

# Test
dbt test
dbt test --models model_name

# Generate docs
dbt docs generate
dbt docs serve

# Compile (no execution)
dbt compile

# Debug connection
dbt debug
```

### Redis
```bash
# Connect to Redis
redis-cli -h hostname -p 6379

# Get key
GET key_name

# Set key with expiration
SETEX key_name 3600 "value"

# Delete key
DEL key_name

# List all keys (use cautiously)
KEYS *

# Check TTL
TTL key_name

# Flush all (dangerous!)
FLUSHALL
```

### AWS DynamoDB
```bash
# List tables
aws dynamodb list-tables

# Describe table
aws dynamodb describe-table --table-name Users

# Get item
aws dynamodb get-item --table-name Users --key '{"id": {"S": "123"}}'

# Put item
aws dynamodb put-item --table-name Users --item '{"id": {"S": "123"}, "email": {"S": "test@example.com"}}'

# Query (requires partition key)
aws dynamodb query --table-name Users --key-condition-expression "id = :id" --expression-attribute-values '{":id": {"S": "123"}}'

# Scan (expensive)
aws dynamodb scan --table-name Users
```

## Decision Framework

### When to Use This Domain
- ✅ Designing database schemas
- ✅ Writing/optimizing queries
- ✅ Creating database migrations
- ✅ Setting up caching
- ✅ Building ETL/data pipelines
- ✅ Data modeling and warehousing
- ✅ Database performance tuning
- ✅ Backup and recovery planning

### When to Coordinate with Other Domains
- **Backend**: Data access patterns, repository implementation
- **Infrastructure**: Database provisioning, RDS/DynamoDB setup
- **Security**: Encryption, access control, audit logging
- **Frontend**: API response structure, pagination

### Database Technology Selection
```
Use PostgreSQL when:
- Complex relationships and joins
- ACID transactions required
- Strong consistency needed
- SQL expertise on team

Use MongoDB when:
- Flexible schema requirements
- Document-oriented data
- Horizontal scaling needed
- Rapid iteration on schema

Use DynamoDB when:
- Serverless architecture
- Predictable read/write patterns
- Single-digit millisecond latency
- AWS-native stack

Use Redis when:
- Caching frequently accessed data
- Session storage
- Real-time leaderboards/counters
- Pub/sub messaging
```

## Example Scenarios

### Scenario 1: Add Index to Improve Query Performance
**Request**: "Query on users table is slow"

**Domain Detection**: Data (keywords: query, slow, performance)

**Workflow**:
```
debug-specialist:
  1. Analyze slow query:
     SELECT * FROM users WHERE email = 'test@example.com'

  2. Run EXPLAIN ANALYZE:
     Seq Scan on users (cost=0.00..1000.00 rows=1)
     Planning Time: 0.5ms
     Execution Time: 250ms  <- SLOW

infrastructure-specialist:
  1. Create index migration:
     -- migrations/add_email_index.sql
     CREATE INDEX idx_users_email ON users(email);

  2. Test on staging:
     - Apply migration
     - Run EXPLAIN ANALYZE again
     - Verify index used: Index Scan using idx_users_email
     - Execution Time: 2ms  <- FAST

  3. Apply to production:
     CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
     -- CONCURRENTLY allows reads/writes during index creation

qa-specialist:
  - Verify query performance improved
  - Test application functionality unchanged

git-workflow-manager:
  - Commit migration
  - Document performance improvement
```

### Scenario 2: Zero-Downtime Schema Change
**Request**: "Add 'phone_number' column to users table"

**Domain Detection**: Data (keywords: add column, users table)

**Workflow**:
```
infrastructure-specialist:
  Phase 1: Add nullable column
    CREATE TABLE migration:
    ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) NULL;

    Deploy application (v1.1):
    - Writes to phone_number when provided
    - Reads work without phone_number

  Phase 2: Backfill data (if needed)
    UPDATE users SET phone_number = legacy_phone WHERE phone_number IS NULL;

  Phase 3: Make column NOT NULL (if required)
    CREATE migration:
    ALTER TABLE users ALTER COLUMN phone_number SET NOT NULL;

    Deploy application (v1.2):
    - Requires phone_number in all writes

security-auditor:
  - Check if phone_number contains PII
  - Verify encryption requirements
  - Add to data masking rules

qa-specialist:
  - Test backward compatibility
  - Verify no downtime during migration
```

## Anti-Patterns to Avoid

### Database Design Anti-Patterns
1. **God Tables**: Tables with 50+ columns
2. **Entity-Attribute-Value (EAV)**: Storing data as key-value pairs in tables
3. **No Indexes**: Causing slow queries
4. **Too Many Indexes**: Slowing down writes
5. **Using VARCHAR for Everything**: Inefficient storage
6. **No Foreign Keys**: No referential integrity
7. **Premature Denormalization**: Before proving need

### Query Anti-Patterns
- **SELECT ***: Fetching unnecessary data
- **N+1 Queries**: Loop with query per iteration
- **No Pagination**: Loading millions of rows
- **Ignoring EXPLAIN**: Not analyzing query plans
- **Cartesian Products**: Joins without conditions

### Migration Anti-Patterns
- **No Rollback Strategy**: Can't undo migrations
- **Direct Production Changes**: Not testing on staging
- **Breaking Changes**: No backward compatibility
- **Large Migrations**: Locking tables for hours

## Success Metrics

### Performance Metrics
- Query response time: < 100ms (p95)
- Database CPU utilization: < 70%
- Connection pool usage: < 80%
- Cache hit rate: > 80%
- Replication lag: < 5 seconds

### Reliability Metrics
- Database uptime: > 99.95%
- Successful backups: 100%
- Migration success rate: 100%
- Zero data loss incidents

### Data Quality Metrics
- Null rate in required fields: 0%
- Duplicate rate: < 0.1%
- Referential integrity violations: 0
- Schema drift incidents: 0

## Resources & References

### Documentation
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [MongoDB Manual](https://docs.mongodb.com/)
- [DynamoDB Guide](https://docs.aws.amazon.com/dynamodb/)
- [Redis Documentation](https://redis.io/documentation)

### Data Modeling
- [Database Design](https://www.ibm.com/topics/database-design)
- [Normalization Guide](https://www.studytonight.com/dbms/database-normalization.php)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)

### Performance Tuning
- [PostgreSQL Performance](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [MongoDB Performance](https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/)
- [Use The Index, Luke](https://use-the-index-luke.com/)
