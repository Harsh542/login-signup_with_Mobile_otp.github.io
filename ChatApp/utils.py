from twilio.rest import Client

# Create your models here.


account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


def send_otp(number, otp):
    message = client.messages.create(
        body=f'Hi there! your otp is - {otp}',
        from_='',
        to=f'+91{number}'
    )
