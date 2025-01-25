variable "credentials" {
  description = "My Credentials"
  default     = "G:/Sensitive/terr/creds.json"

}

variable "project" {
  description = "Project"
  default     = "dev-smoke-448803-a6"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "dev-smoke-448803-a6-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}