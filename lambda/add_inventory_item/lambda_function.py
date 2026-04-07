"""Lambda function to add inventory items to DynamoDB."""
import json
import boto3
import uuid
import os
from decimal import Decimal


def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME','Inventory')

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty': data['item_qty'],
                'item_price': Decimal(str(data['item_price'])),
                'location_id': data['item_location_id']
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }


