![alt text](ai.jpeg)


Comprehensive README: Automated Entry Level Cybersecurity Job Scraper with JSearch API
Introduction
This Python script empowers you to automate the process of scraping cybersecurity job listings from the JSearch API. It streamlines your search for relevant opportunities, saving you time and effort in the job hunting process.
Requirements
•	Python 3: Ensure you have Python 3 installed on your system (download from https://www.python.org/downloads/).
•	requests Library: Install this library using pip install requests in your terminal to interact with the JSearch API.
•	csv Library: Included in the Python standard library, this library allows you to create and write data to CSV files.
•	Openpyxl Library (Optional): Install using pip install openpyxl if you want to save results to Excel (XLSX) files.
•	RapidAPI Account and API Key: Sign up for a RapidAPI account and acquire an API key specifically for the JSearch API. This key is crucial for accessing the API and retrieving data.
Usage
1.	Obtain API Key: Create a RapidAPI account and acquire an API key dedicated to the JSearch API.
2.	Replace Placeholder: Replace "API_KEY" in the headers dictionary with your actual API key.
3.	Configure Search Parameters (Optional): Modify the script to include additional parameters within the querystring dictionary. Refer to the JSearch API documentation for supported parameters like location, date posted, or job type.
4.	Run the Script: Execute the script using Python. Navigate to the directory containing the script (e.g., job_scraper.py) and run the command python job_scraper.py in your terminal.
Output
The script retrieves data from the first 10 pages (customizable) of the JSearch API search results and saves the extracted job information to two files:
•	cyber_security_jobs.csv: A CSV file containing the job listings in a structured format.
•	cyber_security_jobs.xlsx (Optional): An Excel file containing the job listings (requires openpyxl library).
Script Functionality
1. Imports:
•	requests: Facilitates communication with the JSearch API.
•	csv: Allows creation and writing of data to CSV files.
•	os (Optional): Provides operating system interaction (not used in core functionality).
•	openpyxl (Optional): Used for creating and writing to Excel files (if installed).
2. API Endpoint and Headers:
•	Defines the JSearch API endpoint URL.
•	Defines the request headers containing your API key for authentication.
3. get_cyber_security_jobs Function:
•	Retrieves job listings from the JSearch API by iterating through a specified number of pages.
•	Handles potential errors during API requests or data parsing.
•	Extracts relevant job information like title, description, company, location, salary (if available), and job link.
•	Returns a list containing dictionaries of extracted job data.
4. save_to_csv Function:
•	Saves the extracted job data from the list to a CSV file.
•	Handles potential errors during file creation or writing.
5. save_to_excel Function (Optional):
•	Saves the extracted job data to an Excel file (requires openpyxl).
•	Handles potential errors during file creation or writing.
6. Main Execution:
•	Executes the get_cyber_security_jobs function to retrieve data.
•	Prints the total number of jobs retrieved.
•	Calls both save_to_csv and save_to_excel functions (if openpyxl is installed) to save the data.
Customization
•	API Parameters: Explore the JSearch API documentation for additional filtering options you might want to include in the querystring dictionary.
•	Data Extraction: You can modify the fields extracted from the API response within the get_cyber_security_jobs function.
•	Error Handling: Consider implementing more robust error handling for various scenarios.
•	Rate Limits: Be mindful of the JSearch API's rate limits and adjust the script's execution frequency accordingly.
Benefits of Automation
•	Efficiency: Saves you time by automating the job search process.
•	Targeted Search: Focuses on entry-level cybersecurity jobs or customize further based on your needs.
•	Organized Data: Keeps your job search organized with structured data export options in CSV and Excel
Upload an image 
This prompt requires an image that you need to add. Tap the image button to upload an image. 
Got it 
Need a little help with this prompt? 
Power up your prompt and Gemini will expand it to get you better results 
Got it 


import requests  
import csv
import os
from openpyxl import Workbook

# Define the API endpoint and query parameters
url = "https://jsearch.p.rapidapi.com/search"
querystring = { 
    "query": "entry level cyber security",
    "page": "1",
    "num_pages": "1"
}

# Define the request headers
headers = {  # Corrected '-' to '='
    "x-rapidapi-key": "****",
    "x-rapidapi-host":"jsearch.p.rapidapi.com"
}

# Function to retrieve and filter cybersecurity-related jobs from the API
def get_cyber_security_jobs(pages=10):
    all_jobs = []
    for page in range(1, pages + 1):
        try:
            querystring["page"] = str(page)
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an exception for unsuccessful requests

            # Parse the JSON response
            data = response.json()  # Corrected '-' to '='

            # Print the response for debugging
            print(f"Fetching page {page}...")

            if 'data' in data and isinstance(data['data'], list):
                jobs = data['data']  # Corrected 'dat' to 'data'
                print(f"Found {len(jobs)} jobs on page {page}.")
                
                for job in jobs:
                    job_data = {
                        'Job Title': job.get('job_title', 'No Job Title Provided'),
                        'Description': job.get('job_description', 'No Job Description Provided'),
                        'Company': job.get('employer_name', 'No Company Provided'),
                        'Location': f"{job.get('job_city', 'No City Provided')}, {job.get('job_state', 'No State Provided')}",
                        'Salary': job.get('job_salary', 'Not Provided'),
                        'Job Link': job.get('job_apply_link', 'No Job Link Provided')
                    }
                    all_jobs.append(job_data)
                    print(f"Added job: {job_data['Job Title']}")

            else:
                print(f"No jobs found on page {page}.")
                
        except requests.RequestException as e:  
            print(f"Request failed on page {page}: {e}")
        except ValueError as e:
            print(f"Error parsing JSON response on page {page}: {e}")
    
    return all_jobs

def save_to_csv(jobs, filename='cyber_security_jobs.csv'):  
    if jobs:
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["Job Title", "Description", "Company", "Location", "Salary", "Job Link"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(jobs)
            print(f"Successfully saved {len(jobs)} job listings to {filename}")
        except IOError as e:
            print(f"Error saving to CSV: {e}")
    else:
        print("No cybersecurity jobs to save.")

def save_to_excel(jobs, filename='cyber_security_jobs.xlsx'):
    if jobs:
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Cyber Security Jobs"
            
            # Write header
            headers = ["Job Title", "Description", "Company", "Location", "Salary", "Job Link"]
            ws.append(headers)
            
            # Write data
            for job in jobs:
                ws.append([job[header] for header in headers])
            
            wb.save(filename)
            print(f"Successfully saved {len(jobs)} job listings to {filename}")
        except Exception as e:
            print(f"Error saving to Excel: {e}")
    else:
        print("No cybersecurity jobs to save.")

if __name__ == "__main__": 
    entry_level_cyber_security_jobs = get_cyber_security_jobs(pages=10)
    print(f"Retrieved a total of {len(entry_level_cyber_security_jobs)} jobs")
    
    save_to_csv(entry_level_cyber_security_jobs)
    save_to_excel(entry_level_cyber_security_jobs)
