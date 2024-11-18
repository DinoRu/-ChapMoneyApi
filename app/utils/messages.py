from dataclasses import dataclass


@dataclass
class Messages:
    USER_NOT_FOUND = "User with this email not found"
    USER_ALREADY_EXISTS = "User with this email already exists"
    USER_LOGOUT = "User logout"
    USER_CREATED = "User successfully created"

    INVALID_TOKEN = "Invalid token"

    PROFILE_DELETED = "User deleted"

    WRONG_PASSWORD = "Wrong password"
    WRONG_OLD_PASSWORD = "Wrong old password"
    PASSWORDS_NOT_MATCH = "Passwords don't match"
    PASSWORD_RESET = "Password reset"
    NEW_PASSWORD_SIMILAR_OLD = "New password is similar to old one"
    PASSWORD_UPDATED = "Password successfully updated"
    RESET_PASSWORD_MAIL_SENT = "Reset password mail sent"

    BALANCE_NOT_FOUND = "Balance not found"
    BALANCE_ALREADY_EXISTS = "Balance already exists"
    BALANCE_CREATED = "Balance successfully created"
    BALANCE_TOP_UP = "Balance top up"
    INSUFFICIENT_FUNDS = "Insufficient funds"
    BALANCE_WITHDRAW = "Balance withdraw"

    TRANSFER_SUCCESSFUL = "Transfer successful"

    ACCESS_DENIED = "Access denied"

    CURRENCY_NOT_FOUND = "Currency not found"
    CURRENCY_ALREADY_EXISTS = 'Currency already exists'
    CURRENCY_CREATED = "Currency created"
    CURRENCY_DELETED = "Currency was deleted"

    COUNTRY_NOT_FOUND = "Country not found"
    COUNTRY_ALREADY_EXISTS = 'Country already exists'
    COUNTRY_CREATED = "Country created"
    COUNTRY_DELETED = "Country was deleted"
    COUNTRY_UPDATED = "Country was updated"

    METHOD_NOT_FOUND = "Method not found"
    METHOD_ALREADY_EXISTS = 'Method already exists'
    METHOD_CREATED = "Method created"
    METHOD_DELETED = "Method was deleted"
    METHOD_UPDATED = "Method was updated"

    ACCOUNT_NOT_FOUND = "Account not found"
    ACCOUNT_ALREADY_EXISTS = 'Account already exists'
    ACCOUNT_CREATED = "Account created"
    ACCOUNT_DELETED = "Account was deleted"
    ACCOUNT_UPDATED = "Account was updated"


messages = Messages()