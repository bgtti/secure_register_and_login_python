const urlPrefix = {
    // account: "/api/account",
    auth: "/api/auth",
    admin: "/api/admin",
    contact: "/api/contact",
    userSettings: "/api/user_settings"
}

const adminUrl = {
    dash: `${urlPrefix.admin}/dash`,
    messageAction: `${urlPrefix.admin}/message_action`,
    messages: `${urlPrefix.admin}/messages`,
    userAction: `${urlPrefix.admin}/user_action`,
    users: `${urlPrefix.admin}/users`,
}

const authUrl = {
    credentialChange: `${urlPrefix.auth}/credential_change`,
    profile: `${urlPrefix.auth}/profile`,
    recovery: `${urlPrefix.auth}/recovery`,
    registration: `${urlPrefix.auth}/registration`,
    safety: `${urlPrefix.auth}/safety`,
    session: `${urlPrefix.auth}/session`,
}

export const apiEndpoints = {
    baseURL: "http://127.0.0.1:5000",
    //AUTH
    //authentication -- credential change
    resetPasswordToken: `${authUrl.credentialChange}/reset_password_token`, //OK
    changePassword: `${authUrl.credentialChange}/change_password`, //OK
    changeEmail: `${authUrl.credentialChange}/change_email`, //OK (test unvalidated account)
    changeEmailTokenVerification: `${authUrl.credentialChange}/email_change_token_validation`, //OK
    //authentication -- profile
    acctChangeName: `${authUrl.profile}/change_user_name`, //OK
    //authentication -- recovery
    setRecoveryEmail: `${authUrl.recovery}/set_recovery_email`, //OK
    getRecoveryEmailStatus: `${authUrl.recovery}/get_recovery_status`, //OK
    getRecoveryEmail: `${authUrl.recovery}/get_recovery_email`, //OK
    deleteRecoveryEmail: `${authUrl.recovery}/delete_recovery_email`, //OK
    //authentication -- registration
    userSignUp: `${authUrl.registration}/signup`, //OK
    acctDeleteOwnAccount: `${authUrl.registration}/delete_user`, //OK
    //authentication -- session
    getOTP: `${authUrl.session}/get_otp`, //OK
    userLogIn: `${authUrl.session}/login`, //OK
    userLogOut: `${authUrl.session}/logout`, //OK
    userGetOwnAcctInfo: `${authUrl.session}/@me`, //OK
    //authentication -- safety
    setMfa: `${authUrl.safety}/set_mfa`, //OK
    verifyAccount: `${authUrl.safety}/verify_account`, //OK
    //user_settings (preferences)
    setMailingList: `${authUrl.userSettings}/set_mailing_list`, //OK
    setNightMode: `${authUrl.userSettings}/set_night_mode`, //OK
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