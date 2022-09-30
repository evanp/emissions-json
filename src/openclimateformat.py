import urllib.request
import json
import datetime

def fetch_domain_data(domain):
    url = f'https://{domain}/.well-known/emissions.json'
    contents = urllib.request.urlopen(url).read()
    actor = json.loads(contents)
    return actor

def best_id(data):
    if data["type"] == "country" or data["type"] == "adm1":
        return data["identifiers"]["ISO 3166"]
    elif data["type"] == "city":
        return data["identifiers"]["UNLOCODE"]
    elif data["type"] == "company":
        return data["identifiers"]["LEI"]

def write_csv(columns, rows, directory, table):
    with open(f'{directory}/{table}.csv', 'w', encoding="utf-8") as f:
        f.write(",".join(columns) + "\n")
        for row in rows:
            f.write(",".join(map(str, row)) + "\n")

def write_publisher(data, domain, directory):
    id = best_id(data)
    columns = ["id", "name", "url"]
    rows = [[id, data["name"], f'https://{domain}/']]
    write_csv(columns, rows, directory, "Publisher")
    return id

def write_datasource(publisher_id, domain, directory):
    datestamp = datetime.datetime.utcnow().isoformat()[:10]
    datasource_id = f'emissions.json:{domain}:{datestamp}'
    columns = ["datasource_id", "name", "publisher", "published", "URL"]
    rows = [[datasource_id, f'emissions.json for {domain}', publisher_id, datestamp, f'https://{domain}/.well-known/emissions.json']]
    write_csv(columns, rows, directory, "DataSource")
    return datasource_id

def write_actor(data, datasource_id, directory):
    actor_id = best_id(data)
    columns = ["actor_id", "type", "name", "datasource_id"]
    rows = [[actor_id, data["type"], data["name"], datasource_id]]
    write_csv(columns, rows, directory, "Actor")
    return actor_id

def write_actor_identifiers(data, domain, datasource_id, actor_id, directory):
    columns = ["actor_id", "identifier", "namespace", "datasource_id"]
    rows = [[actor_id, domain, "DNS", datasource_id]]
    for key in data['identifiers'].keys():
        rows.append([actor_id, data['identifiers'][key], key, datasource_id])
    write_csv(columns, rows, directory, "ActorIdentifier")

def write_actor_emissions(data, datasource_id, actor_id, directory):
    columns = ["emissions_id", "actor_id", "year", "scope1_agg", "scope2_agg", "scope3_agg", "total_emissions", "datasource_id"]
    rows = []
    for yearstr in data["emissions"].keys():
        emission = data["emissions"][yearstr]
        year = int(yearstr)
        id = f'{actor_id}:{year}:{datasource_id}'
        total = emission["scope1"] + emission["scope2"] + emission["scope3"]
        rows.append([id, actor_id, year, emission["scope1"], emission["scope2"], emission["scope3"], total, datasource_id])
    write_csv(columns, rows, directory, "EmissionsAgg")

def domain_to_openclimate_dir(domain, directory):
    data = fetch_domain_data(domain)
    publisher_id = write_publisher(data, domain, directory)
    datasource_id = write_datasource(publisher_id, domain, directory)
    actor_id = write_actor(data, datasource_id, directory)
    write_actor_identifiers(data, domain, datasource_id, actor_id, directory)
    write_actor_emissions(data, datasource_id, actor_id, directory)

if __name__ == "__main__":
    import sys
    domain_to_openclimate_dir(sys.argv[1], sys.argv[2])
