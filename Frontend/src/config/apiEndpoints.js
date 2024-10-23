const urlPrefix = {
    account: "/api/account",
    admin: "/api/admin",
    contact: "/api/contact",
}

const adminUrl = {
    dash: `${urlPrefix.admin}/dash`,
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
    //admin - dashboard
    adminGetDashboardData: `${adminUrl.dash}/admin_dash`, //MISSING
    //admin - users
    adminGetUsersTable: `${adminUrl.users}/table`, //OK
    adminGetUserInfo: `${adminUrl.users}/user_info`, //OK
    adminGetUserLogs: `${adminUrl.users}/user_logs`, //OK
    adminGetUserMessages: `${adminUrl.users}/user_messages`, // MISSING ---WORKING NOW
    //admin - user action
    adminChangeUserFlag: `${adminUrl.userAction}/flag_change`,//OK
    adminChangeUserAccessType: `${adminUrl.userAction}/access_change`,//OK
    adminBlockUnblockUser: `${adminUrl.userAction}/block_unblock`,//OK
    adminDeleteUser: `${adminUrl.userAction}/delete_user`, //OK
    //admin - messages
    adminMessagesTable: `${adminUrl.messages}/table`, // MISSING
    adminMessageMarkNoAnswer: `${adminUrl.messages}/...`, //MISSING
    adminMessageMarkAnswer: `${adminUrl.messages}/...`, //MISSING
    adminMessageFlagChange: `${adminUrl.messages}/...`, //MISSING
    adminMessageDelete: `${adminUrl.messages}/...`, //MISSING
};

export default apiEndpoints;