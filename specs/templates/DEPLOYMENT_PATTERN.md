# Deployment Pattern: Next.js + Docker + CloudFront

## Overview

This template defines the standard deployment pattern for Next.js applications in this project. All applications MUST follow this pattern to ensure consistency, maintainability, and proper integration.

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                         CloudFront                          │
│              (Single Domain Distribution)                    │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
             │ /                              │ /api/*
             │ /assets/*                      │ (API Routes)
             │ (Static Files)                 │
             ▼                                ▼
    ┌─────────────────┐              ┌──────────────────────┐
    │   S3 Bucket     │              │  Docker Container    │
    │                 │              │                      │
    │  Static Assets  │              │   Next.js App        │
    │  - HTML         │              │   - Frontend Pages   │
    │  - CSS          │              │   - API Routes       │
    │  - JS Bundles   │              │   - Server-Side      │
    │  - Images       │              │     Rendering        │
    └─────────────────┘              └──────────────────────┘
```

## Key Principles

### 1. Single Container Deployment
**CRITICAL**: Next.js frontend and API routes MUST stay together in ONE Docker container.

**Why?**
- Next.js is designed as a unified framework
- API routes share context with frontend
- Splitting creates complexity without benefit
- Server-side rendering requires frontend/backend integration

**Violation Example (DO NOT DO THIS):**
```yaml
# ❌ WRONG - Separating Next.js frontend and backend
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]

  backend:
    build: ./backend
    ports: ["3001:3001"]
```

**Correct Implementation:**
```yaml
# ✅ CORRECT - Unified Next.js container
services:
  nextjs-app:
    build: ./code-dirs/frontend
    ports: ["3000:3000"]
    environment:
      - NODE_ENV=production
```

### 2. CloudFront as Integration Layer
CloudFront distributes traffic based on path patterns:
- Static assets served from S3 (fast, cheap)
- Dynamic content and API routes served from Docker container
- Single domain for all traffic (no CORS issues)

### 3. CDK Infrastructure as Code
All infrastructure MUST be defined using AWS CDK constructs.

---

## CDK Construct Pattern

### Directory Structure

```
code-dirs/
├── frontend/              # Next.js application
│   ├── pages/             # Next.js pages
│   │   ├── index.tsx      # Homepage
│   │   └── api/           # API routes
│   ├── public/            # Static assets
│   ├── Dockerfile         # Multi-stage build
│   └── package.json
│
└── infrastructure/        # CDK deployment code
    ├── lib/
    │   ├── stacks/
    │   │   └── nextjs-stack.ts       # Main stack
    │   ├── constructs/
    │   │   ├── nextjs-container.ts   # Docker container construct
    │   │   ├── static-site.ts        # S3 + CloudFront for static
    │   │   └── cdn.ts                # CloudFront distribution
    │   └── config/
    │       └── deployment-config.ts  # Environment configuration
    ├── bin/
    │   └── app.ts                    # CDK app entry point
    ├── cdk.json
    └── package.json
```

### CDK Stack Example (TypeScript)

```typescript
// infrastructure/lib/stacks/nextjs-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import { Construct } from 'constructs';

export class NextJsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 1. S3 Bucket for Static Assets
    const staticAssetsBucket = new s3.Bucket(this, 'StaticAssetsBucket', {
      bucketName: `${id.toLowerCase()}-static-assets`,
      publicReadAccess: false,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      encryption: s3.BucketEncryption.S3_MANAGED,
    });

    // 2. Docker Container (Fargate Service)
    const cluster = new ecs.Cluster(this, 'NextJsCluster', {
      clusterName: `${id}-cluster`,
      containerInsights: true,
    });

    const fargateService = new ecsPatterns.ApplicationLoadBalancedFargateService(
      this,
      'NextJsFargateService',
      {
        cluster,
        serviceName: `${id}-nextjs-service`,
        cpu: 512,
        memoryLimitMiB: 1024,
        desiredCount: 2, // High availability
        taskImageOptions: {
          image: ecs.ContainerImage.fromAsset('../frontend'), // Builds Dockerfile
          containerPort: 3000,
          environment: {
            NODE_ENV: 'production',
            STATIC_ASSET_URL: staticAssetsBucket.bucketWebsiteUrl,
          },
        },
        publicLoadBalancer: true,
      }
    );

    // 3. CloudFront Distribution (Integration Layer)
    const distribution = new cloudfront.Distribution(this, 'Distribution', {
      comment: `${id} - Next.js Application`,
      defaultBehavior: {
        // Default: Route to Docker container for dynamic content
        origin: new origins.LoadBalancerV2Origin(fargateService.loadBalancer, {
          protocolPolicy: cloudfront.OriginProtocolPolicy.HTTP_ONLY,
        }),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
        cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED, // Dynamic content
      },
      additionalBehaviors: {
        // Static assets: Route to S3
        '/_next/static/*': {
          origin: new origins.S3Origin(staticAssetsBucket),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
        '/static/*': {
          origin: new origins.S3Origin(staticAssetsBucket),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
        '/assets/*': {
          origin: new origins.S3Origin(staticAssetsBucket),
          viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
      },
      priceClass: cloudfront.PriceClass.PRICE_CLASS_100, // US, Canada, Europe
    });

    // Outputs
    new cdk.CfnOutput(this, 'CloudFrontURL', {
      value: distribution.distributionDomainName,
      description: 'CloudFront distribution URL',
    });

    new cdk.CfnOutput(this, 'StaticAssetsBucketName', {
      value: staticAssetsBucket.bucketName,
      description: 'S3 bucket for static assets',
    });
  }
}
```

---

## Docker Configuration

### Multi-Stage Dockerfile

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --production=false

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build Next.js application
RUN yarn build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### next.config.js Configuration

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',

  // Asset prefix for CloudFront (if using custom domain)
  assetPrefix: process.env.ASSET_PREFIX || '',

  // Compress responses
  compress: true,

  // Production optimizations
  swcMinify: true,

  // Image optimization configuration
  images: {
    domains: ['your-cloudfront-domain.cloudfront.net'],
  },
};

module.exports = nextConfig;
```

---

## Deployment Workflow

### 1. Build Phase

```bash
# Navigate to infrastructure directory
cd code-dirs/infrastructure

# Install dependencies
yarn install

# Synthesize CloudFormation template (verify before deploy)
npx cdk synth

# Check for changes
npx cdk diff
```

### 2. Deploy Phase

```bash
# Deploy to AWS
npx cdk deploy

# For production with approval gate
npx cdk deploy --require-approval broadening
```

### 3. Post-Deployment

```bash
# Get CloudFront URL from outputs
CLOUDFRONT_URL=$(aws cloudformation describe-stacks \
  --stack-name NextJsStack \
  --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" \
  --output text)

echo "Application deployed at: https://$CLOUDFRONT_URL"

# Health check
curl -I https://$CLOUDFRONT_URL/api/health
```

---

## Environment Configuration

### Development (.env.local)

```bash
# Local development environment
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:3000/api
DATABASE_URL=postgresql://localhost:5432/dev_db
```

### Production (AWS Systems Manager Parameter Store)

```bash
# Store secrets in Parameter Store
aws ssm put-parameter \
  --name "/nextjs-app/prod/database-url" \
  --value "postgresql://prod-host/prod_db" \
  --type "SecureString"

aws ssm put-parameter \
  --name "/nextjs-app/prod/api-key" \
  --value "your-api-key" \
  --type "SecureString"
```

### CDK Environment Variable Injection

```typescript
// In CDK stack
import * as ssm from 'aws-cdk-lib/aws-ssm';

const databaseUrl = ssm.StringParameter.fromSecureStringParameterAttributes(
  this,
  'DatabaseUrl',
  {
    parameterName: '/nextjs-app/prod/database-url',
  }
);

// Add to container environment
taskImageOptions: {
  environment: {
    NODE_ENV: 'production',
    DATABASE_URL: databaseUrl.stringValue,
  },
}
```

---

## Monitoring and Observability

### CloudWatch Logs

```typescript
// Enable container logging
import * as logs from 'aws-cdk-lib/aws-logs';

const logGroup = new logs.LogGroup(this, 'NextJsLogGroup', {
  logGroupName: `/ecs/${id}-nextjs`,
  retention: logs.RetentionDays.ONE_MONTH,
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});

// Add to Fargate service
taskImageOptions: {
  logDriver: ecs.LogDrivers.awsLogs({
    streamPrefix: 'nextjs',
    logGroup: logGroup,
  }),
}
```

### CloudWatch Alarms

```typescript
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';

// High 5xx error rate alarm
const errorAlarm = new cloudwatch.Alarm(this, 'HighErrorRate', {
  metric: fargateService.loadBalancer.metrics.httpCodeTarget(
    cloudwatch.HttpCodeTarget.TARGET_5XX_COUNT
  ),
  threshold: 10,
  evaluationPeriods: 2,
  alarmDescription: 'Alert on high 5xx error rate',
});
```

---

## Cost Optimization

### 1. Static Asset Caching
- Serve static assets from S3 via CloudFront
- Reduces compute costs (no container CPU for static files)
- CloudFront caching reduces S3 requests

### 2. Container Right-Sizing
- Start with minimal CPU/memory (512 CPU, 1024 MB)
- Monitor and scale based on actual usage
- Use Fargate Spot for non-critical environments

### 3. CloudFront Price Class
- Use PRICE_CLASS_100 (US, Canada, Europe) unless global reach required
- Reduces CloudFront distribution costs

---

## Security Best Practices

### 1. Container Security
- Use official Node.js Alpine images (smaller attack surface)
- Run as non-root user
- Scan images for vulnerabilities (AWS ECR scanning)

### 2. Network Security
- Use VPC for container networking
- Security groups restrict access
- CloudFront provides DDoS protection

### 3. Secrets Management
- NEVER commit secrets to code
- Use AWS Systems Manager Parameter Store or Secrets Manager
- Inject secrets as environment variables at runtime

---

## Validation Checklist

Before deploying, verify:

- [ ] Next.js app builds successfully locally (`yarn build`)
- [ ] Dockerfile builds without errors
- [ ] All environment variables defined in Parameter Store
- [ ] CDK synth produces valid CloudFormation template
- [ ] Static assets configured for S3 upload
- [ ] CloudFront behaviors route correctly (test locally)
- [ ] Health check endpoint exists (`/api/health`)
- [ ] Logging configured for troubleshooting
- [ ] Alarms configured for critical metrics
- [ ] No secrets in code or Docker image

---

## Troubleshooting

### Container won't start
1. Check CloudWatch Logs for error messages
2. Verify environment variables are set correctly
3. Test Docker image locally: `docker build -t test . && docker run -p 3000:3000 test`

### Static assets not loading
1. Verify S3 bucket permissions
2. Check CloudFront behavior path patterns
3. Confirm asset prefix in `next.config.js`

### API routes returning 502
1. Check container health status in ECS console
2. Verify load balancer target group health checks
3. Review application logs for errors

---

## References

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/latest/guide/)
- [Next.js Deployment Docs](https://nextjs.org/docs/deployment)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [CloudFront Best Practices](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/best-practices.html)
