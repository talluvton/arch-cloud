import os
import re

# --- GitHub ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    GITHUB_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

DEFAULT_GH_PER_PAGE = int(os.getenv("GITHUB_PER_PAGE", "8"))
MAX_GH_PER_PAGE = 30

# --- HTML ---
UA = {"User-Agent": "Mozilla/5.0 (ArchCloud/1.0)"}

# Light keyword hints (for HTML only)
HTML_HINTS = [
    # AWS
    "lambda", "s3", "dynamodb", "api gateway", "eks", "ec2", "rds", "cloudfront", "route 53",
    "kinesis", "msk", "firehose", "sqs", "sns", "athena", "glue", "redshift", "eventbridge",
    "step functions", "cloudwatch",
    # Azure
    "app service", "azure functions", "blob storage", "cosmos db", "aks", "azure sql",
    "application gateway", "front door", "traffic manager", "data factory",
    "event hubs", "service bus", "synapse analytics", "monitor", "key vault",
    # GCP
    "cloud functions", "cloud run", "compute engine", "gke", "cloud storage",
    "bigquery", "dataflow", "pub/sub", "spanner", "bigtable", "vertex ai",
]

# Terraform + CloudFormation identifiers (for code files)
CODE_TOKEN_REGEX = re.compile(
    r'('
    r'\b(aws_[a-z0-9_]+|azurerm_[a-z0-9_]+|google_[a-z0-9_]+)\b'  # Terraform
    r'|'
    r'\bAWS::[A-Za-z0-9]+::[A-Za-z0-9]+\b'                        # CloudFormation
    r')',
    flags=re.I
)

# ---- Roles --------------------------------------------------------------
VALID_ROLES = {
    "Compute","Storage","Database","Networking",
    "Security","Monitoring","Integration","Analytics","DevOps","Other"
}

ROLE_SYNONYMS = {
    "ml": "Analytics", "machine learning": "Analytics", "ai": "Analytics",
    "observability": "Monitoring", "monitoring & logging": "Monitoring",
    "messaging": "Integration", "eventing": "Integration", "streaming": "Integration",
    "data integration": "Integration",
    "identity": "Security", "security & identity": "Security",
    "cdn": "Networking", "networking & cdn": "Networking",
    "cicd": "DevOps", "ci/cd": "DevOps",
}

# ---- Service name canonicalization ---------
# Lowercase keys -> canonical name with proper casing
CANONICAL_NAME_MAP = {
    # AWS
    "lambda": "Lambda",
    "s3": "S3",
    "dynamodb": "DynamoDB",
    "api gateway": "API Gateway",
    "kinesis": "Kinesis",
    "msk": "MSK",
    "firehose": "Firehose",
    "redshift": "Redshift",
    "athena": "Athena",
    "cloudwatch": "CloudWatch",
    "cloudfront": "CloudFront",
    "rds": "RDS",
    "eventbridge": "EventBridge",

    # Azure
    "app service": "App Service",
    "azure functions": "Azure Functions",
    "blob storage": "Blob Storage",
    "azure sql": "Azure SQL Database",
    "azure sql database": "Azure SQL Database",
    "cosmos db": "Cosmos DB",
    "application gateway": "Application Gateway",
    "front door": "Front Door",
    "event hubs": "Event Hubs",
    "service bus": "Service Bus",
    "data factory": "Data Factory",
    "synapse analytics": "Synapse Analytics",
    "monitor": "Monitor",
    "application insights": "Application Insights",
    "key vault": "Key Vault",
    "microsoft entra id": "Microsoft Entra ID",

    # GCP
    "cloud storage": "Cloud Storage",
    "cloud functions": "Cloud Functions",
    "pub/sub": "Pub/Sub",
    "dataflow": "Dataflow",
    "bigquery": "BigQuery",
    "workflows": "Workflows",
    "cloud build": "Cloud Build",
    "iam": "IAM",
}

# Final authority for role when a canonical name is recognized
NAME_ROLE_OVERRIDES = {
    # GCP
    "Cloud Storage": "Storage",
    "Cloud Functions": "Compute",
    "Pub/Sub": "Integration",
    "Dataflow": "Integration",
    "BigQuery": "Analytics",
    "Workflows": "Integration",
    "Cloud Build": "DevOps",
    "IAM": "Security",
    # AWS
    "Lambda": "Compute",
    "S3": "Storage",
    "DynamoDB": "Database",
    "API Gateway": "Networking",
    "Kinesis": "Integration",
    "MSK": "Integration",
    "Firehose": "Integration",
    "Redshift": "Analytics",
    "Athena": "Analytics",
    "CloudWatch": "Monitoring",
    "CloudFront": "Networking",
    "RDS": "Database",
    "EventBridge": "Integration",
    # Azure
    "App Service": "Compute",
    "Azure Functions": "Compute",
    "Blob Storage": "Storage",
    "Azure SQL Database": "Database",
    "Cosmos DB": "Database",
    "Application Gateway": "Networking",
    "Front Door": "Networking",
    "Event Hubs": "Integration",
    "Service Bus": "Integration",
    "Data Factory": "Integration",
    "Synapse Analytics": "Analytics",
    "Monitor": "Monitoring",
    "Application Insights": "Monitoring",
    "Key Vault": "Security",
    "Microsoft Entra ID": "Security",
}

# ---- Providers & features ----------------------------------------------
PROVIDER_MAP = {
    "aws": "AWS",
    "amazon web services": "AWS",
    "amazon": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "gcp": "GCP",
    "google cloud platform": "GCP",
    "google cloud": "GCP",
}