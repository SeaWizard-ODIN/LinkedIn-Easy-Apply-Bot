# LinkedIn Easy Apply Bot

Automate the application process on LinkedIn while you focus on more important things.

**Write-up:** [How to Apply for Jobs While You Are Sleeping](https://www.nicolomantini.com/p/how-to-apply-for-jobs-while-you-are-sleeping)  
**Video Tutorial:** [YouTube Demo](https://www.youtube.com/watch?v=4R4E304fEAs)

---

## 🚀 Setup Instructions

### ✅ **1. Install Python**

- Download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
- Ensure you check **“Add Python to PATH”** during installation.

### ✅ **2. Install Google Chrome**

- Download from [https://www.google.com/chrome/](https://www.google.com/chrome/).

---

### 💻 **For Windows Users**

1. Open **Command Prompt** (Press `Win + R`, type `cmd`, and press Enter).
2. Navigate to the bot’s folder. Example:

   cd C:\Users\YourName\Documents\LinkedIn-Easy-Apply-Bot

3. Install the required packages:

   pip install -r requirements.txt

4. Edit the `config.yaml` file and enter your LinkedIn login details, phone number, job positions, and locations:

```yaml
username: # Insert your username here
password: # Insert your password here
phone_number: #Insert your phone number

positions:
  -  # positions you want to search for
  -  # Another position you want to search for
  -  # A third position you want to search for

locations:
  -  # Location you want to search for
  -  # A second location you want to search in

salary: #yearly salary requirement
rate: #hourly rate requirement

uploads:
  Resume: # PATH TO Resume
  Cover Letter: # PATH TO cover letter
  Photo: # PATH TO photo
# Note file_key:file_paths contained inside the uploads section should be written without a dash ('-')

output_filename:
  -  # PATH TO OUTPUT FILE (default output.csv)

blacklist:
  -  # Company names you want to ignore
```

**NOTE: After editing and saving config.yaml, DO NOT upload or share it publicly, as it contains sensitive login information.**

### Uploads

You can add multiple files to the uploads section.
The bot tries to match uploaded files with the required fields during the application process.

## Execute the Boit

To execute the bot run the following in your terminal (Press `Win+R`, type `cmd`, and press Enter)

```
python easyapplybot.py
```

## Important Notes

- The bot applies only to jobs with the "Easy Apply" option.
- You can stop the bot anytime by pressing Ctrl + C in the terminal.
- Fine-tune config.yaml to improve application targeting and avoid applying for irrelevant jobs.
- Ensure your computer remains awake while the bot runs.
