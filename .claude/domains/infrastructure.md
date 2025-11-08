---
domain: infrastructure
priority: 1
primary_agent: infrastructure-specialist
secondary_agents: [security-auditor, dependency-scanner, git-workflow-manager]
related_agents: [systems-architect, debug-specialist]
---

# Domain: Infrastructure & DevOps

## Tech Stack

### Infrastructure as Code (IaC)
- **AWS CDK**: TypeScript-based infrastructure definitions
- **Terraform**: Multi-cloud infrastructure provisioning
- **CloudFormation**: Native AWS infrastructure templates
- **Serverless Framework**: Serverless application deployment

### Cloud Providers
- **AWS (Primary)**:
  - Compute: EC2, ECS, EKS, Lambda, Fargate
  - Storage: S3, EBS, EFS, Glacier
  - Database: RDS, DynamoDB, ElastiCache, DocumentDB
  - Network: VPC, CloudFront, Route53, ALB/NLB, API Gateway
  - Monitoring: CloudWatch, X-Ray, CloudTrail
  - Security: IAM, KMS, Secrets Manager, WAF, Shield
  - Messaging: SNS, SQS, EventBridge, Kinesis

### Containerization & Orchestration
- **Docker**: Container runtime and image management
- **Docker Compose**: Local multi-container orchestration
- **Kubernetes**: Container orchestration (EKS)
- **Amazon ECS**: AWS-native container orchestration
- **Amazon ECR**: Docker image registry

### CI/CD Platforms
- **GitHub Actions**: Automated workflows
- **GitLab CI/CD**: Pipeline automation
- **AWS CodePipeline**: Native AWS CI/CD
- **Jenkins**: Self-hosted automation server

### Configuration Management
- **Ansible**: Server configuration automation
- **AWS Systems Manager**: Parameter Store, Session Manager
- **Consul**: Service discovery and configuration
- **Environment Variables**: `.env` files, AWS Parameter Store

### Monitoring & Observability
- **Logging**: CloudWatch Logs, ELK Stack, Datadog
- **Metrics**: CloudWatch Metrics, Prometheus, Grafana
- **Tracing**: AWS X-Ray, Jaeger, OpenTelemetry
- **APM**: New Relic, Datadog APM, Sentry
- **Alerting**: CloudWatch Alarms, PagerDuty, Opsgenie

## Patterns & Conventions

### CDK Project Structure
```
infrastructure/
├── bin/
│   └── app.ts              # CDK app entry point
├── lib/
│   ├── stacks/
│   │   ├── vpc-stack.ts    # Network infrastructure
│   │   ├── compute-stack.ts # EC2, ECS, Lambda
│   │   ├── data-stack.ts   # Databases, S3
│   │   └── frontend-stack.ts # S3, CloudFront
│   ├── constructs/         # Reusable CDK constructs
│   │   ├── lambda-function.ts
│   │   └── static-site.ts
│   └── config/
│       ├── dev.ts          # Dev environment config
│       ├── prod.ts         # Prod environment config
│       └── types.ts        # TypeScript types
├── cdk.json               # CDK configuration
└── tsconfig.json          # TypeScript config
```

### Serverless Framework Structure
```
serverless/
├── functions/
│   ├── http/              # API Gateway functions
│   ├── events/            # Event-driven functions
│   └── scheduled/         # Cron jobs
├── resources/
│   ├── dynamodb.yml       # DynamoDB tables
│   ├── s3.yml             # S3 buckets
│   └── sns-sqs.yml        # Messaging resources
├── serverless.yml         # Main configuration
└── serverless/
    ├── base.yml           # Base configuration
    ├── dev.yml            # Dev overrides
    └── prod.yml           # Prod overrides
```

### Docker Best Practices
1. **Multi-stage Builds**: Reduce image size
2. **Layer Caching**: Order commands for optimal caching
3. **Security**: Use official base images, scan for vulnerabilities
4. **Size Optimization**: Use Alpine images when possible
5. **.dockerignore**: Exclude unnecessary files

