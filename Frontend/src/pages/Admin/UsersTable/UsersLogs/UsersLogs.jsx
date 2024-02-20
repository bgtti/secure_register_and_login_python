import { useState, useEffect, lazy, Suspense, useRef } from "react";
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice"
import { getUserLogs } from "../../../../config/apiHandler/admin/user_logs.js"
import UsersLogRow from "./UsersLogRow"
import Pagination from "../Pagination/Pagination.jsx";
import "./usersLogs.css"

/**
 * Component returns HTML div with user logs as a table
 * 
 * Child component: UserLogRow
 * 
 * @visibleName Admin Area: Users' Table: User Logs
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {number} props.user.id
 * @param {func} props.setShowUserLogs 
 * @param {func} props.selectUserAction 
 * @returns {React.ReactElement}
 */
function UsersLogs(props) {
    const { user, setShowUserLogs, selectUserAction } = props;
    const { name, email, id } = user;

    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    const [logs, setLogs] = useState([]);
    const [curPage, setCurPage] = useState([]);
    const [tPages, setTPages] = useState([]);

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
                console.warn("getUsers (in UsersTable) encountered an error", error);
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

    function handleReturn() {
        selectUserAction("", "");
        setShowUserLogs(false);
    }

    return (
        <>
            <div className="UsersLogs">
                <button onClick={handleReturn}>Back to Users Table</button>
                <h3>Activity Logs</h3>
                <div>
                    <p><b className="UsersLogs-bold">User:</b> {name}</p>
                    <p><b className="UsersLogs-bold">Email:</b> {email}</p>
                </div>
                {
                    logs && logs.length > 0 && (
                        <table className="MAIN-table UsersLogs-Table" role="table">
                            <thead role="rowgroup">
                                <tr role="row">
                                    <th role="columnheader">Date</th>
                                    <th role="columnheader">Type</th>
                                    <th role="columnheader">Activity</th>
                                    <th role="columnheader">Log message</th>
                                </tr>
                            </thead>
                            <tbody role="rowgroup">
                                {logs && (
                                    logs.map((log, index) => (
                                        <UsersLogRow
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
                        <p className="UsersLogs-bold UsersLogs-noLogs"><b>No logs available.</b></p>
                    )
                }
            </div>
            {
                tPages > 1 && (
                    <Pagination
                        currentPage={curPage}
                        totalPages={tPages}
                        handlePageChange={handlePagination}
                    />
                )
            }
        </>
    );
};

UsersLogs.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        id: PropTypes.number.isRequired
    }).isRequired,
    setShowUserLogs: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired,
};

export default UsersLogs;