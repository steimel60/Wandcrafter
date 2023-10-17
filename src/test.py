import toml

# Load a TOML file
with open('test.toml', 'r') as f:
    data = toml.load(f)

print(type(data))
for key in data:
    print(key)
    print(data[key])