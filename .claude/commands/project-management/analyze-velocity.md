# Analyze Team Velocity

Analyze historical telemetry data to calculate team velocity, identify trends, and generate predictive estimates.

## Usage
/analyze-velocity [--time-range 7d|30d|90d|all] [--by-agent] [--by-task-type]

## What This Does
1. Queries telemetry database for historical workflow data
2. Calculates team velocity metrics (tasks completed, time per task)
3. Analyzes trends over time (improving, stable, declining)
4. Identifies bottlenecks and blockers
5. Generates predictive estimates for future work
6. Provides actionable recommendations

## Example
/analyze-velocity --time-range 90d --by-agent

## Agent Coordination
1. **Main LLM**: Queries and analyzes telemetry data
   - Reads invocations.jsonl for all workflows
   - Aggregates metrics by time period
   - Calculates velocity trends
   - Identifies patterns and anomalies
2. **project-manager**: Interprets data and provides recommendations
   - Analyzes bottlenecks
   - Suggests process improvements
   - Forecasts future capacity

## Output
Velocity Analysis Report:
```markdown
## Team Velocity Analysis

### Time Range: Last 90 Days (Oct 1 - Nov 8, 2025)

### Summary Metrics

**Overall Velocity**:
- Workflows completed: 47
- Average workflow duration: 14.2 minutes
- Total development time: 11.1 hours
- Success rate: 91.5% (43 successful, 4 failed)

**Trends**:
- Velocity improving: +15% vs previous 90 days
- Average workflow time: -8% (faster)
- Success rate: +3% (more reliable)

### Velocity by Time Period

```
Period          | Workflows | Avg Duration | Success Rate
----------------|-----------|--------------|-------------
Week 1 (Oct 1)  |     3     |   18.5 min  |    67%
Week 2 (Oct 8)  |     5     |   16.2 min  |    80%
Week 3 (Oct 15) |     6     |   15.1 min  |    83%
Week 4 (Oct 22) |     7     |   14.8 min  |    86%
Week 5 (Oct 29) |     8     |   13.2 min  |    88%
Week 6 (Nov 5)  |     6     |   12.1 min  |   100%

Trend: ↗ Velocity increasing, duration decreasing, quality improving
```

**Insights**:
- Team is getting faster and more reliable over time
- Week 6 achieved 100% success rate (best performance)
- Average workflow time reduced 35% from Week 1 to Week 6

### Velocity by Agent

**Agent Performance** (ranked by usage):

```
Agent                     | Invocations | Avg Duration | Success Rate
--------------------------|-------------|--------------|-------------
backend-architect         |     47      |   7.8 min   |    96%
design-simplicity-advisor |     45      |   0.7 min   |   100%
security-auditor          |     43      |   1.3 min   |   100%
unit-test-expert          |     41      |   3.2 min   |    93%
quality-gate              |     40      |   2.1 min   |    95%
git-workflow-manager      |     38      |   0.4 min   |   100%
frontend-developer        |     22      |   5.4 min   |    91%
qa-specialist             |     18      |   2.8 min   |    89%
infrastructure-specialist |     12      |  11.2 min   |    92%
project-manager           |      8      |   1.5 min   |   100%
```

**Top Performers**:
1. **design-simplicity-advisor**: 100% success, fastest execution
2. **security-auditor**: 100% success, consistent performance
3. **git-workflow-manager**: 100% success, reliable automation

**Bottlenecks**:
1. **infrastructure-specialist**: Longest duration (11.2 min avg)
2. **backend-architect**: High usage but consumes 55% of workflow time
3. **unit-test-expert**: 7% failure rate, needs improvement

### Velocity by Task Type

**Task Categories** (based on workflow classification):

```
Task Type       | Count | Avg Duration | Success Rate | % of Total
----------------|-------|--------------|--------------|------------
Implementation  |   28  |   15.8 min  |     89%      |    60%
Analysis        |   12  |    8.2 min  |    100%      |    26%
Coordination    |    5  |   22.1 min  |     80%      |    11%
Information     |    2  |    2.1 min  |    100%      |     4%
```

**Insights**:
- Implementation tasks dominate (60% of workload)
- Coordination tasks are slowest and least reliable
- Analysis tasks have perfect success rate
- Information tasks are quick and reliable

### Trends Over Time

**Velocity Trend** (workflows per week):
```
Week 1: ███ (3)
Week 2: █████ (5)
Week 3: ██████ (6)
Week 4: ███████ (7)
Week 5: ████████ (8)
Week 6: ██████ (6)

