import asyncio

async def sowing(*plants):
    async def process_plant(name, soak_time, grow_time, root_time):
        print(f"0 Beginning of sowing the {name} plant")
        
        print(f"1 Soaking of the {name} started")
        await asyncio.sleep(soak_time / 1000)
        print(f"2 Soaking of the {name} is finished")
        
        print(f"3 Shelter of the {name} is supplied")
        await asyncio.sleep(grow_time / 1000)
        print(f"4 Shelter of the {name} is removed")
        
        print(f"5 The {name} has been transplanted")
        await asyncio.sleep(root_time / 1000)
        print(f"6 The {name} has taken root")
        
        print(f"9 The seedlings of the {name} are ready")
    
    async def fertilize(name):
        print(f"7 Application of fertilizers for {name}")
        await asyncio.sleep(3 / 1000)
        print(f"7 Fertilizers for the {name} have been introduced")
    
    async def pest_control(name):
        print(f"8 Treatment of {name} from pests")
        await asyncio.sleep(5 / 1000)
        print(f"8 The {name} is treated from pests")
    
    tasks = []
    for plant in plants:
        name, soak, grow, root = plant
        plant_task = asyncio.create_task(process_plant(name, soak, grow, root))
        fertilize_task = asyncio.create_task(fertilize(name))
        pest_task = asyncio.create_task(pest_control(name))
        
        tasks.extend([plant_task, fertilize_task, pest_task])
    
    await asyncio.gather(*tasks)

asyncio.run(sowing(
    ("El Pommidorro", 2000, 5000, 3000),
    ("Amigo Potato", 1500, 4000, 2500),
    ("Cucu deMber", 3000, 6000, 3500)
))