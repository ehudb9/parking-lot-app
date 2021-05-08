import json
from datetime import datetime
import boto3


def lambda_entry(event, context):
    # connecting to the dynamodb table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('parkingLot')

    # getting params from the request

    plate = event['queryStringParameters']["plate"]
    parkingLot = event['queryStringParameters']["parkingLot"]

    # generating unique ID - combination of plate and parking lot number
    plateNum = str(plate.replace('-', ''))
    id = str(parkingLot) + plateNum

    # converting current time and date to strings
    now = datetime.now()
    entryTime = now.strftime("%H:%M:%S")
    entryDate = str(now.date())

    # storing data into parking lot table in dynamodb
    response = table.put_item(Item={
        "Plate_Number": plate,
        "Parking_Lot": parkingLot,
        "ID": id,
        "Entry_Time": entryTime,
        "Entry_Date": entryDate
    })

    return {
        'body': json.dumps('TicketId: ' + id)
    }
