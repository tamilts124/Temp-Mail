# Free Temp Mail ID Generator

This repository provides a Python script to generate temporary email IDs using Temp-Mail.org, manage them, and view the received emails. The entire process is designed to be quick and efficient.

## Features

- **Instant Email ID Creation:** Generate temporary email IDs within seconds.
- **Manage Multiple IDs:** Easily create, delete, and view emails for multiple temporary mail IDs.
- **Email Viewing:** Fetch and view email content, including links, directly from the terminal.
- **Offline Access:** Stores email data locally for offline viewing.
- **HTML Email Support:** Open email content in the browser for better readability.

## How It Works

The script interacts with Temp-Mail.org's API to:
- Generate temporary email addresses.
- Fetch emails for generated addresses.
- Parse and display email content (text and links).
- Save and manage email data locally using Python's `pickle` module.

## File Structure

The repository consists of a single Python file:

- `TempMail.py`: Contains all the functionality for creating and managing temporary mail IDs.

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/tamilts124/Temp-Mail.git
   cd Temp-Mail
   ```

2. **Install Dependencies:**
   Ensure you have the required Python libraries installed. These are used in the script:
   - `requests`
   - `beautifulsoup4`

   Install them using pip:
   ```bash
   pip install requests beautifulsoup4
   ```

3. **Run the Script:**
   Execute the script directly:
   ```bash
   python TempMail.py
   ```

## Usage

### Main Menu

When you run the script, you will see the following options:

1. **Manage Mail IDs:**
   - Create new mail IDs.
   - View emails for a specific ID.
   - Delete unused IDs.
   - Add existing mail IDs using tokens.

2. **Offline Messages:**
   - View previously fetched messages stored locally.

3. **Save Status & Exit:**
   - Save the current state and exit the program.

### Managing Mail IDs
- **Create Mail IDs:**
  Specify the number of IDs to generate, and they will be created instantly.
- **View Emails:**
  List all received emails for a selected mail ID. View their content or open them in a browser.
- **Delete Mail IDs:**
  Select and remove unused mail IDs.
- **Add Mail ID by Token:**
  Add an existing Temp-Mail ID using its token.

### Viewing Emails
- Emails are displayed with details such as sender, subject, and preview.
- Choose an email to view its full content, including links.
- Open the email content in a browser if needed.

## Notes

- Ensure an active internet connection while using the script to interact with Temp-Mail.org's API.
- All data is stored locally in `TempMail.pkl` for offline access.
- The script is designed for ethical use only. Do not use it for spamming or malicious activities.

## Example Output

```plaintext
    Temp-Mail.org

01. Manage Mail IDs
02. Offline Messages
03. Save Status & Exit

 >> 1

      Manage Mail IDs

01. email1@temp-mail.org
02. email2@temp-mail.org

03. Create Mail IDs
04. Delete Mail IDs
05. Add Mail ID
06. Go Back

 >> 1

 > From: sender@example.com
   Subject: Welcome
   Preview: This is a test email.

 >>
```

## License

This project is licensed under the [MIT License](LICENSE).

