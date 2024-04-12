import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="CST301",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# Create a cursor object
cursor = conn.cursor()

# Sample data (you can replace this with your actual data)
java_list = [
    ('stream()', 'Collection'),
    ('addAll()', 'Collection'),
    ('toSet()', 'Collectors'),
    ('joining()', 'Collectors'),
    ('toCollection()', 'Collectors'),
    ('asList()', 'Arrays'),
    ('split()', 'String'),
    ('fromName()', 'Enum'),
    ('getProperties()', 'System'),
    ('getName()', 'Class'),
    ('equals()', 'Object'),
    ('allOf()', 'EnumSet'),
    ('size()', 'Collection'),
    ('add()', 'Collection'),
    ('contains()', 'Collection')
]
cursor.execute('''CREATE TABLE IF NOT EXISTS API_function_specific
                  (function_name TEXT, api_name TEXT, 
                  api_conext TEXT, api_topic TEXT, function_context TEXT, function_topic TEXT, 
                  llm_expert_API TEXT, sim_expert_API TEXT, llm_expert_function TEXT,
                  sim_expert_function TEXT, PRIMARY KEY (function_name, api_name))''')
# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS functions
                  (function_name TEXT PRIMARY KEY,
                  FOREIGN KEY (api_name) REFERENCES api_function_specific(api_name))''')

# Insert data into the table
cursor.executemany('INSERT INTO functions VALUES (%s, %s)', java_list)

# Commit changes
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
