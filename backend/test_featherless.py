import asyncio

from app.services.featherless import FeatherlessService


async def main():
    service = FeatherlessService()

    response = await service.chat(
        "Explain in one sentence what SQL injection is."
    )

    print("\n--- ShadowCode LLM TEST ---")
    print(response)
    print("--- END TEST ---\n")


if __name__ == "__main__":
    asyncio.run(main())