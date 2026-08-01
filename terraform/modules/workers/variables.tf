variable "cluster_name" {
  type = string
}

variable "worker_nodes_role_arn" {
    type = string 
}

variable "private_subnets_ids" {
    type = list(string)
}

