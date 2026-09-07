from mcp.server.mcpserver import MCPServer
from datetime import datetime, timedelta, timezone
import boto3
from starlette.responses import JSONResponse

from kubernetes import client, config

mcp = MCPServer("taskflow-infra")

cloudwatch = boto3.client("cloudwatch")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "ok"})


def load_k8s_config():
    try:
        config.load_incluster_config()
        print("Config: in-cluster (ServiceAccount)")
    except config.ConfigException:
        config.load_kube_config()
        print("Config: local (~/.kube/config)")


load_k8s_config()

v1 = (
    client.CoreV1Api()
)  # Kubernetes Python Client , creates an object that Python comunicate with Kubernetes through API Server


@mcp.tool()
def get_pods_status(namespace: str = "default") -> list[dict[str, str]]:
    """Returnează statusul podurilor dintr-un namespace dat."""

    pods = v1.list_namespaced_pod(namespace=namespace)

    if not pods.items:
        return []

    return [
        {"name": pod.metadata.name, "status": pod.status.phase} for pod in pods.items
    ]


@mcp.tool()
def get_rds_metrics() -> list[dict]:
    """Returnează CPU-ul mediu al instanței RDS taskflow-postgres din ultimele 10 minute."""

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=10)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/RDS",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "DBInstanceIdentifier", "Value": "taskflow-postgres"}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"],
    )

    datapoints = response["Datapoints"]

    if not datapoints:
        return [
            {
                "rds_instance": "taskflow-postgres",
                "cpu_percent": None,
                "message": "No CPU datapoints available",
            }
        ]

    latest = max(datapoints, key=lambda x: x["Timestamp"])

    return [
        {
            "rds_instance": "taskflow-postgres",
            "cpu_percent": round(latest["Average"], 2),
            "timestamp": latest["Timestamp"].isoformat(),
        }
    ]


@mcp.tool()
def get_nodes_status() -> list[dict[str, str]]:
    """Returnează statusul node-urilor din clusterul Kubernetes."""

    nodes = v1.list_node()

    result = []

    for node in nodes.items:

        name = node.metadata.name
        status = "Unknown"

        for condition in node.status.conditions:
            if condition.type == "Ready":
                status = condition.status
                break

        result.append({"name": name, "status": status})

    return result


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