### Environment Management
1. **Environment Separation**: dev, staging, prod isolated
2. **Configuration as Code**: Infrastructure defined in version control
3. **Secrets Management**: AWS Secrets Manager, never in code
4. **Parameter Store**: Non-sensitive configuration
5. **Environment Variables**: Runtime configuration

### Deployment Strategies
1. **Blue-Green Deployment**: Zero-downtime deployments
2. **Canary Deployment**: Gradual rollout to subset
3. **Rolling Deployment**: Incremental instance updates
4. **Immutable Infrastructure**: Replace vs. update servers
5. **Database Migrations**: Zero-downtime schema changes

### High Availability Patterns
1. **Multi-AZ Deployment**: Distribute across availability zones
2. **Auto Scaling**: Automatic capacity adjustment
3. **Load Balancing**: Distribute traffic (ALB, NLB)
4. **Health Checks**: Automated instance monitoring
5. **Disaster Recovery**: Backup and restore strategies

### Cost Optimization
1. **Right-Sizing**: Match resources to actual needs
2. **Reserved Instances**: Commitment discounts for stable workloads
3. **Spot Instances**: Interruptible workloads at lower cost
4. **Auto Scaling**: Scale down when not needed
5. **S3 Lifecycle Policies**: Move to cheaper storage tiers
6. **CloudWatch Cost Monitoring**: Track and alert on costs

## Infrastructure Patterns

### Static Website (S3 + CloudFront)
```typescript
// CDK Stack
const bucket = new s3.Bucket(this, 'WebsiteBucket', {
  websiteIndexDocument: 'index.html',
  publicReadAccess: false,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
});

const distribution = new cloudfront.Distribution(this, 'CDN', {
  defaultBehavior: {
    origin: new origins.S3Origin(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
  },
  domainNames: ['example.com'],
  certificate: cert,
});
```

### Serverless API (Lambda + API Gateway)
```yaml
# serverless.yml
functions:
  getUser:
    handler: src/handlers/users/get.handler
    events:
      - httpApi:
          path: /users/{id}
          method: get
    environment:
      TABLE_NAME: ${self:custom.tableName}
    iamRoleStatements:
      - Effect: Allow
        Action:
          - dynamodb:GetItem
        Resource: !GetAtt UsersTable.Arn
```

### Containerized Application (ECS Fargate)
```typescript
// CDK Stack
const cluster = new ecs.Cluster(this, 'AppCluster', { vpc });

const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef');
taskDefinition.addContainer('app', {
  image: ecs.ContainerImage.fromRegistry('myapp:latest'),
  memoryLimitMiB: 512,
  environment: {
    NODE_ENV: 'production',
  },
  logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'app' }),
});

const service = new ecs.FargateService(this, 'Service', {
  cluster,
  taskDefinition,
  desiredCount: 2,
});
```

### Event-Driven Architecture (SNS + SQS + Lambda)
```yaml
# serverless.yml
resources:
  Resources:
    UserEventsTopic:
      Type: AWS::SNS::Topic
      Properties:
        TopicName: user-events

    EmailQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: email-queue
        RedrivePolicy:
          deadLetterTargetArn: !GetAtt EmailDLQ.Arn
          maxReceiveCount: 3

functions:
  emailWorker:
    handler: src/workers/email.handler
    events:
      - sqs:
          arn: !GetAtt EmailQueue.Arn
          batchSize: 10
```

## Agent Workflows

### Simple Infrastructure Setup
**Trigger**: "Create S3 bucket for static hosting", "Set up CloudWatch alarm"
```
infrastructure-specialist → security-auditor → git-workflow-manager
```

### Full Application Deployment
**Trigger**: "Deploy application to AWS", "Set up production environment"
```
systems-architect → infrastructure-specialist → security-auditor → dependency-scanner → git-workflow-manager
```

