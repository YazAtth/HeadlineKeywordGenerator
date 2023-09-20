import Main
import NounFrequency


def lambda_handler(event, context):

    Main.run()

    return {
        'statusCode': 200
    }