Trend: Generally increasing, slight dip in Week 6 (expected variance)
```

**Duration Trend** (minutes per workflow):
```
Week 1: ████████████████████ (18.5 min)
Week 2: ████████████████ (16.2 min)
Week 3: ███████████████ (15.1 min)
Week 4: ██████████████ (14.8 min)
Week 5: █████████████ (13.2 min)
Week 6: ████████████ (12.1 min)

Trend: Consistently decreasing (35% improvement)
```

**Success Rate Trend**:
```
Week 1: 67%  ████████████████████████
Week 2: 80%  ████████████████████████████
Week 3: 83%  █████████████████████████████
Week 4: 86%  ██████████████████████████████
Week 5: 88%  ███████████████████████████████
Week 6: 100% ███████████████████████████████████

Trend: Improving quality and reliability
```

### Bottleneck Analysis

**Top 3 Bottlenecks**:

1. **Infrastructure Deployment Tasks** (11.2 min average)
   - Root cause: CDK synthesis and deployment takes time
   - Impact: Blocks 25% of workflows
   - Recommendation: Parallelize CDK operations, use cached builds

2. **Backend Implementation** (7.8 min average)
   - Root cause: Complex logic requires careful implementation
   - Impact: Consumes 55% of workflow time
   - Recommendation: Create reusable patterns, improve templates

3. **Unit Test Creation** (3.2 min + 7% failure rate)
   - Root cause: Test failures require debugging and fixes
   - Impact: Delays workflow completion
   - Recommendation: Improve test templates, better error messages

### Predictive Analysis

**Forecasted Velocity** (next 30 days):
- Expected workflows: 24-28 (based on trend)
- Average duration: 11-12 minutes (improving)
- Success rate: 92-95% (continuing improvement)
- Total capacity: 4.5-5.5 hours of work

**Capacity Planning**:
- Current throughput: ~7 workflows/week
- With 35% improvement trend: ~9 workflows/week achievable
- Bottleneck mitigation could add: +2 workflows/week
- Realistic target: 8-9 workflows/week

**Confidence Intervals**:
- Workflows/week: 7 ± 2 (80% confidence)
- Duration/workflow: 12 ± 3 minutes (80% confidence)
- Success rate: 92% ± 5% (80% confidence)

### Recommendations

**Immediate Actions** (High Impact):
1. **Optimize infrastructure-specialist**: Cache CDK builds, parallelize operations
   - Expected gain: 5 minutes per infrastructure workflow
   - Impact: 15% overall velocity improvement

2. **Improve unit-test-expert reliability**: Better templates, clearer error messages
   - Expected gain: Reduce failure rate from 7% to 3%
   - Impact: 4% workflow success rate improvement

3. **Create backend-architect patterns library**: Reusable code patterns for common tasks
   - Expected gain: 2-3 minutes per backend workflow
   - Impact: 12% overall velocity improvement

**Short-term Improvements** (Medium Impact):
4. Document successful workflows for knowledge sharing
5. Create automation for repetitive tasks
6. Implement workflow templates for common scenarios

**Long-term Strategic** (High Value):
7. Invest in agent training and optimization
8. Build telemetry-driven workflow recommendations
9. Implement predictive workflow scheduling

### Historical Comparison

**Previous 90 Days vs Current 90 Days**:
```
Metric                 | Previous | Current | Change
-----------------------|----------|---------|--------
Workflows completed    |    41    |   47    | +15%
Avg workflow duration  |   15.4   |  14.2   |  -8%
Success rate           |   88.5%  |  91.5%  | +3%
Velocity (workflows/wk)|    6.2   |   7.1   | +15%
```

**Year-over-year trend**: Significant improvement in all metrics

### Key Insights

1. **Velocity is improving**: Team is 15% more productive than previous period
2. **Quality is increasing**: Success rate improved from 88.5% to 91.5%
3. **Efficiency gains**: Workflows complete 8% faster on average
4. **Bottlenecks identified**: Infrastructure and backend tasks need optimization
5. **Predictable performance**: Velocity trends are consistent and predictable

### Next Review

Recommended: Run velocity analysis weekly or monthly to track progress on recommendations.

**Schedule next analysis**: /analyze-velocity --time-range 30d (in 30 days)
```

This provides data-driven insights into team performance with actionable recommendations.
## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
