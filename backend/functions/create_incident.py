
import json
import os
import uuid
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        title = body.get("title", "").strip()
        description = body.get("description", "").strip()
        service = body.get("service", "").strip()

        if not title or not description or not service:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Title, description and service are required."
                })
            }

        severity = body.get("severity", "medium").lower()

        if severity not in ["low", "medium", "high", "critical"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid severity level."})
            }

        incident = {
            "incident_id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "service": service,
            "severity": severity,
            "status": "open",
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=incident)

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(incident)
        }

    except Exception as error:
        print(f"Error creating incident: {error}")

        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error."})
        }
