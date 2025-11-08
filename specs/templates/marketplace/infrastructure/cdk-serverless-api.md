---
template_id: cdk-serverless-api
template_name: CDK Serverless API
category: infrastructure
difficulty: advanced
estimated_time: 6-10 hours
tags: [aws, cdk, lambda, api-gateway, serverless, typescript]
author: claude-oak-agents
version: 1.0.0
last_updated: 2025-11-08
popularity: 87
dependencies: [aws-cdk, aws-sdk]
related_templates: [rest-crud-api, saas-auth-complete]
---

# CDK Serverless API

Production-ready serverless API infrastructure using AWS CDK, Lambda, API Gateway, and DynamoDB with monitoring and CI/CD.

## Overview

This template deploys a complete serverless API stack:
- API Gateway REST API with custom domain
- Lambda functions (Node.js or Python)
- DynamoDB tables with Global Secondary Indexes
- CloudWatch Logs and Metrics
- X-Ray tracing for distributed debugging
- Secrets Manager for sensitive configuration
- CloudFront CDN (optional)
- CI/CD pipeline with GitHub Actions

**Architecture**: API Gateway → Lambda → DynamoDB

## Use Cases

- **Scalable REST APIs**: Auto-scaling backend for web/mobile apps
- **Event-Driven Architectures**: Serverless microservices
- **Cost-Optimized APIs**: Pay-per-request pricing
- **Global APIs**: Multi-region deployment with low latency

## Requirements

### Technical Prerequisites
- AWS Account with appropriate IAM permissions
- AWS CLI configured (`aws configure`)
- Node.js 18+ (for CDK)
- CDK CLI (`npm install -g aws-cdk`)
- Domain name (optional, for custom domain)

### AWS Services Required
- Lambda (compute)
- API Gateway (HTTP endpoint)
- DynamoDB (database)
- CloudWatch (monitoring)
- X-Ray (tracing)
- Secrets Manager (configuration)
- Route53 (DNS, if custom domain)
- ACM (SSL certificate, if custom domain)

## Implementation Plan

### Phase 1: CDK Project Setup (1 hour)

**1.1 Initialize CDK Project**
```bash
mkdir serverless-api && cd serverless-api
cdk init app --language typescript
npm install @aws-cdk/aws-lambda @aws-cdk/aws-apigateway @aws-cdk/aws-dynamodb
```

**1.2 Project Structure**
```
serverless-api/
├── lib/
│   ├── api-stack.ts           # Main API Gateway + Lambda stack
│   ├── database-stack.ts      # DynamoDB tables
│   └── monitoring-stack.ts    # CloudWatch dashboards and alarms
├── lambda/
│   ├── handlers/
│   │   ├── getUser.ts
│   │   ├── createUser.ts
│   │   └── listUsers.ts
│   └── shared/
│       ├── db.ts              # DynamoDB client
│       └── utils.ts
├── bin/
│   └── app.ts                 # CDK entry point
├── test/
│   └── api-stack.test.ts
└── cdk.json
```

### Phase 2: DynamoDB Stack (1 hour)

**2.1 DynamoDB Table Definition**
```typescript
// lib/database-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

export class DatabaseStack extends cdk.Stack {
  public readonly usersTable: dynamodb.Table;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Users table with GSI for email lookups
    this.usersTable = new dynamodb.Table(this, 'UsersTable', {
      partitionKey: { name: 'userId', type: dynamodb.AttributeType.STRING },
      sortKey: { name: 'createdAt', type: dynamodb.AttributeType.NUMBER },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      encryption: dynamodb.TableEncryption.AWS_MANAGED,
      pointInTimeRecovery: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,

      stream: dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
    });

    // GSI for email-based queries
    this.usersTable.addGlobalSecondaryIndex({
      indexName: 'EmailIndex',
      partitionKey: { name: 'email', type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
    });

    // Outputs
    new cdk.CfnOutput(this, 'UsersTableName', {
      value: this.usersTable.tableName,
    });
  }
}
```

### Phase 3: Lambda Functions (2 hours)

**3.1 Lambda Handler Example**
```typescript
// lambda/handlers/getUser.ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

export async function handler(event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  try {
    const userId = event.pathParameters?.id;

    if (!userId) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Missing userId' }),
      };
    }

    const result = await docClient.send(new GetCommand({
      TableName: process.env.USERS_TABLE_NAME!,
      Key: { userId },
    }));

    if (!result.Item) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'User not found' }),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify(result.Item),
    };
  } catch (error) {
    console.error('Error fetching user:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
}
```

**3.2 Shared Database Client**
```typescript
// lambda/shared/db.ts
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';

export const dynamoDbClient = DynamoDBDocumentClient.from(
  new DynamoDBClient({
    region: process.env.AWS_REGION,
  })
);

export const USERS_TABLE = process.env.USERS_TABLE_NAME!;
```

### Phase 4: API Gateway Stack (2 hours)

