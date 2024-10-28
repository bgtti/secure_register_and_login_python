const urlPrefix = {
    account: "/api/account",
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
    //account
    userSignUp: `${urlPrefix.account}/signup`, //OK
    userLogIn: `${urlPrefix.account}/login`, //OK
    userLogOut: `${urlPrefix.account}/logout`, //OK
    userGetOwnAcctInfo: `${urlPrefix.account}/@me`, //OK
    userDeleteOwnAccount: `${urlPrefix.account}/delete`, //MISSING
    userChangeEmail: `${urlPrefix.account}/...`, //MISSING
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
    adminMessagesTable: `${adminUrl.messages}/table`, // OK ? (check filter...)
    adminMessageMarkAs: `${adminUrl.messageAction}/mark_as`, //OK 
    adminMessageAnswer: `${adminUrl.messageAction}/...`, //MISSING
    adminMessageFlagChange: `${adminUrl.messageAction}/flag_change`, //MISSING ------------WORKING NOW
    adminMessageDelete: `${adminUrl.messageAction}/...`, //MISSING
};

export default apiEndpoints;