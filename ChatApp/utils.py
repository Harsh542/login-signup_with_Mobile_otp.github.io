from twilio.rest import Client

# Create your models here.


account_sid = 'AC6697aa51bc8b11f12c6e4e306877a206'
auth_token = '8e6ce924e078b86af01c70ec78c68718'
client = Client(account_sid, auth_token)


def send_otp(number, otp):
    message = client.messages.create(
        body=f'Hi there! your otp is - {otp}',
        from_='+17372154524',
        to=f'+91{number}'
    )