**4.1 API Gateway + Lambda Integration**
```typescript
// lib/api-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

interface ApiStackProps extends cdk.StackProps {
  usersTable: dynamodb.Table;
}

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    // Lambda function for getting user
    const getUserFn = new lambda.Function(this, 'GetUserFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'getUser.handler',
      code: lambda.Code.fromAsset('lambda/dist'),
      environment: {
        USERS_TABLE_NAME: props.usersTable.tableName,
      },
      tracing: lambda.Tracing.ACTIVE,
      timeout: cdk.Duration.seconds(10),
      memorySize: 256,
    });

    // Grant DynamoDB read permissions
    props.usersTable.grantReadData(getUserFn);

    // API Gateway REST API
    const api = new apigateway.RestApi(this, 'ServerlessApi', {
      restApiName: 'Serverless API',
      description: 'API Gateway for serverless backend',
      deployOptions: {
        stageName: 'prod',
        tracingEnabled: true,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
        metricsEnabled: true,
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    // /users resource
    const users = api.root.addResource('users');

    // GET /users/{id}
    const user = users.addResource('{id}');
    user.addMethod('GET', new apigateway.LambdaIntegration(getUserFn));

    // Lambda function for listing users
    const listUsersFn = new lambda.Function(this, 'ListUsersFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'listUsers.handler',
      code: lambda.Code.fromAsset('lambda/dist'),
      environment: {
        USERS_TABLE_NAME: props.usersTable.tableName,
      },
      tracing: lambda.Tracing.ACTIVE,
    });

    props.usersTable.grantReadData(listUsersFn);

    // GET /users
    users.addMethod('GET', new apigateway.LambdaIntegration(listUsersFn));

    // Lambda function for creating user
    const createUserFn = new lambda.Function(this, 'CreateUserFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'createUser.handler',
      code: lambda.Code.fromAsset('lambda/dist'),
      environment: {
        USERS_TABLE_NAME: props.usersTable.tableName,
      },
      tracing: lambda.Tracing.ACTIVE,
    });

    props.usersTable.grantWriteData(createUserFn);

    // POST /users
    users.addMethod('POST', new apigateway.LambdaIntegration(createUserFn));

    // Outputs
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
    });
  }
}
```

### Phase 5: Monitoring Stack (1 hour)

**5.1 CloudWatch Dashboard**
```typescript
// lib/monitoring-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

interface MonitoringStackProps extends cdk.StackProps {
  api: apigateway.RestApi;
  functions: lambda.Function[];
}

export class MonitoringStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MonitoringStackProps) {
    super(scope, id, props);

    // Dashboard
    const dashboard = new cloudwatch.Dashboard(this, 'ApiDashboard', {
      dashboardName: 'ServerlessApiDashboard',
    });

    // API Gateway metrics
    dashboard.addWidgets(
      new cloudwatch.GraphWidget({
        title: 'API Requests',
        left: [props.api.metricCount()],
      }),
      new cloudwatch.GraphWidget({
        title: 'API Latency',
        left: [props.api.metricLatency()],
      })
    );

    // Lambda metrics
    props.functions.forEach((fn) => {
      dashboard.addWidgets(
        new cloudwatch.GraphWidget({
          title: `${fn.functionName} Invocations`,
          left: [fn.metricInvocations()],
        }),
        new cloudwatch.GraphWidget({
          title: `${fn.functionName} Errors`,
          left: [fn.metricErrors()],
        })
      );
    });

    // Alarms
    const errorAlarm = new cloudwatch.Alarm(this, 'ApiErrorAlarm', {
      metric: props.api.metricServerError(),
      threshold: 10,
      evaluationPeriods: 1,
      alarmDescription: 'Alert when API has 10+ server errors',
    });

    // SNS topic for alerts (optional)
    // const topic = new sns.Topic(this, 'AlertTopic');
    // errorAlarm.addAlarmAction(new cloudwatchActions.SnsAction(topic));
  }
}
```

### Phase 6: Deployment Pipeline (2 hours)

**6.1 GitHub Actions Workflow**
```yaml
# .github/workflows/deploy.yml
name: Deploy CDK Stack

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build Lambda functions
        run: npm run build:lambda

      - name: CDK Synth
        run: npx cdk synth

      - name: CDK Deploy
        if: github.ref == 'refs/heads/main'
        run: npx cdk deploy --all --require-approval never
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-1
```

**6.2 Build Script**
```json
// package.json
{
  "scripts": {
    "build:lambda": "tsc -p lambda/tsconfig.json",
    "synth": "cdk synth",
    "deploy": "cdk deploy --all",
    "test": "jest"
  }
}
```

## Agent Workflow