### CDK Stack Development
**Trigger**: "Create CDK stack for Lambda functions", "Deploy with CDK"
```
infrastructure-specialist → security-auditor → git-workflow-manager
```

### Docker Containerization
**Trigger**: "Dockerize Node.js app", "Create multi-stage Dockerfile"
```
infrastructure-specialist → security-auditor (image scan) → git-workflow-manager
```

### CI/CD Pipeline Setup
**Trigger**: "Set up GitHub Actions pipeline", "Automate deployment"
```
systems-architect → infrastructure-specialist → security-auditor → git-workflow-manager
```

### Monitoring & Alerting
**Trigger**: "Set up CloudWatch alarms", "Configure error tracking"
```
infrastructure-specialist → git-workflow-manager
```

### Troubleshooting & Debugging
**Trigger**: "CloudFormation stack failed", "Lambda function timing out"
```
debug-specialist → infrastructure-specialist (fix) → git-workflow-manager
```

## Triggers

### Keywords
- **Infrastructure**: infrastructure, IaC, CDK, CloudFormation, Terraform
- **Cloud Services**: AWS, Lambda, S3, EC2, RDS, DynamoDB, CloudFront
- **Deployment**: deploy, deployment, CI/CD, pipeline, release
- **Containers**: Docker, Dockerfile, container, ECS, Kubernetes, K8s
- **Monitoring**: monitoring, logging, CloudWatch, alerts, metrics
- **Networking**: VPC, network, load balancer, API Gateway, Route53
- **Serverless**: serverless, Lambda, API Gateway, Step Functions
- **DevOps**: DevOps, automation, provisioning, orchestration

### File Patterns
- `infrastructure/**/*`, `infra/**/*`
- `cdk.json`, `bin/**/*.ts`, `lib/**/*.ts`
- `serverless.yml`, `serverless/**/*.yml`
- `Dockerfile`, `docker-compose.yml`
- `.github/workflows/**/*`
- `terraform/**/*.tf`
- `cloudformation/**/*.yml`

### Tech Stack Mentions
- AWS CDK, CloudFormation, Terraform
- Docker, Kubernetes, ECS, Fargate
- Lambda, API Gateway, S3, CloudFront
- GitHub Actions, GitLab CI, Jenkins
- CloudWatch, X-Ray, Sentry

## Quality Standards

### Infrastructure Code Quality
- **TypeScript Strict Mode**: All CDK code strictly typed
- **CDK Best Practices**: Follow AWS CDK patterns
- **Resource Tagging**: All resources tagged (Environment, Project, Owner)
- **Naming Conventions**: Consistent resource naming
- **No Hardcoded Values**: Use parameters/environment variables

### Security Standards
- **Least Privilege IAM**: Minimal required permissions
- **Encryption**: Encrypt data at rest and in transit
- **Network Isolation**: Use VPCs, security groups, NACLs
- **Secrets Management**: AWS Secrets Manager, no plaintext secrets
- **Security Scanning**: Scan Docker images, dependencies
- **WAF**: Web Application Firewall for public endpoints
- **Audit Logging**: CloudTrail for all API calls

### Deployment Standards
- **Automated Deployments**: No manual deployments to production
- **Infrastructure Testing**: Validate CDK synth output
- **Rollback Strategy**: Automated rollback on failure
- **Change Management**: Document infrastructure changes
- **Version Control**: All infrastructure code in git

### Monitoring Requirements
- **CloudWatch Dashboards**: Visualize key metrics
- **Log Aggregation**: Centralized logging
- **Alerting**: Automated alerts for critical issues
- **Uptime Monitoring**: Synthetic monitoring for endpoints
- **Cost Monitoring**: Track and alert on cost anomalies

### Performance Metrics
- **Deployment Time**: < 10 minutes for typical deployment
- **Lambda Cold Start**: < 1s
- **API Gateway Latency**: < 50ms overhead
- **CloudFront Cache Hit Rate**: > 80%
- **RDS Connection Time**: < 100ms

## Common Tasks & Solutions

