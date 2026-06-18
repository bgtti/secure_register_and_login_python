"""
Defines the length of time before expiry of an OTP, security code, and of the MFA total process.

Currently used in the User db model and auth-related services.
"""
# Define length of time (in minutes) that the OTP should be valid.
OTP_VALIDITY_MINUTES = 30 
"""OTP valid for: 30 minutes"""

# Define length of time (in minutes) that the OTP should be valid.
SECURITY_CODE_VALIDITY_MINUTES = 30 
"""Security code valid for: 30 minutes"""


#TODO:check if needed!!!
# Define max length of time (in minutes) allowed for user to complete MFA process (ie: input of password and OTP)
MFA_VALIDITY_MINUTES = 30
"""MFA must be completed within: 30 minutes""" 