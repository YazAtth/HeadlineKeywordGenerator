import Main
import NounFrequency


def lambda_handler(event, context):

    Main.run()
    # NounFrequency.get_top_nouns_and_plural_hash(["hello world", "python programming world"], 1)

    return {
        'statusCode': 200
    }

