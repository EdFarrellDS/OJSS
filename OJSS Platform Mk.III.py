# coding: utf-8

# In[ ]:


# Visual formatting options

# Sets the display to 98% of the window's max width.
#from IPython.core.display import display, HTML
#display(HTML("<style>.container { width:98% !important; }</style>"))


# In[ ]:


# -------
# Imports
# -------

# Top-level, and always useful
import re
import os
from collections import Counter
from IPython.display import display
import sys
from copy import copy as sCopy

# Misc
import random
import ast

# Dataframes, yo!
import pandas as pd
import numpy as np

# ---------
# Functions
# ---------
# Flatten list of lists
def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

# Append items to list in-line, returning a list with appended items
def ret_append(lst, item):
    lst.append(item)
    return lst

def DROP_DATABASE(database_list):
    for database in database_list:
        if ".csv" in database:
            assert database in os.listdir(os.getcwd())
            os.remove(database)
            print("\nFile",database,"successfully deleted.")
        else:
            pass

# -----------------
# Misc declarations
# -----------------
# Pandas declarations

# Hide Chained Assignment (SettingWithCopy warning)
pd.options.mode.chained_assignment = None  # default='warn'


# In[ ]:


# Dataframe global variables
globAccountsDF = "accounts_db.csv"
globJobsDF = "jobs_db.csv"
globJobCatDF = "job_categories.csv"
globDocumentationDF = "job_documents.csv"
globInvitationDF = "job_invitation.csv"
glob_all_dataframes = [globAccountsDF, globJobsDF, globJobCatDF, globDocumentationDF, globInvitationDF]
glob_all_df_names = ["accounts_db.csv", "jobs_db.csv", "job_categories.csv", "job_documents.csv", "job_invitation.csv"]

local_files = os.listdir(os.getcwd())

# Global variables
#globUID = 'tetest0001s'
globUID = ''
globRecommendedCategories = []


# In[ ]:


# TO CLEAR ALL CSV FILES; 
#DROP_DATABASE(glob_all_df_names)


# # UI
# #### Boundary class
# For initialising and running the program

# In[ ]:


