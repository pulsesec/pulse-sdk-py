from pulse import PulseAPI, TokenNotFoundError, TokenUsedError, TokenExpiredError
import os


async def main():
    client = PulseAPI(os.getenv("PULSE_SITE_KEY"), os.getenv("PULSE_SECRET_KEY"))

    async def classify(token: str) -> bool:
        try:
            is_bot = await client.classify(token)
            return is_bot
        except TokenNotFoundError:
            raise "Token not found"
        except TokenUsedError:
            raise "Token already used"
        except TokenExpiredError:
            raise "Token expired"
        except Exception as e:
            raise e
