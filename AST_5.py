import psycopg2


# Function to parse the function properties from a line
def parse_function(line):
    parts = line.strip().split("= ")
    if len(parts) < 2:
        return None
    function_name = parts[0].strip()
    properties = [prop.strip() for prop in parts[1].strip("[]").split(",")]
    return function_name, properties


# Establish connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="CST-301",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

file_path = "output4.txt"
detailed_api_function_list = []
function_list = []

# Read and parse each line in the file
with open(file_path, "r") as file:
    for line in file:
        parsed_data = parse_function(line)
        if parsed_data:
            function_name, properties = parsed_data
            detailed_api_function_list.append(tuple(properties))
            function_list.append(tuple(properties[:2]))

# Create a cursor for database operations
cursor = conn.cursor()
# Insert data into the tables
try:
    cursor.executemany('INSERT INTO functions_api (function_name, api_name) VALUES (%s, %s)', function_list)
    cursor.executemany('INSERT INTO api_function_specific (function_name_fk, api_name_fk, api_context, api_topic, '
                       'function_context, function_topic, llm_expert_api, sim_expert_api, llm_expert_function, '
                       'sim_expert_function) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       detailed_api_function_list)
    conn.commit()  # Commit the transaction if no errors
except psycopg2.Error as e:
    print("Database error:", e)
    conn.rollback()  # Roll back in case of errors

# Close the cursor and connection
cursor.close()
conn.close()
