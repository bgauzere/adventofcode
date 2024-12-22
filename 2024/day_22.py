import sys

def next_secret(number):
    secret = number * 64
    secret = mix(secret, number)
    secret = prune(secret)
    result = int(secret / 32)
    secret = mix(secret, result)
    secret = prune(secret)
    result = secret * 2048
    secret = mix(secret, result)
    secret = prune(secret)
    return secret

def prune(number):
    return number % 16777216

def mix(number, other_number):
    return number ^ other_number

def generate(number):
    for _ in range(2000):
        number = next_secret(number)
    return number 

def read_numbers(filename):
    with open(filename) as f:
        data = f.readlines()
        return [int(number.strip()) for number in data]

if __name__ == "__main__":
    numbers = read_numbers(sys.argv[1])
    print(sum([generate(number) for number in numbers]))
