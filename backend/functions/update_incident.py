
import json
import os

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        incident_id = event.get("pathParameters", {}).get("incident_id")

        if not incident_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Incident ID is required."})
            }

        body = json.loads(event.get("body") or "{}")
        new_status = body.get("status", "").lower()

        allowed_statuses = ["open", "investigating", "resolved"]

        if new_status not in allowed_statuses:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid incident status."})
            }

        response = table.update_item(
            Key={"incident_id": incident_id},
            UpdateExpression="SET #status = :status",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":status": new_status},
            ConditionExpression="attribute_exists(incident_id)",
            ReturnValues="ALL_NEW"
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response["Attributes"])
        }

    except ClientError as error:
        if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Incident not found."})
            }
        raise

    except Exception as error:
        print(f"Error updating incident: {error}")

        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Unable to update incident."})
        }