### Creating a CDK Stack
1. Initialize CDK project: `cdk init app --language=typescript`
2. Define stack in `lib/stacks/`
3. Configure environment in `bin/app.ts`
4. Add resources (S3, Lambda, etc.)
5. Define IAM permissions
6. Add tags and naming conventions
7. Synthesize: `cdk synth`
8. Deploy: `cdk deploy`

### Dockerizing an Application
1. Create Dockerfile with multi-stage build
2. Create .dockerignore file
3. Build image: `docker build -t myapp:latest .`
4. Test locally: `docker run -p 3000:3000 myapp:latest`
5. Scan for vulnerabilities: `docker scan myapp:latest`
6. Push to ECR: `docker push <ecr-url>/myapp:latest`

### Setting Up CI/CD Pipeline
1. Define workflow in `.github/workflows/deploy.yml`
2. Configure environment secrets
3. Add build steps (lint, test, build)
4. Add deployment step (CDK deploy, serverless deploy)
5. Configure deployment approvals for production
6. Add notifications (Slack, email)

### Configuring Monitoring
1. Create CloudWatch dashboard
2. Define custom metrics
3. Set up log groups and retention
4. Create alarms for critical metrics
5. Configure SNS notifications
6. Set up X-Ray tracing for distributed systems

### Database Migration (Zero-Downtime)
1. Create new schema version in parallel
2. Deploy application with dual-write (old + new schema)
3. Migrate existing data
4. Deploy application to read from new schema
5. Verify data integrity
6. Remove old schema

## Integration Points

### Frontend Integration
- **S3 + CloudFront**: Static website hosting
- **API Gateway**: REST/GraphQL API endpoints
- **Environment Variables**: Build-time configuration via CDK

### Backend Integration
- **Lambda Functions**: Serverless compute
- **RDS/DynamoDB**: Database provisioning
- **Secrets Manager**: Database credentials, API keys
- **VPC**: Network isolation for backend services

### Data Integration
- **Data Storage**: S3, RDS, DynamoDB, ElastiCache
- **Data Processing**: Lambda, Glue, EMR
- **Data Streaming**: Kinesis, EventBridge

### Security Integration
- **IAM Policies**: Least-privilege access control
- **KMS**: Encryption key management
- **WAF**: Web application firewall rules
- **Security Groups**: Network-level security

## Domain-Specific Commands

### CDK Commands
```bash
# Initialize project
cdk init app --language=typescript

# Synthesize CloudFormation
cdk synth
cdk synth <stack-name>

# Deploy stack
cdk deploy
cdk deploy <stack-name>
cdk deploy --all

# Destroy stack
cdk destroy <stack-name>

# Diff changes
cdk diff

# Bootstrap CDK (first time)
cdk bootstrap aws://<account>/<region>
```

### Serverless Framework
```bash
# Deploy all functions
serverless deploy
serverless deploy --stage prod

# Deploy single function
serverless deploy function -f functionName

# Invoke function locally
serverless invoke local -f functionName

# View logs
serverless logs -f functionName -t

# Remove stack
serverless remove
```

### Docker Commands
```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -p 3000:3000 myapp:latest
docker run -d --name myapp myapp:latest

# View logs
docker logs -f myapp

# Execute command in container
docker exec -it myapp sh

# Scan for vulnerabilities
docker scan myapp:latest

# Push to registry
docker tag myapp:latest <ecr-url>/myapp:latest
docker push <ecr-url>/myapp:latest

# Clean up
docker system prune -a
```

### AWS CLI Commands
```bash
# S3 operations
aws s3 sync ./dist s3://bucket-name
aws s3 ls s3://bucket-name

# CloudFormation
aws cloudformation describe-stacks
aws cloudformation delete-stack --stack-name my-stack

# Lambda
aws lambda invoke --function-name myFunc output.json
aws lambda update-function-code --function-name myFunc --zip-file fileb://function.zip

# Secrets Manager
aws secretsmanager get-secret-value --secret-id my-secret
aws secretsmanager create-secret --name my-secret --secret-string "value"

# CloudWatch Logs
aws logs tail /aws/lambda/functionName --follow
aws logs describe-log-groups
```