class UI:
#Checks whether the data is in the current working directory; if not, it builds new database files to work with.
    def initialise():
        global globAccountsDF
        global globJobsDF
        global globJobCatDF
        global globDocumentationDF
        global globInvitationDF
        global glob_all_dataframes
        global glob_all_df_names
        global globUID

        local_files = os.listdir(os.getcwd())

        # Checks whether database is present in CWD; if not, generate a new database
        for dbase in glob_all_dataframes:
            if dbase in os.listdir(os.getcwd()):
                print(dbase, "detected.")
                dbase = pd.read_csv(dbase)
            else:
                print(dbase, "not detected.")   

        # Handling missing databases
        local_files = os.listdir(os.getcwd())
        # If the accounts database is not present
        if "accounts_db.csv" not in local_files:
            demo_seeker = {'firstName':'Ted',
                           'lastName':'Testable',
                           'password':'testerted',
                           'is_seeker':True,
                           'UID':['tetest0001s'],
                           'email':'tester@jobapps.org',
                           'skills':"['Systems Testing', 'Network Security', 'Data Science', 'Python']"}
            demo_recruiter = {'firstName':'Rick',
                              'lastName':'Recruitable',
                              'password':'recruiterrick',
                              'is_seeker':False,
                              'UID':['rirecr0001r'],
                              'email':'recruiter@jobapps.org',
                              'skills':"['Recruiting', 'People Management']"}
            demo_admin = {'firstName':'Adam',
                              'lastName':'Administrator',
                              'password':'adminadam',
                              'is_seeker':False,
                              'UID':['adadmi0001a'],
                              'email':'admin@jobapps.org',
                              'skills':"['Database Management', 'System Controller Development']"}
            globAccountsDF = pd.concat([pd.DataFrame(demo_seeker), pd.DataFrame(demo_recruiter), pd.DataFrame(demo_admin)])
            globAccountsDF = globAccountsDF[['UID', 'firstName', 'lastName', 'email', 'password', 'is_seeker', 'skills']]
            globAccountsDF.to_csv("accounts_db.csv", index=False)
            print("\nAccounts database generated.")

        # If the job listing database is missing
        if "jobs_db.csv" not in local_files:
            demo_job = {'jobName':'Python Developer',
                        'jobCreatorUID':'rirecr0001r',
                        'jobType':'IT/Technology',
                        'jobSalary':'65000',
                        'jobUID':['IT000001'],
                        'jobAdvertised':True,
                        'jobKeyword':"['Python','Developer','Melbourne','Full-Time', 'ClosedDemo']",
                        'jobSkillset':"['Python', 'Full-Stack', 'Team Experience']",
                        'applicants':"['tetest0001s', 'value0001s', 'tetest0002s']"}
            globJobsDF = pd.DataFrame(demo_job)
            globJobsDF = globJobsDF[['jobName','jobCreatorUID','jobType','jobSalary','jobUID','jobAdvertised','jobKeyword','jobSkillset','applicants']]
            globJobsDF.to_csv("jobs_db.csv", index=False)
            print("\nJobs database generated.")

        # If the job categories database is missing
        if "job_categories.csv" not in local_files:
            demo_job_cats = {'jobCategories':['IT/Technology', 'Finance/Banking', 'Hospitality', 'Construction',
                                              'Healthcare', 'Education', 'Agriculture', 'Other Service Industry',
                                              'Communications / PR', 'Accounting', 'Legal Profession',
                                              'Other Professional Services']}
            globJobCatDF = pd.Series(demo_job_cats)
            globJobCatDF.to_csv("job_categories.csv", index=False)
            print("\nJob Categories database generated.")

        # If the Job Documentation Dataframe is missing
        if "job_documents.csv" not in local_files:
            demo_documentation = {'jobID':['IT000001'],
                                 'seekerID':'tetest0001s',
                                 'documentsUploaded':"['Ted_resume.docx', 'Ted_CoverLetter.docx']"}
            globDocumentationDF = pd.DataFrame(demo_documentation, index=[0])
            globDocumentationDF = globDocumentationDF[['jobID', 'seekerID', 'documentsUploaded']]
            globDocumentationDF.to_csv("job_documents.csv", index=False)
            print("\nJob Documentation database generated.")

        # If the job invitation dataframe is missing
        if "job_invitation.csv" not in local_files:
            demo_invitation = {'recruiterUID':'rirecr0001r',
                              'seekerUID':'tetest0001s',
                               'jobUID':['IT000001'],
                              'location':'123 Main Street, Melbourne VIC 3000',
                              'time':'12:65pm, 31/02/2019',
                              'accepted':True}
            globInvitationDF = pd.DataFrame(demo_invitation, index=[0])
            globInvitationDF = globInvitationDF[['recruiterUID', 'seekerUID','jobUID', 'location', 'time', 'accepted']]
            globInvitationDF.to_csv("job_invitation.csv", index=False)
            print("\nJob Invitation database generated.")

        # Global variables
        globUID = ''
        globRecommendedCategories = []

        # Setting database links
        globAccountsDF = pd.read_csv("accounts_db.csv")
        globJobsDF = pd.read_csv("jobs_db.csv")
        globJobCatDF = pd.read_csv("job_categories.csv", squeeze=True)
        globDocumentationDF = pd.read_csv("job_documents.csv")
        globInvitationDF = pd.read_csv("job_invitation.csv")
    
    # Initialises the data, and then begins running the OJSS platform via Menu.splash_menu()
    def start_ojss():
        UI.initialise()
        Menu.splash_menu()
    
    # Calls Menu.splash_menu
    def run():
        Menu.splash_menu()


# # System Controller
# #### Controller Class

# In[ ]:


