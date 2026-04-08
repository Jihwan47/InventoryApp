import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
TABLE_NAME = 'Inventory'

# Function to convert Decimal to int/float
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):  
        return int(obj) if obj % 1 == 0 else float(obj)  # Convert to int if whole number, else float
    return obj

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    try:
        item_id = event['pathParameters']['id']
        location_id = int(event['queryParameter']['location_id'])
        
        # Query to get all items with PK = "Location1"
        response = table.delete_item(
            Key={
                'item_id': item_id,
                'location_id': location_id
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Item deleted successfully')
        }
    
    except ClientError as e:
        print(f"Failed to delete items: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to query items')
        }

