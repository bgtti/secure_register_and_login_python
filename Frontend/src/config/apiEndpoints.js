const apiEndpoints = {
    baseURL: "http://127.0.0.1:5000",
    //contact
    contactUs: "api/contact/contact_form", //OK
    //account
    userSignUp: "api/account/signup", //OK
    userLogIn: "/api/account/login", //OK
    userLogOut: "/api/account/logout", //OK
    userGetOwnAcctInfo: "/api/account/@me", //OK
    userDeleteOwnAccount: "/api/account/delete", //MISSING
    //admin
    adminGetDashboardData: "/api/admin/restricted_dashboard",
    adminGetUsersTable: "api/admin/restricted_area/users",
    adminGetUserLogs: "api/admin/restricted_area/users/user_logs",
    adminBlockUnblockUser: "api/admin/restricted_area/users/block_unblock",
    adminDeleteUser: "api/admin/restricted_area/users/delete",
    //DELETE ROUTES:
    adminLogIn: "/api/admin/restricted_login",
};

export default apiEndpoints;