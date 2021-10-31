import yaml

with open('Project2/values.yml') as stream:
    values = yaml.safe_load(stream)

print(values)