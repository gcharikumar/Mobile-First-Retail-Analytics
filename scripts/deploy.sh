#!/bin/bash
# scripts/deploy.sh
"""
Deploy to AWS: Builds Docker, pushes to ECR, updates ECS.
Requires AWS CLI, credentials in env.
"""
set -e
export AWS_REGION=ap-south-1  # Mumbai for DPDP
docker build -f Dockerfile.backend -t retail-backend .
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin <your-ecr-repo>
docker tag retail-backend <your-ecr-repo>/retail-backend:latest
docker push <your-ecr-repo>/retail-backend:latest
aws ecs update-service --cluster retail-cluster --service backend-service --force-new-deployment
cd frontend
npm run build
aws s3 sync dist/ s3://retail-pwa-bucket --delete
cd ../mobile
flutter build apk --release
aws s3 cp build/app/outputs/flutter-apk/app-release.apk s3://retail-mobile-bucket/