# Defining SystemController class
class SystemController:
    # Logs users into the system
    def login(attempts = 0):
        global globUID
        if attempts > 3:
            print("\nYou've attempted to login unsuccessfully too many times, please create a new account.")
            return Account().create_account()
        else:
            login_email = input("Please provide your email address, or type EXIT (in all caps) to exit the program.")
            # If email is detected
            if len(globAccountsDF[(globAccountsDF.email == login_email)]) != 0:
                pword = input("Please enter your password.")
                if pword == "".join(globAccountsDF.password[globAccountsDF.email == login_email].tolist()):
                    globUID = "".join(globAccountsDF.UID[(globAccountsDF.email == login_email)].tolist())
                    print("\nSuccessfully logged in!")
                    attempts = 0
                    return Menu.main_menu()
                else:
                    print("\nPassword incorrect, attempting to login again.")
                    return SystemController.login(attempts+1)
            # Exit statement
            elif login_email == "EXIT":
                raise SystemExit
            # Handle missing/incorrect email. Offer retry (limited attempts) or generate account.
            else:
                print("\nEmail not detected. Enter 1 to retry, or anything else to create an account.")
                state = input()
                if state == "1":
                    SystemController.login(attempts+1)
                else:
                    Account().gen_account()
    
    # Logs users out.
    def logout():
        global globUID
        globUID = ''
        print("\nLogged out. Please login to continue.")
        return Menu.splash_menu()   
    
    # Matches job seekers to jobs, based on their skills.
    def matching_scores():
        if globUID == '':
            return SystemController.login()
        userUID = globUID
        # If the requester is a job seeker
        match_term_count = 0
        score = 0
        if userUID[-1] == 's':
            # If no jobs are available to apply for
            state = True
            if len(globJobsDF[globJobsDF.jobAdvertised == True]) == 0:
                print("\nWARNING:\nNo jobs are currently available to apply for, so we've returned you to the main menu. Please try later!\n")
                state = False
            if state is False:
                return Menu.main_menu()
            
            # Display the list of available industries / job types. Ensures the industry selection is correct.
            print(globJobsDF.jobType.unique().tolist())
            industry = input("Please enter the industry that you're interesting in having us match you with.")
            if industry not in globJobsDF.jobType.unique().tolist():
                return SystemController.matching_scores()
            else:
                pass
            
            # Display their skills and keywords chosen at account creation
            try:
                skills = ast.literal_eval(globAccountsDF.skills[globAccountsDF.UID == globUID][0])
            except (KeyError, ValueError):
                skills = ast.literal_eval(globAccountsDF.skills[globAccountsDF.UID == globUID].tolist()[0])
                        
            # Build the best possible score, based on the values provide by the user.
            iterscore = ['No Match', 0]
            # Build a new dataframe with only the jobs that can be applied for in the dataframe, where the user has not already applied for that job.
            relevant_jobs = globJobsDF[(globJobsDF.jobAdvertised == True)
                                       & (globJobsDF.jobType == industry)
                                       & (globJobsDF.applicants.str.contains(userUID)==False)].reset_index(drop=True)
            if len(relevant_jobs) == 0:
                print("Your best-match job cannot be identified, and it appears you've applied for all available jobs.")
                return Menu.main_menu()
            # Iterate through the new dataframe
            for job in range(0,len(relevant_jobs)):
                count = 0
                jobskills_ = relevant_jobs.jobSkillset[relevant_jobs.index == job][0]
                for term in skills:
                    if term in jobskills_:
                        count += 1
                score = count / len(jobskills_)
                if score > iterscore[1]:
                    iterscore[1] = score
                    iterscore[0] = relevant_jobs.jobUID[relevant_jobs.index == job][0]
                else:
                    pass
            if iterscore[1] > 0:
                print("\nYour optimal job can be found by applying for job UID", iterscore[0])
                display(globJobsDF[[i for i in globJobsDF.columns.tolist() if i != "applicants"]][globJobsDF.jobUID == iterscore[0]])
                return JobSeekerController.job_apply()
            else:
                print("\nSorry, we couldn't identify a job to recommend based on the details you provided. Please try again some other time!")
                return Menu.main_menu()
        
        # If the requester cannot be identified
        else:
            print("\nThere's an issue with your account - please login again after we've logged you out.")
            SystemController.logout()
    
    # Pointer to Account().update_skills
    def update_skills():
        return Account().update_skills()
    
    def create_job():
        return Job().create_job()
    
    def gen_account():
        return Account.gen_account()


# # System Administrator Controller
# #### Controller Class

# In[ ]:


class SystemAdministrator:
    def update_categories():
        if globUID[-1] == 'a': # Check that the logged-in user is an administrator
            global globJobCatDF
            global globRecommendedCategories
            if len(globRecommendedCategories) > 0:
                print("\nThe following job categories have been requested by job recruiters.")
                print(globRecommendedCategories)
            values = input("Input the new job categories, indicating the start and finish of each category with a comma").split(",")
            cats = [i.strip() for i in globJobCatDF.name[2:-2].replace("'", "").split(",")]
            update = [i.strip() for i in values] + cats
            values = pd.Series({"Job Categories":set(update)})
            globJobCatDF = values
            globJobCatDF.to_csv("job_categories.csv", index=False)
            globJobCatDF = pd.read_csv("job_categories.csv", squeeze=True)
            globRecommendedCategories = []
            return "Job categories successfully updated, and category request store has been wiped."
        else:
            print("\nYou don't have permission to do that. Please logout, and log back in with an admin account.")
            return SystemController.logout()
        


