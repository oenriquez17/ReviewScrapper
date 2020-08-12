import smtplib

def send_email():
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("in.amazon.reviews@gmail.com", "instanatural")

    # message to be sent
    message = "Testing sending email"

    # sending the mail
    s.sendmail("in.amazon.reviews@gmail.com", "in.amazon.reviews@gmail.com", message)

    print('Email sent to update lightning deal')

    # terminating the session
    s.quit()

    if __name__ == "__main__":
        send_email()