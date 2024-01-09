const apiEndpoints = {
    userSignUp: "api/account/signup",
    userLogIn: "/api/account/login",
    userLogOut: "/api/account/logout",
    userGetOwnAcctInfo: "/api/account/@me",
    userDeleteOwnAccount: "/api/account/delete",
    adminLogIn: "/api/admin/restricted_login",
    adminGetDashboardData: "/api/admin/restricted_dashboard",
    adminGetUsersTable: "api/admin/restricted_area/users",
    adminBlockUnblockUser: "api/admin/restricted_area/users/block_unblock",
    adminDeleteUser: "api/admin/restricted_area/users/delete",
};

export default apiEndpoints