# # Account
# #### Entity Class

# In[ ]:


class Account:
    def __init__(self):
        self.data = []
        
    def gen_account(self):
        global globAccountsDF
        self.first = input("What is your first name? ")
        self.last = input("What is your surname? ")
        self.email =  input("What is your email address?")
        if len(globAccountsDF[(globAccountsDF.email == self.email)]) != 0:
            print("\n\nWARNING: An account with the email is recorded in the system - please login, or contact us on [GENERIC_EMAIL] if you"+
                  " have forgotten your password.")
            return Menu.splash_menu()
        else:
            pass
        check_state = False
        while check_state == False:
            self.password = input("Please type your password: ")
            self.pass_check = input("Please type your password again to confirm: ")
            if self.password == self.pass_check:
                check_state = True
            else:
                print("\nPasswords did not match; please try again.")

        # Set seeker status
        self.is_seeker = Account.seeker()        
        
        # Generate unique ID
        self.id_string = self.first.lower()[0:2] + self.last.lower()[0:4]
        if len(self.id_string) < 6:
            self.id_string += (6-len(self.id_string))*'x'
        # Counts the occurence count of the user ID, add one, and use this for numbering.
        self.id_string += (str(len(globAccountsDF[globAccountsDF.UID.str.contains(self.id_string)])+1).zfill(4))

        # 's'/'r' seeker/recruiter substring
        if self.is_seeker:
            self.id_string += ('s')
        else:
            self.id_string += ('r')
        
        # Filling in skills
        self.new_skills = input("Please enter any skills you wish to add to your account, separating each with a comma.").split(',')
        
        print("\nAll details are approved for submission.")
        
        self.details = {'firstName':self.first,
                        'lastName':self.last,
                        'password':self.password,
                        'is_seeker':self.is_seeker,
                        'UID':self.id_string,
                        'email':self.email,
                        'skills':str(self.new_skills)}

        globAccountsDF.loc[len(globAccountsDF)] = self.details
        globAccountsDF.to_csv("accounts_db.csv", index=False)
        print("\nNew account created!")
        return Menu.splash_menu()
    
    # Check seeker status
    def seeker():
        is_seeker = input("Are you a jobseeker? If so, please type True. If not, please type False. ")
        if is_seeker.lower() == 'true':
            is_seeker = True
        elif is_seeker.lower() == 'false':
            is_seeker = False
        else: # Recursive request if not True/False
            print("\nNot a recognised input; please try again.")
            is_seeker = Account.seeker()
        return is_seeker
    
    def update_account(self, uid = globUID):
        global globAccountsDF
        state = False
        while state == False:
            state = input("What would you like to update? \n1. Email address\n2. Password\n3. Skills\n4. Exit\nEnter the relevant number.")
            if state == "4":
                state = True
            else:
                if state == "1":
                    self.newemail = input("Pleases enter your new email.")
                    self.emailcheck = input("Please re-enter your new email.")
                    if self.newemail == self.emailcheck:
                        globAccountsDF['email'][globAccountsDF.UID == uid] = self.newemail
                        globAccountsDF.to_csv("accounts_db.csv", index=False)
                        return "Email updated."
                    else:
                        print("\nEmails entered did not match, please try again.")
                        return Account().update_account()
                elif state == "2":
                    return "Function not yet available."
                elif state == "3":
                    return Account().update_skills()
        
    # Prompt users to provide their skill sets.
    def update_skills(self):
        global globAccountsDF
        userUID = globUID
        # Pull existing skillset if it is not empty, otherwise use an empty list
        if not globAccountsDF.skills[globAccountsDF.UID == globUID].tolist() == ['[]']:
            try:
                self.current_skills = ast.literal_eval(globAccountsDF.skills[globAccountsDF.UID == userUID][0])
                #print("Option 1")
            except KeyError:
                self.current_skills = ast.literal_eval(str(globAccountsDF.skills[globAccountsDF.UID == userUID].tolist())[2:-2])
                #print("Option 2")
            print("Your existing skills are listed as;", self.current_skills)
        else:
            self.current_skills = []
        state = 'hgfghfj'
        while state.lower() not in ['true', 'false']:
            state = input("Do you wish to add to your current skills, or replace them entirely? Please enter either TRUE (to append) or FALSE (to rewrite).")
        # Receive new skills from user, append to list and then turn list to string.
        provision = input("Please provide your skills, separating each skillset by a comma.").split(',')
        self.new_skills = [i.strip() for i in list(provision)]
        # Write to dataframe, and save CSV
        if state.lower() == "false":
            globAccountsDF['skills'][globAccountsDF.UID == globUID] = str(list(self.new_skills))
        else:
            globAccountsDF['skills'][globAccountsDF.UID == globUID] = str(list(set(self.current_skills + self.new_skills)))
        print("Updated values")
        globAccountsDF.to_csv("accounts_db.csv", index=False)
        print("Skills updated.")
        return Menu.main_menu()    


