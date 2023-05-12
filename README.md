# nuclear_job_database
This project is designed to compile a database of all nuclear related jobs for undergraduates to use when applying for jobs or internships. The project uses BeautifulSoup to parse HTML from a job postings and will add the information to a public spreadsheet using Google Sheets. 

# Current Problems
* Duplicate problem
    When parsing the job titles and locations, there are duplicates
* Loading dataframe to existing sheet, gives error " ValueError: Sheet 'Westinghouse' already exists and if_sheet_exists is set to 'error'." 