from pulse import PulseAPI, TokenNotFoundError, TokenUsedError
import os


async def main():
    client = PulseAPI(os.getenv("PULSE_SITE_KEY"), os.getenv("PULSE_SECRET_KEY"))

    async def classify(token: str) -> bool:
        try:
            is_bot = await client.classify(token)
            return is_bot
        except TokenNotFoundError:
            print("Token not found")
        except TokenUsedError:
            print("Token used")
        except Exception as e:
            print(f"An error occurred: {e}")