# # Job
# #### Entity Class

# In[ ]:


class Job:
    def __init__(self):
        self.data = []
        
    # Generate a new job. 'job' argument exists for handling incorrect inputs.
    def create_job(self, job=""):
        global globJobsDF
        if job == "":
            self.job_name = input("Please provide name of job.")
        else:
            self.job_name = job
        
        # Return all available job categories
        job_cats = ast.literal_eval(globJobCatDF.name)
        print(job_cats)
        self.job_type = input("Please enter the relevant category from the list above, or type EXIT to leave.")
        if self.job_type in job_cats:
            pass
        elif self.job_type.lower() == "exit":
            return Menu.main_menu()
        else:
            print("\nInput not recognised, please try again.")
            return Job().create_job(job=self.job_name)
        
        # Input details, store in dict, then append to end of jobs dataframe
        print("\nEntering EXIT in any of the following states will return you to the menu once all inputs are taken.")
        self.job_salary = 'a'
        while not self.job_salary.replace(',', '').isnumeric():
            self.job_salary = input("Please provide the salary of the job (in whole dollars per annum).")
        self.job_keyword = input("Please provide job keywords, separating each keyword by a comma.").split(',')
        self.job_skillsets = input("Please provide job skillsets, separating each skillset by a comma.").split(',')
        self.job_id = self.job_type[:2] + str(len(globJobsDF[globJobsDF.jobUID.str.contains(self.job_type[:2])])+1).zfill(6)
        
        # Check for exit requests.
        for i in [self.job_salary, self.job_keyword, self.job_skillsets]:
            if type(i) == str:
                if i.lower() == 'exit':
                    return Menu.main_menu()
        
        self.details = {'jobName':self.job_name,
                        'jobCreatorUID':globUID,
                        'jobType':self.job_type,
                        'jobSalary':self.job_salary,
                        'jobUID':self.job_id,
                        'jobAdvertised':False,
                        'jobKeyword':str(self.job_keyword),
                        'jobSkillset':str(self.job_skillsets),
                        'applicants':'[]'}
        
        # Save to the CSV database
        globJobsDF.loc[len(globJobsDF)] = self.details
        globJobsDF.to_csv("accounts_db.csv", index=False)
        print("New job created successfully - don't forget to advertise this job.")
        return Menu.main_menu()
    


# # Job Recruiter
# #### Controller Class

# In[ ]:


class JobRecruiterController:
    # Display all jobs created by the logged-in recruiter
    def get_jobs():
        display(globJobsDF[globJobsDF.jobCreatorUID == globUID])
        return Menu.main_menu()
    
    # Return the applicant UIDs for applicants to a given (requested) job UID.
    def check_applicants():
        jobUID = input("Please enter the job UID for the job you wish to see applicants for, or enter MENU to return to the menu.")
        if jobUID.lower() == "menu":
            return Menu.main_menu()
        if jobUID not in globJobsDF.jobUID.unique().tolist():
            return JobRecruiterController.get_jobs()
        if len(globJobsDF.applicants[globJobsDF.jobUID == jobUID]) <= 2: #Indicates no job seekers
            print("\nNo applicants detected, please try with another job from the list below.")
            return JobRecruiterController.get_jobs()
        else:
            applicants = [i.strip() for i in globJobsDF["applicants"][(globJobsDF.jobCreatorUID == globUID) & (globJobsDF.jobUID == jobUID)][0].replace("[", "").replace("]", "").replace("'", "").split(",")]
    
    # Check the status of issued job interview invitations
    def check_invitations():
        display(globInvitationDF[globInvitationDF.recruiterUID == globUID])
        state = input("Enter TRUE if you wish to send invitations, otherwise enter anything else to return to the menu.")
        if state.lower() == 'true':
            return Invitations.issue_invitation()
        else:
            return Menu.main_menu()
            
    # Publish a job so it is available for job seekers to see
    def publish_job():
        print(JobRecruiterController.get_jobs())
        jobUID = input("Please enter the job UID for the job you wish to remove, or enter MENU to return to the menu.")
        if jobUID.lower() == "menu":
            return Menu.main_menu()
        if jobUID not in globJobsDF.jobUID.unique().tolist():
            return JobRecruiterController.get_jobs()
        else:
            globJobsDF.jobAdvertised[globJobsDF.jobUID == jobUID] = True
            globJobsDF.to_csv("jobs_db.csv", index=False)
            return "Job successfully advertised."
        
    # Request a new job category is added to the list of available options.
    def request_category():
        global globRecommendedCategories
        categories = input("Please enter your requested job categories, separating each with a comma.").split(",")
        globRecommendedCategories += categories
        return "Categories request has been sent!"
        
    # "Remove" a job by setting its advertise status to False, i.e. it will no longer show in job searches.
    def remove_job():
        jobUID = input("Please enter the job UID for the job you wish to remove, or enter MENU to return to the menu.")
        if jobUID.lower() == "menu":
            return Menu.main_menu()
        if jobUID not in globJobsDF.jobUID.unique().tolist():
            return JobRecruiterController.get_jobs()
        else:
            globJobsDF.jobAdvertised[globJobsDF.jobUID == jobUID] = False
            globJobsDF.to_csv("jobs_db.csv", index=False)
            return "Job successfully delisted."


