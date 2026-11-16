
import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        response = table.scan()
        incidents = response.get("Items", [])

        # Retrieve remaining records if DynamoDB paginates results
        while "LastEvaluatedKey" in response:
            response = table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            incidents.extend(response.get("Items", []))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(incidents)
        }

    except Exception as error:
        print(f"Error retrieving incidents: {error}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Unable to retrieve incidents."
            })
        }
