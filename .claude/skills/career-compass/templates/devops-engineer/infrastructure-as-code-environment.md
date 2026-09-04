---
title: "Infrastructure as Code for a Cloud Environment"
track: "devops-engineer"
difficulty_tier: "intermediate"
estimated_hours: 16
role: "core"
skill_tags: ["infrastructure-as-code", "cloud-platforms", "networking-fundamentals", "secrets-management"]
skill_prerequisites: ["linux-cli", "git-version-control"]
project_prerequisites: []
prerequisite_learning_hours: 5
---

# Infrastructure as Code for a Cloud Environment

## Production Workflow Mirrored
1. Declaring networks, compute, storage, and access in version-controlled code
2. Planning and reviewing infrastructure changes before applying them
3. Managing remote state safely with locking
4. Reusing modules across environments with different variables
5. Tearing everything down cleanly and proving it comes back identically

## What You'll Build
A Terraform (or Pulumi/OpenTofu) project that provisions a small but
realistic environment on AWS, GCP, or Azure: a VPC with public and
private subnets, a compute instance or container service in the private
subnet, a load balancer in the public subnet, a managed database, a
storage bucket, least-privilege IAM, and remote state with locking, all
parameterized so a `staging` and a `prod` workspace differ only by
variables.

## Student-Scope Notes
- Use the cloud free tier and the smallest instance sizes. Set a billing
  alarm before you start and destroy the environment when not in use.
- One cloud provider. The concepts transfer.
- Use a hosted state backend (S3 plus DynamoDB, GCS, or Terraform Cloud).
  Local state is not acceptable for this project.

## Steps
1. Set up the remote state backend with locking and a separate state per
   workspace. Set the billing alarm.
2. Write the network module: VPC, public and private subnets across two
   availability zones, route tables, NAT for private egress.
3. Write the compute module: an instance or container service in the
   private subnet with a security group that only accepts traffic from
   the load balancer.
4. Add the load balancer with a health check, the managed database in
   the private subnet with a generated password stored in the cloud's
   secrets manager, and a private storage bucket.
5. Write IAM roles with least privilege for the compute to reach the
   bucket and the secret, and nothing else.
6. Create `staging` and `prod` workspaces and prove they deploy from the
   same code with different variables (sizes, counts, names).
7. Make a change (add a subnet, resize an instance), review the plan,
   apply it, and confirm the plan is empty afterward. Then destroy and
   re-apply to prove reproducibility.
8. Add a CI workflow that runs format, validate, and plan on pull
   requests and posts the plan as a comment. Write up the architecture
   diagram, the module structure, and the cost of the environment.

## Extension Ideas
- Add policy checks (OPA or the provider's policy framework) that block
  public buckets.
- Add drift detection on a schedule.
- Add a bastion or SSM-based access path for the private instance.
- Convert the compute to an autoscaling group with a launch template.

## Skills Demonstrated
- Declarative infrastructure with modules and workspaces
- Cloud networking, load balancing, and least-privilege IAM
- Remote state, plan review, and reproducibility
- Infrastructure change management in CI

## Industry Relevance

Cloud-Native SaaS, Fintech, Enterprise IT. Every cloud environment in these sectors is expected to be reproducible from code, and infrastructure engineers are hired on their ability to design networks and IAM safely and manage change through plans. A reviewed, reproducible environment on a real cloud is the standard portfolio piece.
