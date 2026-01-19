terraform {
  backend "s3" {
    encrypt = true
    bucket = "nau-richie-site-factory-terraform"
    dynamodb_table = "nau-richie_site_factory_terraform_state_locks"
  }
}

terraform {
  required_providers {
    aws = "~> 2.70"
  }
}
