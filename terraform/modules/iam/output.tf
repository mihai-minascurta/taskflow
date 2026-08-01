output "cluster_role_arn" {

  value = aws_iam_role.eks_cluster_role.arn
}

output "worker_nodes_role_arn" {

  value = aws_iam_role.worker_nodes_role.arn

}