```yaml
agent_sequence:
  phase_1_design:
    - agent: design-simplicity-advisor
      task: "Review serverless architecture (Lambda vs ECS vs K8s)"
      output: "Recommendation: Lambda for simple APIs, ECS for complex workloads"

    - agent: infrastructure-specialist
      task: "Design CDK stack structure (single vs multi-stack)"
      output: "3 stacks: Database, API, Monitoring"

  phase_2_implementation:
    - agent: infrastructure-specialist
      task: "Implement DynamoDB stack with GSIs"
      duration: "1 hour"

    - agent: backend-architect
      task: "Implement Lambda functions (handlers + shared utilities)"
      duration: "2 hours"

    - agent: infrastructure-specialist
      task: "Implement API Gateway stack with Lambda integrations"
      duration: "2 hours"

  phase_3_observability:
    - agent: infrastructure-specialist
      task: "Implement CloudWatch dashboard and alarms"
      duration: "1 hour"

  phase_4_security:
    - agent: security-auditor
      task: "Security review: IAM permissions, API auth, encryption"
      output: "Security checklist and recommendations"

    - agent: infrastructure-specialist
      task: "Implement security improvements (API keys, WAF, secrets)"
      duration: "1 hour"

  phase_5_deployment:
    - agent: infrastructure-specialist
      task: "Setup GitHub Actions CI/CD pipeline"
      duration: "1 hour"

    - agent: git-workflow-manager
      task: "Create PR with CDK infrastructure"
```

## Testing Strategy

### CDK Unit Tests
```typescript
import { Template } from 'aws-cdk-lib/assertions';
import * as cdk from 'aws-cdk-lib';
import { DatabaseStack } from '../lib/database-stack';

test('DynamoDB table created with correct properties', () => {
  const app = new cdk.App();
  const stack = new DatabaseStack(app, 'TestStack');
  const template = Template.fromStack(stack);

  template.hasResourceProperties('AWS::DynamoDB::Table', {
    BillingMode: 'PAY_PER_REQUEST',
    StreamSpecification: {
      StreamViewType: 'NEW_AND_OLD_IMAGES',
    },
  });
});
```

### Lambda Integration Tests
```typescript
test('GET /users/:id returns user', async () => {
  const response = await fetch(`${API_URL}/users/123`);
  expect(response.status).toBe(200);
  const user = await response.json();
  expect(user.userId).toBe('123');
});
```

### Load Tests
- Use Artillery or k6 for load testing
- Target: 100 req/sec sustained
- Monitor Lambda concurrency limits
- Watch DynamoDB throttling metrics

## Common Pitfalls

### 1. Lambda Cold Starts
**Problem**: First request after idle period is slow (1-3s)
**Solution**: Provisioned concurrency for critical functions, keep functions warm

### 2. DynamoDB Throttling
**Problem**: Exceeding RCU/WCU limits causes errors
**Solution**: Use on-demand billing or auto-scaling capacity

### 3. IAM Permission Errors
**Problem**: Lambda cannot access DynamoDB
**Solution**: Use `table.grantReadData(fn)` instead of manual IAM policies

### 4. CORS Issues
**Problem**: Browser blocks API requests
**Solution**: Configure `defaultCorsPreflightOptions` in API Gateway

### 5. Large Bundle Sizes
**Problem**: Lambda deployment package >50MB
**Solution**: Use Lambda layers for dependencies, exclude dev dependencies

### 6. Missing Environment Variables
**Problem**: Lambda fails because env vars not set
**Solution**: Define all env vars in CDK construct, use Secrets Manager for sensitive data

## Cost Optimization

### Estimated Monthly Costs (100k requests/month)
- Lambda: $0.20 (100k invocations × 256MB × 100ms)
- API Gateway: $0.35 (100k requests)
- DynamoDB: $1.25 (on-demand pricing)
- CloudWatch Logs: $0.50 (1GB logs)
- **Total: ~$2.30/month**

### Cost Reduction Strategies
- Use Lambda Reserved Concurrency for predictable workloads
- DynamoDB on-demand vs provisioned capacity analysis
- CloudWatch Logs retention policy (7 days vs 30 days)
- API Gateway caching for repeated requests

## Success Criteria

- [ ] CDK stacks deploy successfully
- [ ] API Gateway endpoint accessible
- [ ] Lambda functions execute without errors
- [ ] DynamoDB queries work correctly
- [ ] CloudWatch dashboard shows metrics
- [ ] Alarms trigger on errors
- [ ] CI/CD pipeline deploys automatically
- [ ] X-Ray tracing enabled
- [ ] Security review passes
- [ ] Load test handles 100 req/sec

## Production Checklist

- [ ] Custom domain configured (Route53 + ACM)
- [ ] API Gateway usage plan and API keys
- [ ] WAF rules (rate limiting, geo-blocking)
- [ ] VPC integration (if accessing private resources)
- [ ] Secrets Manager for sensitive configuration
- [ ] DynamoDB Point-in-Time Recovery enabled
- [ ] Lambda Reserved Concurrency set
- [ ] CloudWatch alarms configured
- [ ] SNS topic for alerts
- [ ] Backup and disaster recovery plan

## Future Enhancements

- Multi-region deployment (Route53 failover)
- API Gateway authorizer (JWT validation)
- DynamoDB Global Tables (multi-region)
- EventBridge integration (async processing)
- Step Functions (complex workflows)
- AppSync GraphQL alternative
