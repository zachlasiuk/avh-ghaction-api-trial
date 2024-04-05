#Tutorial for AVH trial Actions.

Pipeline:
1. GitHub Action triggers manually (will change to any PR when streamlined)
2. GitHub connects to AWS Lambda function URL, with a private key (stored in GitHub secrets) for authentication.
3. AWS Lambda authenticates request is valid, then runs a basic AVH test spinning up a RPi4 instance.
4. Status is returned to GitHub Actions (max timeout is 15min for a test to AVH)

Coming improvements:
- Dynamic test support via AWS Lambda proxy service
