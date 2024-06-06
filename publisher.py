import pika
import yaml
import json
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_path", type=str, help="path of yaml file for parameters")
    args = parser.parse_args()

    # Load parameters
    with open(args.yaml_path, "r") as file:
        parameters = yaml.safe_load(file)
    
    previous_id = parameters["io_parameters"]["uid_retrieve"]
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='latent_space_explorer', auto_delete=True)

    channel.basic_publish(
        exchange='',
        routing_key='latent_space_explorer',
        body=json.dumps({"flow_id": previous_id}),
    )

    connection.close()