# # Job Seeker
# #### Controller Class

# In[ ]:


class JobSeekerController:
    # Allow jobseekers to search for a job based on their skills.
    def job_search():
        userUID = globUID
        print(ast.literal_eval(globJobCatDF.name))
        jobtype = input("Provide the job type you would like to search for, from the list above.")
        
        # If no jobs exist for that category;
        curr_jobs = globJobsDF.jobType.unique().tolist()
        if jobtype not in curr_jobs:
            print("\nSorry, we don't have any jobs for that job category.")
            print("\nWe currently have jobs available in the following sectors;")
            print(curr_jobs)
            return JobSeekerController.job_search()
        
        userskills = ast.literal_eval(globAccountsDF.skills[globAccountsDF.UID==globUID].tolist()[0])
        if type(userskills[0]) == list:
            userskills = flatten(userskills)
        print(userskills)
        
        jobskills = '2189gdnsgi1099' # Nonsense string
        while jobskills not in userskills:
            jobskills = input("Provide which primary skill you would like to search with, from your skillset listed above. Note that only one skill can be selected. To leave, please enter EXIT.").split(",")[0]
            if jobskills.lower() == 'exit':
                return Menu.main_menu()
        # Pull available jobs. Second catch for whether jobs are available.
        jobs_avail = globJobsDF[[i for i in globJobsDF if i != 'applicants']][(globJobsDF.jobType == jobtype) & (globJobsDF.jobSkillset.str.contains(jobskills)) & (globJobsDF.applicants.str.contains(userUID)==False)]
        if len(jobs_avail) == 0:
            print("\nNo jobs available, based on your search terms. Returning you to the menu now.")
            return Menu.main_menu()
        else:
            display(jobs_avail)
            state = '2189gdnsgi1099' # Nonsense string
            while state.lower() not in ["apply", "exit"]:
                state = input("To apply for any of these jobs, please enter APPLY, or enter EXIT to return to the menu.")
                if state.lower() == "exit":
                    return Menu.main_menu()
                elif state.lower() == "apply":
                    JobSeekerController.job_apply()
                    
    def industry_search():
        userUID = globUID
        print(ast.literal_eval(globJobCatDF.name))
        jobtype = input("Provide the job type you would like to search for, from the list above.")
        
        # If no jobs exist for that category;
        curr_jobs = globJobsDF.jobType.unique().tolist()
        if jobtype not in curr_jobs:
            print("\nSorry, we don't have any jobs for that job category.")
            print("\nWe currently have jobs available in the following sectors;")
            print(curr_jobs)
            return JobSeekerController.industry_search()
        
        # Pull available jobs. Second catch for whether jobs are available.
        jobs_avail = globJobsDF[[i for i in globJobsDF if i != 'applicants']][(globJobsDF.jobType == jobtype) & (globJobsDF.applicants.str.contains(userUID)==False) & (globJobsDF.jobAdvertised == True)]
        if len(jobs_avail) == 0:
            print("\nYou've applied for all available jobs in the industry. Returning you to the menu now.")
            return Menu.main_menu()
        
        # Ask whether the searcher wants to apply to any of the jobs.
        state = '2189gdnsgi1099'
        while state.lower() not in ['true', 'false']:
            state = input("Please enter TRUE to apply for one of these jobs, otherwise enter EXIT to return to the menu.")
        if state.lower() == 'true':
            return JobSeekerController.job_apply()
        else:
            return Menu.main_menu()
    
    # Apply for jobs. Requires job seeker knows the job UID.
    def job_apply():
        global globJobsDF
        jobapply = input("Please provide the job UID that you wish to apply for.")
        if jobapply not in globJobsDF.jobUID.unique().tolist():
            state = ("Job ID not detected. Enter RETRY to attempt again, SEARCH to search for jobs, or EXIT to return to the menu.")
            if state.lower() == "retry":
                JobSeekerController.job_apply()
            elif state.lower() == "search":
                JobSeekerController.job_search()
            else:
                Menu.main_menu()
        else:
            target_applicants = ast.literal_eval(globJobsDF.applicants[globJobsDF.jobUID == jobapply][0])
            if globUID in target_applicants:
                print("You've already applied for that job, please try again.")
                return Menu.main_menu()
            else:
                globJobsDF.applicants[globJobsDF.jobUID == jobapply] = str(target_applicants + [globUID])
                globJobsDF.to_csv("jobs_db.csv", index=False)
                print("You've successfully applied to your selected job.")
        return Menu.main_menu()
    
    # Check jobs that the seeker has applied for
    def job_check():
        applied_jobs = globJobsDF[[i for i in globJobsDF.columns.tolist() if i != 'applicants']][globJobsDF.applicants.str.contains(globUID)]
        if len(applied_jobs) > 0:
            display(globJobsDF[[i for i in globJobsDF.columns.tolist() if i != 'applicants']][globJobsDF.applicants.str.contains(globUID)])
        else:
            print("\nYou haven't applied for any jobs!")
        return Menu.main_menu()
    
    # Check for any interview requests that have been sent
    def invitation_check():
        invites = globInvitationDF[(globInvitationDF.seekerUID == globUID) & (globInvitationDF.accepted == False)]
        accepted = globInvitationDF[(globInvitationDF.seekerUID == globUID) & (globInvitationDF.accepted == True)]
        if len(invites) > 0:
            print("\n/nHere are the interview invitations requests waiting for your approval.")
            display(invites)
            if input("Please enter YES if you wish to accept/reject any of these invitations.").lower() == 'yes':
                return Invitations.accept_invitation()
            else:
                return globInvitationDF[globInvitationDF.seekerUID == globUID]
        else:
            if len(accepted) > 0:
                print("\nHere are the interview invitations which you have accepted.")
                display(accepted)
                return "You've accepted all interview invitations sent to you."
            else:
                return "No interview invitations are recorded for your account."


