from bot import Vtuber
import asyncio
async def main():
    vtuber = Vtuber()
    await vtuber.conversation()

if __name__ == "__main__":
    asyncio.run(main())