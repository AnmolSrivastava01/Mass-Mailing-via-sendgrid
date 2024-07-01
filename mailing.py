import pandas as pd
import requests
import os

def send_email(api_key, from_email, to_email, subject, html_content):
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {"email": from_email},
        "content": [{"type": "text/html", "value": html_content}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 202:
        print(f"Email sent successfully to {to_email}")
    else:
        try:
            print(f"Failed to send email to {to_email}: {response.json()}")
        except requests.exceptions.JSONDecodeError:
            print(f"Failed to send email to {to_email}: {response.text}")

def load_html_template(category):
    template_folder = 'folder location'
    template_file = os.path.join(template_folder, f"{category}.html")
    
    with open(template_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return html_content

def main():
    # Replace with your actual SendGrid API key
    api_key = 'your key'
    from_email = 'example@try.com'
    csv_file = 'example.csv'
    
    # Load CSV data and clean up
    data = pd.read_csv(csv_file)
    
    # Strip leading and trailing spaces from column names
    data.columns = data.columns.str.strip()
    
    # Check if columns exist and drop NaN rows
    if 'email' in data.columns and 'category' in data.columns:
        data.dropna(subset=['email', 'category'], inplace=True)
    else:
        raise KeyError("Columns 'email' and/or 'category' not found in DataFrame.")
    
    data.reset_index(drop=True, inplace=True)

    # Print the DataFrame to check headers and data
    print(data.head())
    print(data.columns)

    for index, row in data.iterrows():
        to_email = row['email']
        category = row['category']
        subject = f"Your Special Offer for {category}"
        
        # Load HTML template based on category
        html_content = load_html_template(category)
        
        # Send email
        send_email(api_key, from_email, to_email, subject, html_content)

if __name__ == "__main__":
    main()
