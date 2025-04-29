import asyncio

async def interviews(*candidates):
    async def process_candidate(name, prep1, defense1, prep2, defense2):
        # Первое задание
        print(f"{name} started the 1 task.")
        await asyncio.sleep(prep1 / 100)
        print(f"{name} moved on to the defense of the 1 task.")
        await asyncio.sleep(defense1 / 100)
        print(f"{name} completed the 1 task.")
        
        print(f"{name} is resting.")
        await asyncio.sleep(5 / 100)
        
        print(f"{name} started the 2 task.")
        await asyncio.sleep(prep2 / 100)
        print(f"{name} moved on to the defense of the 2 task.")
        await asyncio.sleep(defense2 / 100)
        print(f"{name} completed the 2 task.")
    await asyncio.gather(
        *(process_candidate(*candidate) for candidate in candidates)
    )


asyncio.run(interviews(
    ("Ashen one", 500, 300, 400, 200),
    ("Oceiros", 200, 100, 300, 150),
    ("Artorias", 1000, 200, 500, 300)
))