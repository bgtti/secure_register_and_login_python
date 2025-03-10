import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice";
import { PATH_TO } from "../../../../router/routePaths.js";
import { getUserLogs } from "../../../../config/apiHandler/admin/userLogs.js"
import UserLogRow from "./UserLogRow.jsx"
import Pagination from "../../../../components/Pagination/Pagination.jsx";
import "./userLogs.css"

/**
 * Component returns HTML div with selected user's logs
 * 
 * Should be passed a location state when navigated to: the selected user's id, name, and email.
 * 
 * @param {object} state //selected user passed as location state
 * @param {string} state.name
 * @param {string} state.email
 * @param {number} state.id
 * @returns {React.ReactElement}
 * @example
 * navigate("userLogs", { state: user })
 */
function UserLogs() {
    const location = useLocation();
    const user = location.state;
    const { name, email, id } = user;

    if (!user || !user.name || !user.email || !user.id) {
        console.error("Missing location state in UserLogs.")
    }

    const dispatch = useDispatch();
    const navigate = useNavigate();

    // Only set state if component is mounted
    const isComponentMounted = useIsComponentMounted();

    // Store logs and pagination
    const [logs, setLogs] = useState([]);
    const [curPage, setCurPage] = useState([]);
    const [tPages, setTPages] = useState([]);

    // Request user info upon component mount
    useEffect(() => {
        getLogs();
    }, [])

    function getLogs(pageNr = 1) {
        if (id === 0) {
            return
        }
        dispatch(setLoader(true))
        getUserLogs(pageNr, id)
            .then(response => {
                if (isComponentMounted()) {
                    if (response.data) {
                        setLogs(response.logs);
                        setCurPage(response.currentPage);
                        setTPages(response.totalPages);
                    } else {
                        setLogs([]);
                        setCurPage(1);
                        setTPages(1);
                    }
                }
            })
            .catch(error => {
                console.warn("getUserLogs (in UserLogs) encountered an error", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    }

    function handlePagination(newPage) {
        if (Number.isInteger(newPage) && newPage >= 1 && newPage <= totalPages) {
            getLogs(newPage);
        }
    }



    return (
        <div className="MAIN-subNav-page UserLogs">
            <h3>User Logs</h3>

            <div className="UserLogs-btnContainer">
                <button onClick={() => { navigate(PATH_TO.adminArea_userInfo, { state: id }) }}>Back to User's Info</button>
                <button onClick={() => { navigate(PATH_TO.adminArea_usersTable) }}>Back to Users Table</button>
            </div>

            <h4 >User</h4>

            <div>
                <p><b>User:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
            </div>

            <h4>Logs</h4>

            {
                logs && logs.length > 0 && (
                    <table className="MAIN-table UserLogs-Table" role="table">
                        <thead role="rowgroup">
                            <tr role="row">
                                <th role="columnheader">Date</th>
                                <th role="columnheader">Level</th>
                                <th role="columnheader">Activity</th>
                                <th role="columnheader">Log message</th>
                            </tr>
                        </thead>
                        <tbody role="rowgroup">
                            {logs && (
                                logs.map((log, index) => (
                                    <UserLogRow
                                        log={log}
                                        key={index}
                                    />
                                ))
                            )}
                        </tbody>
                    </table>
                )
            }
            {
                ((logs && logs.length == 0) || (!logs)) && (
                    <p className="UserLogs-bold UserLogs-noLogs"><b>No logs available.</b></p>
                )
            }
            {
                tPages > 1 && (
                    <Pagination
                        currentPage={curPage}
                        totalPages={tPages}
                        handlePageChange={handlePagination}
                    />
                )
            }
        </div>
    );
}
export default UserLogs;