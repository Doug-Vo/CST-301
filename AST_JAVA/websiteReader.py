import requests
from bs4 import BeautifulSoup


def read_java_documentation(url):
    result = ""
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the text content
        documentation_content = soup.find('div', class_="header")
        if documentation_content:
            result += documentation_content.get_text(separator='')
        else:
            print("Java documentation content not found on this page.")

        # Extract the text content
        documentation_content = soup.find('div', class_="inheritance")
        if documentation_content:
            result += documentation_content.get_text(separator='')
        else:
            print("Java documentation content not found on this page.")

        # Extract the text content
        documentation_content = soup.find('section', class_="class-description")
        if documentation_content:
            result += documentation_content.get_text(separator='')
        else:
            print("Java documentation content not found on this page.")
    else:
        print("Failed to retrieve Java documentation. Status code: {}".format(response.status_code))

    return result


# Example Java documentation URL
java_doc_url = "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ArrayList.html"

# Call the function to read the Java documentation content
java_doc_content = read_java_documentation(java_doc_url)
print(java_doc_content)