# In[ ]:


#globUID = 'tetest0001s'
#JobSeekerController.job_search()


# # Documentation
# #### Entity Class

# In[ ]:


class Documentation:
    def __init__(self):
        self.documents = {}
        
    def get_doc(self, job_id, seeker_id):
        self.doc_name = input("Please insert all file names including extenstions, seperated by a comma.").split(',')
        self.doc_name = [i.strip() for i in self.doc_name]
        details = {'jobID': job_id,
                  'seekerID': seeker_id,
                  'documentsUploaded': str(self.doc_name)}
        globDocumentationDF.loc[len(df)] = details
        globDocumentationDF.to_csv("accounts_db.csv", index=False)
        return "Documents uploaded"


# # Menus
# #### Boundary Class

# In[ ]:


class Menu:
    # Catchall menu; uses UID identifying character to determine which menu to show.
    def main_menu():
        global globUID
        UID = globUID
        if UID[-1] == 's':
            Menu.seeker_menu()
        elif UID[-1] == 'r':
            Menu.recruiter_menu()
        elif UID[-1] == 'a':
            Menu.admin_menu()
        else:
            print("\nUID not recognised.")
            globUID = ''
            Menu.splash_menu()
    
    # Only accessible by job seekers.
    def seeker_menu():
        print("\nAvailable Options:\n"+
              "1. Update Skills\n"+
              "2. Search for Jobs\n"+
              "3. See Current Interview Invitations\n"+
              "4. See Current Job Applications\n"+
              "5. Run a generalised job search\n"+
              "6. Run our recommendation platform's job suggester\n"+
              "7. Exit")
        request = input("Please select the number option that you wish to proceed with.")
        if request == '1':
            SystemController.update_skills()
        elif request == '2':
            JobSeekerController.job_search()
        elif request == '3':
            JobSeekerController.invitation_check()
        elif request == '4':
            JobSeekerController.job_check()
        elif request == '5':
            JobSeekerController.industry_search()
        elif request == '6':
            SystemController.matching_scores()
        elif request == '7':
            SystemController.logout()
            return
        else:
            print("\nInput not recognised.")
            return Menu.seeker_menu()
    
    # Only accessible by recruiters.
    def recruiter_menu():
        print("\nAvailable Options:\n"+
              "1. Create Job\n"+
              "2. Publish Job\n"+
              "3. Remove Job\n"+
              "4. View Job Applicants\n"+
              "5. Check and Send Interview Invitations\n"+
              "6. Suggest Job Category\n"+
              "7. Check current job listings\n"+
              "8. Exit")
        request = input("Please select the number option you wish to proceed with.")
        if request == '1':
            SystemController.create_job()
        elif request == '2':
            JobRecruiterController.publish_job()
        elif request == '3':
            JobRecruiterController.delete_job()
        elif request == '4':
            JobRecruiterController.check_applicants()
        elif request == '5':
            JobRecruiterController.check_invitations()
        elif request == '6':
            JobRecruiterController.request_category()
        elif request == '7':
            JobRecruiterController.get_jobs()
        elif request == '8':
            SystemController.logout()
        else:
            print("\nInput not recogcnised.")
            return Menu.recruiter_menu()
    
    # Only accessible by admins.
    def admin_menu():
        print("\nAvailable Options:\n"+
             "1. Create Job Category:\n"+ 
             "2. Exit")
        request = input("Please select the number option you wish to proceed with.")
        if request == '1':
            SystemAdministrator.update_categories()
        elif request == '2':
            SystemController.logout()
        else:
            print("\nInput not recognised.")
            return Menu.admin_menu()
    
    # First menu people come across, or if their UID identifying character is corrupted.
    def splash_menu():
        print("\nDo you wish to log in, start a new account, or close the program?")
        request = input("Please enter either LOGIN, NEW, or EXIT.")
        if request.lower() == "login":
            SystemController.login()
        elif request.lower() == "new":
            SystemController.gen_account()
        elif request.lower() == 'exit':
            raise SystemExit
        else:
            Menu.splash_menu()


