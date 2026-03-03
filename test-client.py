import requests
import time
import uuid

US_url = f"http://136.115.153.255:8080"
Euro_url = f"http://34.53.248.49:8080"

def measure_latency(url, endpoint):
    start = time.time()
    requests.post(f"{url}{endpoint}")
    end = time.time()
    return (end - start)

def run_latency_test():
    iterations = 10
    instances = [
        {'name': 'US-Central1', 'url': US_url},
        {'name': 'Europe-West1', 'url': Euro_url}
    ]

    for instance in instances:
        total_register_time = 0
        total_list_time = 0
        for _ in range(iterations):
            total_register_time += measure_latency(instance['url'], '/register')
            total_list_time += measure_latency(instance['url'], '/list')
        print(instance['name'] + f" Avg Latency /register: {total_register_time / iterations}s")
        print(instance['name'] + f" Avg Latency /list: {total_list_time / iterations}s")

def run_consistency_test():
    iterations = 100
    missed_updates = 0
    for i in range(iterations):
        username = f"user_{uuid.uuid4()}"
        requests.post(f"{US_url}/register", json={"username": username})
        response = requests.get(f"{Euro_url}/list")
        users = response.json().get('users', [])
        if username not in users:
            missed_updates += 1
    print(f"Consistency Misses: {missed_updates}")

if __name__ == "__main__":
    requests.post(f"{US_url}/clear")
    requests.post(f"{Euro_url}/clear")
    run_latency_test()
    run_consistency_test()