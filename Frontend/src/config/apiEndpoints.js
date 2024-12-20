const urlPrefix = {
    // account: "/api/account",
    auth: "/api/auth",
    admin: "/api/admin",
    contact: "/api/contact",
}

const adminUrl = {
    dash: `${urlPrefix.admin}/dash`,
    messageAction: `${urlPrefix.admin}/message_action`,
    messages: `${urlPrefix.admin}/messages`,
    userAction: `${urlPrefix.admin}/user_action`,
    users: `${urlPrefix.admin}/users`,
}

export const apiEndpoints = {
    baseURL: "https://127.0.0.1:5000",
    //contact
    contactUs: `${urlPrefix.contact}/contact_form`, //OK
    //authentication -- profile
    //...
    //authentication -- recovery
    setRecoveryEmail: `${urlPrefix.auth}/set_recovery_email`, //OK
    // authentication -- registration
    // ...
    //authentication -- session
    getOTP: `${urlPrefix.auth}/get_otp`, //OK
    //authentication -- main
    userSignUp: `${urlPrefix.auth}/signup`, //OK
    userLogIn: `${urlPrefix.auth}/login`, //OK (test mfa)
    userLogOut: `${urlPrefix.auth}/logout`, //OK
    userGetOwnAcctInfo: `${urlPrefix.auth}/@me`, //OK
    //authentication -- account
    acctRequestVerifyEmail: `${urlPrefix.auth}/request_email_verification`, //OK
    acctVerifyEmail: `${urlPrefix.auth}/verify_acct_email`, //OK
    acctChangeName: `${urlPrefix.auth}/change_user_name`, //OK
    acctChangeEmail: `${urlPrefix.auth}/request_auth_change`, //--test
    acctChangeTokenVerify: `${urlPrefix.auth}/request_token_validation`, //--working on for email (password uses same route)
    acctChangePassword: `${urlPrefix.auth}/...`, //MISSING 2-step
    acctDeleteOwnAccount: `${urlPrefix.auth}/delete`, //MISSING
    //admin - dashboard
    adminGetDashboardData: `${adminUrl.dash}/admin_dash`, //MISSING
    //admin - users
    adminGetUsersTable: `${adminUrl.users}/table`, //OK
    adminGetUserInfo: `${adminUrl.users}/user_info`, //OK
    adminGetUserLogs: `${adminUrl.users}/user_logs`, //OK
    adminGetUserMessages: `${adminUrl.users}/user_messages`, //OK
    //admin - user action
    adminChangeUserFlag: `${adminUrl.userAction}/flag_change`,//OK
    adminChangeUserAccessType: `${adminUrl.userAction}/access_change`,//OK
    adminBlockUnblockUser: `${adminUrl.userAction}/block_unblock`,//OK
    adminDeleteUser: `${adminUrl.userAction}/delete_user`, //OK
    //admin - messages
    adminMessagesTable: `${adminUrl.messages}/table`, // OK ? (check filter and pagination)
    adminMessageMarkAs: `${adminUrl.messageAction}/mark_as`, //OK 
    adminMessageAnswer: `${adminUrl.messageAction}/answer_message`, //OK
    adminMessageFlagChange: `${adminUrl.messageAction}/flag_change`, //OK
    adminMessageDelete: `${adminUrl.messageAction}/delete_message`, //MISSING
};

export default apiEndpoints;