from dineqr.settings import DEFAULT_FROM_EMAIL
from .mail import ForgotPasswordOtpMail, ForgotPasswordSuccessfulMail, SendStaffInviteMail

class RestaurantController():
    
    def send_forgot_password_otp_email(email, name, otp):

        mail = ForgotPasswordOtpMail(
            context={
                "otp": otp,
                "name": name
            }
        )
        to_emails = [email, ]

        mail.send(to_emails, from_email=DEFAULT_FROM_EMAIL)


    def send_forgot_password_email_successful(email, name):

            mail = ForgotPasswordSuccessfulMail(
                context={
                    "name": name
                }
            )
            to_emails = [email, ]

            mail.send(to_emails, from_email=DEFAULT_FROM_EMAIL)


    def send_staff_invite_email(email, invite_link, res_name):

            mail = SendStaffInviteMail(
                context={
                    "invite_link": invite_link,
                    "organisation_name": res_name
                }
            )
            to_emails = [email, ]
            mail.send(to_emails, from_email=DEFAULT_FROM_EMAIL)

