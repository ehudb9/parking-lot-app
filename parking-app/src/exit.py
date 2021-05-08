import json
import boto3
from datetime import datetime, time
import math
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


def lambda_exit(event, context):
    # connecting to the dynamodb table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('parkingLot')

    # initializing the exit Ticket
    exitTicket = {}

    exitTimeDate = datetime.now()

    # getting params from the request
    ticketId = event['queryStringParameters']["ticketId"]

    try:
        # getting the entry ticket data fro m the Parking-lot table in dynamodb
        response = table.get_item(Key={'ID': ticketId})

        # convert entry time to datetime object
        entryTimeStr = response['Item']['Entry_Time']
        entryDateStr = response['Item']['Entry_Date']
        entryTimeDateStr = entryDateStr + ' ' + entryTimeStr
        entryTime = datetime.strptime(entryTimeDateStr, '%Y-%m-%d %H:%M:%S')

        # calculating time difference
        totalTime = exitTimeDate - entryTime
        totalHours = totalTime.seconds // 3600
        totalMin = (totalTime.seconds % 3600) // 60
        charge = 2.5 * math.ceil(((totalTime.seconds / 60) / 15))

        # preparing exit ticket
        exitTicket['Plate Number'] = response['Item']['Plate_Number']
        exitTicket['Total Parked Time'] = f"{totalHours} Hours and {totalMin} Minutes"
        exitTicket['Parking Lot ID'] = response['Item']['Parking_Lot']
        exitTicket['Charge'] = f"{charge} $"

        table.delete_item(Key={'ID': ticketId})
        return {
            'body': json.dumps(exitTicket)
        }
    except:
        return {"Error": "Please enter a valid ticket id"}