### Docker Compose
```bash
# Start services
docker-compose up
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f <service>

# Rebuild
docker-compose build
docker-compose up --build
```

## Decision Framework

### When to Use This Domain
- ✅ Provisioning cloud resources
- ✅ Setting up infrastructure (networks, databases, compute)
- ✅ Deploying applications
- ✅ Configuring CI/CD pipelines
- ✅ Setting up monitoring and logging
- ✅ Managing containers and orchestration
- ✅ Troubleshooting deployment issues

### When to Coordinate with Other Domains
- **Frontend**: Deployment configuration (S3, CloudFront)
- **Backend**: Lambda functions, API Gateway, databases
- **Security**: IAM policies, encryption, network security
- **Data**: Database provisioning, backup strategies

## Example Scenarios

### Scenario 1: Deploy Static Website
**Request**: "Deploy React app to AWS with CDK"

**Domain Detection**: Infrastructure + Frontend (keywords: deploy, AWS, CDK)

**Workflow**:
```
infrastructure-specialist:
  1. Create CDK Stack:
     - S3 bucket with static website hosting
     - CloudFront distribution
     - Route53 DNS record
     - ACM certificate for HTTPS

  2. Configure:
     - Bucket policy for CloudFront OAI
     - CloudFront cache behaviors
     - Error pages (404 → index.html for SPA)
     - Security headers

  3. Deploy:
     - Build frontend: yarn build
     - CDK deploy
     - Sync build artifacts to S3
     - Invalidate CloudFront cache

security-auditor:
  - Verify HTTPS enforcement
  - Check bucket is not publicly accessible
  - Validate CloudFront security headers
  - Review IAM permissions

git-workflow-manager:
  - Commit CDK stack code
  - Create PR with deployment instructions
```

### Scenario 2: Serverless API with Database
**Request**: "Create serverless API with DynamoDB backend"

**Domain Detection**: Infrastructure + Backend (keywords: serverless, API, DynamoDB)

**Workflow**:
```
systems-architect:
  - Design API architecture
  - Define DynamoDB table schema
  - Plan Lambda function structure

infrastructure-specialist:
  1. Create Serverless Framework config:
     - Define Lambda functions (CRUD operations)
     - Configure API Gateway HTTP API
     - Create DynamoDB table
     - Set up IAM roles

  2. Implement:
     - Handler functions in src/functions/
     - DynamoDB client setup
     - Error handling
     - Environment variables

  3. Deploy:
     - serverless deploy --stage dev
     - Test endpoints
     - View CloudWatch logs

security-auditor:
  - Review IAM policies (least privilege)
  - Check API Gateway authorization
  - Verify DynamoDB encryption at rest
  - Validate input validation

git-workflow-manager:
  - Commit serverless configuration
  - Document API endpoints
  - Create deployment guide
```

### Scenario 3: Containerize Application
**Request**: "Dockerize Node.js Express app and deploy to ECS"

**Domain Detection**: Infrastructure (keywords: Docker, ECS, deploy)

**Workflow**:
```
infrastructure-specialist:
  1. Create Dockerfile:
     - Multi-stage build (build + runtime)
     - Use node:18-alpine base image
     - Copy only necessary files
     - Run as non-root user

  2. Create docker-compose.yml (local dev):
     - App container
     - MongoDB container
     - Network configuration

  3. Test locally:
     - docker-compose up
     - Verify app functionality
     - Test hot-reload

  4. Create ECR repository:
     - aws ecr create-repository --repository-name myapp

  5. Push to ECR:
     - Build and tag image
     - docker push to ECR

  6. Create ECS infrastructure (CDK):
     - VPC and subnets
     - ECS cluster (Fargate)
     - Task definition
     - Fargate service with ALB
     - Auto-scaling policies

  7. Deploy:
     - cdk deploy
     - Verify service running
     - Test through ALB

security-auditor:
  - Scan Docker image: docker scan
  - Review Dockerfile best practices
  - Check ECS task IAM role
  - Verify network isolation (security groups)
  - Check container secrets management

dependency-scanner:
  - Audit npm dependencies
  - Check base image vulnerabilities
```

