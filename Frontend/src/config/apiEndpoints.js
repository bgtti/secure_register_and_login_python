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
    //AUTH
    //authentication -- credential change
    resetPasswordToken: `${urlPrefix.auth}/reset_password_token`, //OK
    changePassword: `${urlPrefix.auth}/change_password`, //OK
    changeEmail: `${urlPrefix.auth}/change_email`, //OK (test unvalidated account)
    changeEmailTokenVerification: `${urlPrefix.auth}/email_change_token_validation`, //OK
    //authentication -- profile
    acctChangeName: `${urlPrefix.auth}/change_user_name`, //OK
    //authentication -- recovery
    setRecoveryEmail: `${urlPrefix.auth}/set_recovery_email`, //OK
    getRecoveryEmailStatus: `${urlPrefix.auth}/get_recovery_status`, //OK
    getRecoveryEmail: `${urlPrefix.auth}/get_recovery_email`, //OK
    deleteRecoveryEmail: `${urlPrefix.auth}/delete_recovery_email`, //OK
    //authentication -- registration
    userSignUp: `${urlPrefix.auth}/signup`, //OK
    acctDeleteOwnAccount: `${urlPrefix.auth}/delete_user`, //OK
    //authentication -- session
    getOTP: `${urlPrefix.auth}/get_otp`, //OK
    userLogIn: `${urlPrefix.auth}/login`, //OK
    userLogOut: `${urlPrefix.auth}/logout`, //OK
    userGetOwnAcctInfo: `${urlPrefix.auth}/@me`, //OK
    //authentication -- security
    setMfa: `${urlPrefix.auth}/set_mfa`, //OK
    verifyAccount: `${urlPrefix.auth}/verify_account`, //OK
    //ADMIN
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
    //contact
    contactUs: `${urlPrefix.contact}/contact_form`, //OK
};

export default apiEndpoints;