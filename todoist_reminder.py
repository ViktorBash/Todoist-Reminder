"""
Todoist Gmail Reminder
"""

import todoist
import os
import random
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

API_KEY = str(os.environ.get("Todoist_API_Key"))


# Function which will get three random items from Todoist (also works if Todoist has less than 3 tasks added)
def get_three_items():
    # Connect to the API with an API key
    api = todoist.TodoistAPI(API_KEY)
    api.sync()

    # Get items from the API
    items = api.items.all()

    # Use a list comprehension to store the title of each item in a list
    items_list = [item['content'] for item in items]
    # items_list = [items_list[1]]

    three_items = []

    if len(items_list) > 3:  # If there are 3 or less items we will return those items instead of getting random ones
        while len(three_items) < 3:  # While the random 3 items is not filled up, get more random items
            random_item = random.choice(items_list)
            if random_item not in three_items:
                three_items.append(random_item)
    else:  # We have 3 or less items already, so just add them
        three_items = items_list
    return three_items


# Here we send the email with smtplib

sender = "youremail@gmail.com"
receiver = "youremail@gmail.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "3 Todoist Items Reminder - Pick One"
msg['From'] = sender
msg['To'] = receiver

three_items = get_three_items()

# Create the body of the message (a plain-text and an HTML version).
text = f"Here are your 3 items:" \
       f"Task 1: {three_items[0] if len(three_items) > 0 else 'NA'}" \
       f"Task 2: {three_items[1] if len(three_items) > 1 else 'NA'}" \
       f"Task 3: {three_items[2] if len(three_items) > 2 else 'NA'}" \

html = f"""\
<html>
  <head></head>
  <body>
  <p style="font-size:18px; font-family:Tahoma, sans-serif;">Here are your 3 items:</p>
    <h3>Task 1: {three_items[0] if len(three_items) > 0 else "NA"}</h3>
    <h3>Task 2: {three_items[1] if len(three_items) > 1 else "NA"}</h3>
    <h3>Task 3: {three_items[2] if len(three_items) > 2 else "NA"}</h3>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
# Send the message via local SMTP server.
mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login('youremail@gmail.com', str(os.environ.get("Todoist_Reminder_Gmail")))
mail.sendmail(sender, receiver, msg.as_string())
mail.quit()