### Scenario 4: CI/CD Pipeline Setup
**Request**: "Set up GitHub Actions to deploy on push to main"

**Domain Detection**: Infrastructure (keywords: CI/CD, GitHub Actions, deploy)

**Workflow**:
```
infrastructure-specialist:
  1. Create .github/workflows/deploy.yml:
     - Trigger on push to main
     - Checkout code
     - Setup Node.js
     - Install dependencies
     - Run tests
     - Build application
     - Deploy to AWS (CDK/Serverless)

  2. Configure secrets:
     - AWS_ACCESS_KEY_ID
     - AWS_SECRET_ACCESS_KEY
     - Add to GitHub repository secrets

  3. Add environment protection:
     - Require approval for production
     - Set environment variables

  4. Test pipeline:
     - Push to feature branch
     - Verify build succeeds
     - Merge to main
     - Verify deployment

security-auditor:
  - Review GitHub Actions permissions
  - Verify secrets are not logged
  - Check AWS IAM user has minimal permissions
  - Recommend using OIDC instead of access keys

git-workflow-manager:
  - Document pipeline workflow
  - Add pipeline status badge to README
```

## Anti-Patterns to Avoid

### Infrastructure Anti-Patterns
1. **ClickOps**: Manual changes in AWS console (use IaC)
2. **Snowflake Servers**: Unique, non-reproducible servers
3. **Shared IAM Credentials**: Use roles and temporary credentials
4. **No Disaster Recovery**: Always have backup/restore strategy
5. **Missing Monitoring**: Deploy without observability
6. **Hardcoded Secrets**: Use Secrets Manager
7. **No Tagging**: Resources without proper tags
8. **Over-Provisioning**: Paying for unused resources

### Deployment Anti-Patterns
- **Big Bang Deployments**: Deploy all changes at once
- **No Rollback Plan**: Can't revert bad deployments
- **Manual Deployments**: Human error-prone
- **Deploying on Fridays**: Risk over weekend
- **No Testing in Staging**: Deploy directly to production

### Container Anti-Patterns
- **Large Images**: Multi-GB images slow to deploy
- **Root User**: Security risk
- **Latest Tag**: Non-deterministic builds
- **Secrets in Dockerfile**: Exposed in image layers
- **No Health Checks**: Container appears healthy but isn't

## Success Metrics

### Deployment Metrics
- Deployment frequency: Daily or more
- Lead time: < 1 hour from commit to production
- Change failure rate: < 15%
- Mean time to recovery (MTTR): < 1 hour

### Infrastructure Metrics
- Infrastructure provision time: < 15 minutes
- CDK synth time: < 2 minutes
- Uptime: > 99.9%
- Cost variance: < 10% month-over-month

### Security Metrics
- Zero production secrets in code
- All resources encrypted at rest
- 100% IAM least-privilege policies
- Zero critical vulnerabilities in production

## Resources & References

### Documentation
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [Serverless Framework Docs](https://www.serverless.com/framework/docs)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### Best Practices
- [12-Factor App](https://12factor.net/)
- [AWS CDK Best Practices](https://docs.aws.amazon.com/cdk/latest/guide/best-practices.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Infrastructure as Code Patterns](https://www.thoughtworks.com/insights/blog/infrastructure-code-reason-smile)

### Tools
- [CDK Patterns](https://cdkpatterns.com/)
- [AWS Solutions Constructs](https://aws.amazon.com/solutions/constructs/)
- [Terraform AWS Modules](https://registry.terraform.io/namespaces/terraform-aws-modules)
