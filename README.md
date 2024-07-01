<h1 align="center"><a href="https://www.pulsesecurity.org/">Pulse Security</a></h1>
<p align="center">
<img src="https://avatars.githubusercontent.com/u/161549711?s=200&v=4"/>
</p>
<h1 align="center">Python SDK</h1>

## Installation

```sh
$ pip install pulsesec
```

## Example

```py
from pulse import Pulse, TokenNotFoundError, TokenUsedError, TokenExpiredError
import os


async def main():
    client = Pulse(os.getenv("PULSE_SITE_KEY"), os.getenv("PULSE_SECRET_KEY"))

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
```
