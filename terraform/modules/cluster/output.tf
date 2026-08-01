output "cluster_name" {
  value = aws_eks_cluster.main_cluster.name
}

output "cluster_certificate_authority_data" {
  description = "Cluster CA certificate"
  value       = aws_eks_cluster.main_cluster.certificate_authority[0].data
}

output "oidc_issuer_url" {
  description = "OIDC issuer URL for IRSA"
  value = aws_eks_cluster.main_cluster.identity[0].oidc[0].issuer
}