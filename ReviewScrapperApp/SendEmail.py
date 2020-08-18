import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import datetime


def send_email():
    send_from = 'in.amazon.reviews@gmail.com'
    send_to = 'reviewsandratings.b8407h@zapiermail.com'

    print('Sending...')
    msg = MIMEMultipart()
    msg['From'] = 'in.amazon.reviews@gmail.com'
    msg['To'] = 'in.amazon.reviews@gmail.com'
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Reviews & Ratings'
    current_date = datetime.datetime.now()
    body = ('%02d' % current_date.month) + '/' + ('%02d' % current_date.day) + '/' + str(current_date.year)
    ext = '_' + ('%02d' % current_date.month) + ('%02d' % current_date.day) + str(current_date.year)

    msg.attach(MIMEText(body))

    filename = 'RatingReviews' + ext + '.csv'

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filename, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="' + filename + '"')
    msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("in.amazon.reviews@gmail.com", "instanatural")
    s.sendmail(send_from, send_to, msg.as_string())
    print('Sent success')
    s.quit()


if __name__ == "__main__":
    print('Starting main')
    send_email()