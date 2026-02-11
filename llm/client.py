import boto3
from botocore.exceptions import BotoCoreError, ClientError

class BedrockClient:
    """
    A generic client for interacting with language models on AWS Bedrock.
    """
    def __init__(self, region_name: str = "us-east-1"):
        """
        Initializes the Bedrock client.

        :param region_name: The AWS region for the Bedrock runtime client.
        """
        try:
            self.client = boto3.client("bedrock-runtime", region_name=region_name)
            print("Bedrock client initialized successfully.")
        except (BotoCoreError, ClientError) as e:
            print(f"Error initializing Bedrock client: {e}")
            self.client = None

    def converse(self, model_id: str, prompt: str) -> str:
        """
        Sends a prompt to a model using the Converse API and gets a response.

        :param model_id: The ID of the model to use (e.g., 'amazon.nova-lite-v1:0').
        :param prompt: The user prompt to send to the model.
        :return: The text content of the model's response, or an error message.
        """
        if not self.client:
            return "Error: Bedrock client not initialized."

        try:
            response = self.client.converse(
                modelId=model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}
            ],
            )
            return response["output"]["message"]["content"][0]["text"]
        except (ClientError, BotoCoreError) as e:
            return f"Error during conversation with model '{model_id}': {e}"
        except (KeyError, IndexError) as e:
            return f"Error parsing response from model '{model_id}': {e}"

if __name__ == '__main__':
    # This is an example of how to use the client.
    # To run this, you need to have AWS credentials configured.
    
    # 1. Create a client instance
    bedrock_client = BedrockClient()

    # 2. Check if the client was created successfully
    if bedrock_client.client:
        
        # 3. Specify the model and prompt
        # As per user's info: amazon.nova-micro-v1:0, amazon.nova-lite-v1:0, etc.
        # You can also use other models like 'anthropic.claude-3-sonnet-20240229-v1:0'
        # model_to_use = "anthropic.claude-3-sonnet-20240229-v1:0"
        model_to_use = "amazon.nova-lite-v1:0"
        user_prompt = "こんにちは。自己紹介をしてください。"
        
        # 4. Send the prompt to the model
        print(f"\nSending prompt to {model_to_use}: '{user_prompt}'")
        model_response = bedrock_client.converse(model_id=model_to_use, prompt=user_prompt)
        
        # 5. Print the response
        print(f"\nResponse:\n---\n{model_response}\n---")

