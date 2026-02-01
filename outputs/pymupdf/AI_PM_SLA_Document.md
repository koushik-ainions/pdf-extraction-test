**Service Level Agreement (SLA)** AI Program Manager (Peeku.Nion)

Version: 1.0

Effective Date: March 1, 2025

Review Period: Quarterly

**1. Service Overview**

This SLA defines the performance standards, availability commitments, and penalty structures for the AI Program Manager (Peeku.Nion) service provided by aiNions.

**1.1 Service Scope**

- AI-powered program management orchestration

- Multi-project coordination and tracking

- Enterprise integration management (Jira, MS Teams, Outlook, Confluence)

- Real-time status monitoring and reporting

- Risk identification and mitigation recommendations

**2. Service Level Objectives (SLOs)**

**2.1 System Availability**

|Metric|Threshold|Measurement Period|

|---|---|---|
|System Uptime|≥ 99.5%|Monthly|

|Scheduled Maintenance Window|≤ 4 hours/month|Monthly|
|Unplanned Downtime|≤ 3.6 hours/month|Monthly|

**Exclusions:**

- Scheduled maintenance (with 72-hour advance notice)

- Force majeure events

- Customer infrastructure failures

- Third-party service outages (Jira, MS365, etc.)

**2.2 Response Time Performance**

|Service Component|Target Response Time|Threshold|

|---|---|---|
|User Query Response|≤ 3 seconds|95th percentile|

|Project Status Update|≤ 5 seconds|95th percentile|

|Complex Analysis Request|≤ 15 seconds|95th percentile|

|---|---|---|
|Report Generation|≤ 30 seconds|90th percentile|

|Integration Sync|≤ 60 seconds|95th percentile|

**2.3 Accuracy & Quality Metrics**

|Metric|Threshold|Measurement|

|---|---|---|
|Task Status Accuracy|≥ 98%|Weekly validation|

|Risk Detection Accuracy|≥ 90%|Monthly audit|
|Dependency Mapping Accuracy|≥ 95%|Monthly validation|

|Action Item Assignment Accuracy|≥ 97%|Weekly review|
|Meeting Summary Accuracy|≥ 95%|Per-meeting validation|

**3. Support Response Standards**

**3.1 Issue Severity Levels**

|Severity|Definition|Initial Response|Resolution Target|

|---|---|---|---|
|Critical (P0)|Complete service outage|15 minutes|4 hours|

|High (P1)|Major feature unavailable|1 hour|8 hours|
|Medium (P2)|Degraded performance|4 hours|24 hours|

|Low (P3)|Minor issues, feature requests|8 hours|72 hours|

**4. Service Credits & Penalties**

**4.1 Uptime-Based Service Credits**

Monthly uptime is calculated as: _((Total Minutes in Month - Downtime Minutes) / Total Minutes in Month) × 100_

|Monthly Uptime %|Service Credit|

|---|---|
|99.5% - 99.99%|0% (SLA met)|

|99.0% - 99.49%|10% of monthly fees|
|98.0% - 98.99%|25% of monthly fees|

|95.0% - 97.99%|50% of monthly fees|
|< 95.0%|100% of monthly fees + termination option|

**4.2 Performance-Based Credits**

|Metric Breach|Service Credit|

|---|---|
|Response Time SLA miss (>5% of requests)|5% of monthly fees|

|Integration sync failures (>2% failure rate)|10% of monthly fees|
|Accuracy metrics below threshold (>1 week)|15% of monthly fees|

|Multiple SLA breaches (3+ in one month)|25% of monthly fees|

**4.3 Support Response Credits**

|Severity|Breach|Credit per Incident|

|---|---|---|
|P0 Critical|Response > 15 min OR Resolution > 4 hrs|5% of monthly fees|

|P1 High|Response > 1 hr OR Resolution > 8 hrs|3% of monthly fees|
|P2 Medium|Resolution > 24 hrs|1% of monthly fees|

**Maximum Monthly Credit:** 50% of monthly subscription fees

**5. Credit Claim Process**

**5.1 Eligibility Requirements**

- Customer account must be in good standing

- Claim must be submitted within 30 days of incident

- Customer must provide detailed incident documentation

- Credits only apply to verified SLA breaches

**5.2 Claim Submission**

1. Submit claim via support portal or dedicated email

2. Include: incident date/time, affected services, impact duration

3. aiNions will investigate within 5 business days

4. Approved credits applied to next billing cycle

**5.3 Exclusions from Credits**

- Downtime during scheduled maintenance windows

- Issues caused by customer's network or infrastructure

- Third-party service outages beyond aiNions' control

- Beta or preview features

- Non-production environments

**6. Security & Compliance SLAs**

**6.1 Security Incident Response**

|Incident Type|Detection Time|Notification Time|Resolution Target|

|---|---|---|---|
|Critical Security Breach|≤ 15 minutes|≤ 1 hour|≤ 24 hours|

|Data Exposure Risk|≤ 30 minutes|≤ 2 hours|≤ 48 hours|
|Suspicious Activity|≤ 1 hour|≤ 4 hours|≤ 72 hours|

**6.2 Compliance Commitments**

|Requirement|Standard|

|---|---|
|Data Encryption (at rest)|AES-256|

|Data Encryption (in transit)|TLS 1.3|
|Backup Frequency|Every 6 hours|

|Backup Retention|30 days|
|Disaster Recovery RTO|≤ 4 hours|

|Disaster Recovery RPO|≤ 15 minutes|
|Security Audit Frequency|Quarterly|

**7. Monitoring & Reporting**

**7.1 Real-Time Monitoring**

- System health dashboard (99.9% availability)

- Performance metrics updated every 60 seconds

- Automated alerting for threshold breaches

**7.2 Monthly SLA Reports**

Provided by the 5th business day of each month:

- Uptime percentage and downtime incidents

- Response time metrics (p50, p95, p99)

- Integration sync success rates

- Accuracy metrics validation results

- Support ticket statistics

- Service credits issued

**8. Termination Rights**

**8.1 Customer Termination Rights**

Customer may terminate without penalty if:

- Monthly uptime falls below 95% for 2 consecutive months

- Critical (P0) SLA breached 3+ times in 90 days

- aiNions fails to remediate repeated SLA violations

**8.2 Notice Period**

- Standard tier: 30 days written notice

- Enterprise tier: 60 days written notice

**9. Contact Information**

**SLA Inquiries & Claims:** Email: sla-claims@ainions.com Support Portal: https://support.ainions.com

**Escalation Contact:** Email: escalations@ainions.com Phone: [Enterprise customers only]

**Service Status:** https://status.ainions.com

**10. Acceptance**

By using the AI Program Manager (Peeku.Nion) service, Customer acknowledges and agrees to the terms of this Service Level Agreement.

Customer Signature: ________________________________________Date: ____________________

aiNions Representative: ________________________________________Date: ____________________

_Document Version: 1.0 Last Updated: February 2025 Next Review: May 2025_

