
# US_Visa_Approval_Prediction

## Git Commands

To update the folder structure and push changes to the repository, use the following commands:

```bash
git add .
git commit -m "folder_update_structure"
git push origin main
```

## How to run?

To set up and run the project, follow these steps:

1. Create a new conda environment with Python 3.8:

```bash
conda create -n visa python=3.8 -y
```

2. Activate the newly created environment:

```bash
conda activate visa
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Workflow

- **constant**
- **config_entity**
- **artifact_entity**
- **component**
- **pipeline**
- **app.py / demo.py**

## Export the environment variables

Make sure to export the necessary environment variables before running the application:

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>...."
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

## AWS-CICD-Deployment-with-Github-Actions

### Steps for AWS Deployment:

1. **Login to AWS Console**.
2. **Create an IAM user for deployment** with specific access:
    - EC2 access: Provides access to virtual machines.
    - ECR: Elastic Container Registry to store your Docker image.

### Deployment Process:

1. **Build Docker image** of the source code.
2. **Push Docker image to ECR**.
3. **Launch EC2 instance**.
4. **Pull Docker image from ECR** to EC2.
5. **Run Docker image in EC2**.

### Policies to Assign:

- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess`

### Steps to Set Up EC2:

1. **Create ECR repository** to store/save the Docker image.
   - Save the URI: `136566696263.dkr.ecr.us-east-1.amazonaws.com/mlproject`

2. **Create EC2 machine** (Ubuntu instance).

3. **Open EC2 and install Docker on the EC2 machine**:

Optional steps:

```bash
sudo apt-get update -y
sudo apt-get upgrade
```

Required steps:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

4. **Configure EC2 as a self-hosted runner**:

- Navigate to **Settings > Actions > Runners > New Self-hosted Runner**.
- Choose the operating system and run the provided commands one by one.

5. **Set up GitHub secrets**:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `ECR_REPO`

This will allow you to deploy and manage the US Visa Approval Prediction project with GitHub Actions and AWS.

---

### Note:

This `README.md` provides a basic outline of setting up the project, pushing to GitHub, and deploying it using Docker, ECR, and EC2 with AWS CI/CD pipelines.
