import logging

import uvicorn

from bingo.settings import settings


def main() -> None:
    logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOGGING_FORMAT)
    uvicorn.run(
        "bingo.api:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
