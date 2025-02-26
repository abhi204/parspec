import asyncio
import aiohttp
import time
import argparse

process_times = []

async def send_request(session, url, payload):
    async with session.post(url, json=payload) as response:
        start_time = time.time()
        response_data = await response.json()
        process_times.append(time.time() - start_time)
        return response_data

async def main(url, num_requests):
    payload = {
        "user_id": 1,
        "item_ids": [1,2,3,4,5],
        "total_amount": 1234
    }
    tasks = []

    async with aiohttp.ClientSession() as session:
        print("Script Start time: ", time.time())
        for _ in range(num_requests):
            tasks.append(send_request(session, url, payload))

        start_time = time.time()
        responses = await asyncio.gather(*tasks)

        print("Script End time: ", time.time())
        print("Total script execution time: ", time.time() - start_time)
        print("Average request processing time: ", sum(process_times) / len(process_times))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send async requests to a URL.')
    parser.add_argument('--url', type=str, default='http://localhost:8080/create_order', help='The URL to send requests to.')
    parser.add_argument('--num_requests', type=int, default=10, help='The number of requests to send.')

    args = parser.parse_args()
    asyncio.run(main(args.url, args.num_requests))