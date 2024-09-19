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
    "x-rapidapi-key": "0beb7f2182mshdaa8d0a1d500f2ep1490ebjsnc5d5ee125d5d",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
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