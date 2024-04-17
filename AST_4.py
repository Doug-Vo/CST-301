import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="CST-301",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# Path to the file containing simple function API list
function_file_path = 'inputFile/Function_API_List.txt'

# Reading the file into a list of tuples
function_list = []
with open(function_file_path, 'r') as file:
    for line in file:
        # Strip newline and split by comma
        entries = line.strip().split(', ')
        # Append as a tuple
        function_list.append(tuple(entries))

# Path to the file containing detailed API and function information
detailed_file_path = 'inputFile/API_Function_Specific_Details.txt'

# Reading the file into a list of tuples
detailed_api_function_list = []
with open(detailed_file_path, 'r') as file:
    for line in file:
        # Strip newline and split by comma
        entries = line.strip().split(', ')
        # Append as a tuple
        detailed_api_function_list.append(tuple(entries))



# Create a cursor object
cursor = conn.cursor()

# Sample data (you can replace this with your actual data)
cursor.executemany('INSERT INTO functions_api VALUES (%s, %s)', function_list)
# Insert data into the table
cursor.executemany('INSERT INTO api_function_specific VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', detailed_api_function_list)

# Commit changes
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
