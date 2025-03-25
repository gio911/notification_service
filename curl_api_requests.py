# curl -X 'POST' \
#   'http://localhost:8000/api/v1/notifications/send_mail' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "recipient": "centurion91186@gmail.com",
#   "subject": "Test Email",
#   "body": "This is a test email."
# }'