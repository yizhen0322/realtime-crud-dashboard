$stage = "staging_area"

# Clean start
Remove-Item -Path "submission.zip" -Force -ErrorAction SilentlyContinue
Remove-Item -Path $stage -Recurse -Force -ErrorAction SilentlyContinue
New-Item -Path $stage -ItemType Directory -Force | Out-Null

# Copy folders
Copy-Item -Path "backend" -Destination $stage -Recurse
Copy-Item -Path "frontend" -Destination $stage -Recurse

# Remove node_modules and pycache just in case
Remove-Item -Path "$stage\frontend\node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$stage\backend\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$stage\backend\*.pyc" -Recurse -Force -ErrorAction SilentlyContinue

# Copy config files
Copy-Item -Path "docker-compose.yml" -Destination $stage
Copy-Item -Path "requirements.txt" -Destination $stage
Copy-Item -Path "README.md" -Destination $stage
Copy-Item -Path "DEPLOY_TO_AWS_EC2.md" -Destination $stage
Copy-Item -Path "DEMO_SCRIPT.md" -Destination $stage

# Zip
Compress-Archive -Path "$stage\*" -DestinationPath "submission.zip" -Force

# Cleanup staging
Remove-Item -Path $stage -Recurse -Force
Write-Host "Submission zip updated."
