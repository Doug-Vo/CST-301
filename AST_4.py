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
api_function_specific = [
    ("getInstance", "java.util.Calendar", "Provides methods to manipulate date and time.", "Date and Time", "Retrieves a Calendar instance.", "Date and Time", "Utility", "Date and Time", "Data Structure", "Date and Time"),
    ("setField","java.text.MessageFormat",  "Formats messages based on a pattern.", "Text Formatting", "Sets a field's value in a MessageFormat.", "Text Formatting", "Utility", "Setup", "Data Structure", "Text Formatting"),
    ("setCiteKey", "org.jabref.model.entry.BibEntry", "Represents a bibliographic entry.", "Bibliography", "Assigns a citation key to a BibEntry.", "Bibliography", "Databases", "Data Structure", "Databases", "Data Structure"),
    ("nextInt", "java.util.Scanner", "Provides simple text scanning utilities.", "Text Processing", "Returns the next int from this scanner.", "Text Processing", "Utility", "Logic", "Utility", "Logic"),
    ("getEntries", "java.util.zip.ZipFile", "Accesses the contents of zip files.", "Compression", "Returns an enumeration of ZIP file entries.", "Compression", "Utility", "Setup", "Data Structure", "Compression"),
    ("insertEntry", "org.jabref.model.database.BibDatabase", "Manages a collection of bibliographic entries.", "Bibliography", "Inserts a new BibEntry into a BibDatabase.", "Bibliography", "Databases", "Data Structure", "Databases", "Data Structure"),
    ("savePartOfDatabase", "org.jabref.logic.exporter.BibDatabaseWriter", "Handles exporting parts of bibliographic databases.", "Bibliography", "Saves a part of a BibDatabase to a file.", "Bibliography", "Databases", "Data Structure", "Databases", "Data Structure"),
    ("getImportFormatPreferences", "org.jabref.logic.importer.ImportFormatPreferences", "Manages preferences for import formats in JabRef.", "Bibliography", "Retrieves preferences for import formats.", "Bibliography", "Utility", "Setup", "Data Structure", "Bibliography"),
    ("parse", "java.text.SimpleDateFormat", "Parses date strings into Date objects.", "Date Parsing", "Parses text to produce a Date.", "Date Parsing", "Utility", "Setup", "Data Structure", "Date Parsing"),
    ("toList", "java.util.stream.Stream", "Transforms stream elements into a List.", "Data Processing", "Collects elements into a List.", "Data Processing", "Utility", "Application", "Data Structure", "Data Processing"),
    ("inferMode", "org.jabref.logic.bibtex.InferBibtexMode", "Infers the BibTeX mode based on content.", "Bibliography", "Infers BibTeX mode from database content.", "Bibliography", "Databases", "Data Structure", "Databases", "Data Structure"),
    ("format", "java.text.DateFormat", "Formats Date objects into date/time strings.", "Date Formatting", "Formats a Date into a date/time string.", "Date Formatting", "Utility", "Setup", "Data Structure", "Date Formatting"),
    ("containsAll", "java.util.Collection", "Provides collection manipulation utilities.", "Data Management", "Checks if the collection contains all items.", "Data Management", "Data Structure", "Application", "Data Structure", "Data Management"),
    ("main", "java.lang.String", "Serves as the entry point for Java applications.", "Application Control", "Serves as the entry point for applications.", "Application Control", "Utility", "Software Development", "Utility", "Software Development")
]

# Insert data into the table
cursor.executemany('INSERT INTO api_function_specific VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', api_function_specific)

# Commit changes
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