# # Invitations
# #### Entity Class

# In[ ]:


class Invitations:
    def __init__(self):
        self.data = []
        
    def issue_invitation():
        self.jobUID = input("Please provide the job UID for which you wish to send interview requests to applicants.")
        jobselection = globJobsDF.applicants[globJobsDF.jobUID == self.jobUID].tolist()
        print(jobselection)
        self.applicant = input("Please input the applicant UID that you wish to apply for.")
        if self.applicant not in jobselection:
            print("\nApplicant ID not recognised, please try again.")
            return Menu.main_menu()
        else:
            pass
        self.location = input("Please provide the address you wish to have the interview at.")
        self.time = input("Please provide the time that you wish to meet the applicant.")
        
    def accept_invitation():
        self.jobUID = input("Please enter the job UID you wish to respond to an invitation for.")
        if self.jobUID in globInvitationDF.jobUID[globInvitationDF.seekerID == globUID].unique.tolist():
            pass
        else:
            print("\nYou're not able to respond to interview requests for that job.")
            return Invitations().accept_invitation()
        state = input("Do you wish to accept the invitation? Please enter YES (to accept) or NO (to turn down).")
        if state.lower == "true":
            globInvitationDF.accepted[(globInvitationDF.seekerID == globUID) & (globInvitationDF.jobID)] = True
            globInvitationDF.to_csv("job_invitation.csv", index=False)
            return "Invitation successfully applied for."
        elif state.lower == "false":
            globInvitationDF.accepted[(globInvitationDF.seekerID == globUID) & (globInvitationDF.jobID)] = False
            globInvitationDF.to_csv("job_invitation.csv", index=False)
            return "Invitation successfully turned down."
        else:
            return Invitations().accept_invitation()


# # Testing
# 
# Running this section will call the UI.initialise() method to generate and setup the databases (if this is your first time running the program), or otherwise will proceed to setting up the databases if their root CSV files are already present in the working directory.
# 
# It then calls UI.run() to begin the login / account creation process.

# In[ ]:


UI.initialise()


# In[ ]:


UI.run()

