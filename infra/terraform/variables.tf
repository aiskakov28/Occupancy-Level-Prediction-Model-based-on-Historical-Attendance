variable "region"      { type = string  default = "us-east-1" }
variable "project"     { type = string  default = "occupancy" }
variable "db_user"     { type = string  default = "postgres" }
variable "db_password" { type = string  sensitive = true }
