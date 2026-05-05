# CMSC471 Final Project Report
**Student:** Alpha Bah  
**Course:** CMSC471  
**Project:** Yellow Sign Diner — Serverless AWS Shopping List Application

---

## 1. Architecture Overview

The Yellow Sign Diner application is a fully serverless web application built on AWS. The system allows users to upload handwritten shopping list photos, process them using AWS Textract OCR, and store the extracted items in DynamoDB. The application is composed of 14 AWS resources orchestrated through AWS SAM and CloudFormation.

The user interacts with the system through a browser-based dashboard served via API Gateway and a Static Proxy Lambda function. The dashboard is an HTML/JavaScript single-page application stored in an S3 bucket. When a user uploads an image, it is stored in a separate Inbox S3 bucket. The user then selects the image and clicks the PROCESS button, which triggers a Step Functions state machine through the LSubmit Lambda. The state machine orchestrates three Lambda functions: L1Fetch retrieves the image from S3, L2Call sends it to AWS Textract for text extraction, and L3Save stores the extracted items in the RecordsTable DynamoDB table. The LPoll Lambda allows the frontend to check the job status by querying the JobsTable DynamoDB table. The LRecords Lambda provides GET and DELETE endpoints for managing the extracted shopping list items.

---

## 2. Security and Compliance

### IAM Least Privilege
In the current implementation, all Lambda functions use the LabRole IAM role provided by AWS Academy Learner Lab. In a production environment, each Lambda function should have its own IAM role with only the permissions it needs. For example, the LInbox Lambda should only have s3:GetObject, s3:PutObject, and s3:DeleteObject permissions on the Inbox bucket. The LSubmit Lambda should only have dynamodb:PutItem on the JobsTable and states:StartExecution on the State Machine.

### Data Protection
All S3 buckets in this application use AWS KMS server-side encryption (SSEAlgorithm: aws:kms) to encrypt data at rest. Public access is blocked on all buckets using PublicAccessBlockConfiguration. DynamoDB tables use AWS-managed encryption by default. All API traffic uses HTTPS through API Gateway, enforced by the S3 bucket policy which denies all non-HTTPS requests.

### API Gateway Security
In production, the API Gateway should be secured using AWS Cognito for user authentication or API keys for service-to-service communication. Rate limiting should be applied to prevent abuse. Currently the API is open to the public which is acceptable for a development environment but not for production.

### Disaster Recovery Plan
Each resource in the system has a potential failure mode and recovery strategy. S3 buckets should have versioning enabled so deleted files can be recovered. DynamoDB tables should have point-in-time recovery (PITR) enabled to restore data to any point in the last 35 days. Lambda functions are stateless and automatically recover from failures. Step Functions automatically retry failed executions. API Gateway has built-in high availability across multiple availability zones.

---

## 3. Well-Architected Framework

### Pillar 1 — Operational Excellence
**Question:** How does the application monitor and respond to operational events?

**Answer:** The application uses AWS CloudWatch for logging all Lambda function executions. Each Lambda has a dedicated log group with a retention period set to 7 days. The health endpoint at /api/health provides real-time status monitoring of the application. In production, CloudWatch Alarms should be configured to alert on Lambda errors, high latency, or DynamoDB throttling events. AWS X-Ray tracing is enabled on all Lambda functions to trace requests end to end through the system.

### Pillar 2 — Security
**Question:** How does the application protect data and control access?

**Answer:** The application enforces encryption in transit by denying all non-HTTPS requests through S3 bucket policies. Data at rest is encrypted using AWS KMS on all S3 buckets. In production, each Lambda should have a least-privilege IAM role rather than the shared LabRole. API Gateway should be protected with Cognito authentication. DynamoDB tables should have fine-grained access control so only authorized Lambda functions can read or write to them.

### Pillar 3 — Reliability
**Question:** How does the application handle failures and ensure availability?

**Answer:** The application uses AWS managed services that provide built-in high availability. Lambda functions automatically scale and retry on failure. Step Functions provides error handling and retry logic for the state machine. DynamoDB is a fully managed NoSQL database with built-in replication across multiple availability zones. In production, DynamoDB point-in-time recovery should be enabled. Dead letter queues should be added to Lambda functions to capture failed invocations for later analysis.

### Pillar 4 — Performance Efficiency
**Question:** How does the application use resources efficiently?

**Answer:** The application uses a serverless architecture which means resources are only consumed when requests are made. Lambda functions scale automatically based on demand with no idle costs. DynamoDB uses PAY_PER_REQUEST billing mode which scales automatically based on traffic. S3 pre-signed URLs are used for direct image uploads from the browser to S3, bypassing the Lambda function and reducing latency. AWS Textract provides fast OCR processing without requiring any infrastructure management.

### Pillar 5 — Cost Optimization
**Question:** How does the application minimize costs while meeting requirements?

**Answer:** The serverless architecture ensures the application only incurs costs when it is actually used. Lambda functions are billed per invocation and per millisecond of execution time. DynamoDB PAY_PER_REQUEST mode means there are no costs for idle capacity. S3 storage costs are minimal for small image files. CloudWatch log retention is set to 7 days to minimize log storage costs. In production, AWS Cost Explorer and Budgets should be configured to monitor and alert on unexpected cost increases.

---

## 4. Total Cost of Ownership (TCO)

Based on estimates from calculate.aws for the AWS services used in this application running in us-east-1:

| Service | Monthly Estimate |
|---|---|
| API Gateway (1M requests) | $3.50 |
| Lambda (1M invocations, 512MB) | $0.20 |
| S3 (10GB storage) | $0.23 |
| DynamoDB (PAY_PER_REQUEST, 1M reads/writes) | $1.25 |
| Step Functions (10K executions) | $0.25 |
| AWS Textract (1K pages) | $1.50 |
| CloudWatch Logs (5GB) | $2.50 |
| **Total Estimated Monthly Cost** | **~$9.43** |

This estimate assumes moderate usage of approximately 1 million API requests per month. The serverless architecture means costs scale linearly with usage and there are no fixed infrastructure costs. For a small team or individual user, monthly costs could be as low as $1-2.

---

## 5. Architecture Diagram

See `architecture.md` for the full Mermaid diagram.

---

## 6. UI Screenshot

The Yellow Sign Diner dashboard features:
- A three-column layout with Inbox, Process, and Records panels
- A dark theme with yellow accents
- An activity log at the bottom showing real-time processing status
- Upload, Process, and Delete functionality