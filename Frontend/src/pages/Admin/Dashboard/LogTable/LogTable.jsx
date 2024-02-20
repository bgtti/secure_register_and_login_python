import { useState, useEffect, lazy, Suspense, useRef } from "react";
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice"
import { getUserLogs } from "../../../../config/apiHandler/admin/user_logs.js"
import LogTableRow from "./LogTableRow"
// import Pagination from "../Pagination/Pagination.jsx";
import "./logTable.css"

/**
 * Component returns HTML div with logs as a table
 * 
 * Child component: UserLogRow
 * 
 * @todo place a filter option to filter table according to log type
 * @todo implement pagination
 * @todo get logs using API handler
 * 
 * @visibleName Admin Area: Dashboard: Log table
 * @param {func} props.setShowLogs 
 * @returns {React.ReactElement}
 */
function LogTable(props) {
    const { setShowLogs } = props
    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    const [logs, setLogs] = useState([
        {
            "activity": "signup",
            "createdAt": "09 Jan 2024",
            "message": "successful signup.",
            "type": "INFO",
            "userId": 12345
        },
        {
            "activity": "login",
            "createdAt": "09 Jan 2024",
            "message": "successful login.",
            "type": "INFO",
            "userId": 12345
        },
        {
            "activity": "signup",
            "createdAt": "09 Jan 2024",
            "message": "problem",
            "type": "SUSPISCIOUS",
            "userId": 0
        }
    ]);
    const [curPage, setCurPage] = useState([]);
    const [tPages, setTPages] = useState([]);

    useEffect(() => {
        console.log("get log data");
    }, [])

    // function getLogs(pageNr = 1) {
    //     dispatch(setLoader(true))
    //     getUserLogs(pageNr, uuid)
    //         .then(response => {
    //             if (isComponentMounted()) {
    //                 if (response.data) {
    //                     setLogs(response.logs);
    //                     setCurPage(response.currentPage);
    //                     setTPages(response.totalPages);
    //                 } else {
    //                     setLogs([]);
    //                     setCurPage(1);
    //                     setTPages(1);
    //                 }
    //             }
    //         })
    //         .catch(error => {
    //             console.warn("getUsers (in UsersTable) encountered an error", error);
    //         })
    //         .finally(() => {
    //             dispatch(setLoader(false));
    //         })
    // }

    function handlePagination(newPage) {
        if (Number.isInteger(newPage) && newPage >= 1 && newPage <= totalPages) {
            // getLogs(newPage);
            console.log("getting new page")
        }
    }

    function handleReturn() {
        // selectUserAction("", "");
        setShowLogs(false);
    }

    return (
        <>
            <div>
                <button onClick={handleReturn}>Back to Dashboard</button>
                <h3>Recent Logs</h3>
                {/* <div>
                    <p><b className="UsersLogs-bold">User:</b> {name}</p>
                    <p><b className="UsersLogs-bold">Email:</b> {email}</p>
                </div> */}
                {
                    logs && logs.length > 0 && (
                        <table className="MAIN-table LogTable" role="table">
                            <thead role="rowgroup">
                                <tr role="row">
                                    <th role="columnheader">Date</th>
                                    <th role="columnheader">Type</th>
                                    <th role="columnheader">Activity</th>
                                    <th role="columnheader">Log message</th>
                                    <th role="columnheader">Action</th>
                                </tr>
                            </thead>
                            <tbody role="rowgroup">
                                {logs && (
                                    logs.map((log, index) => (
                                        <LogTableRow
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
            {/* {
                tPages > 1 && (
                    <Pagination
                        currentPage={curPage}
                        totalPages={tPages}
                        handlePageChange={handlePagination}
                    />
                )
            } */}
        </>
    );
};

LogTable.propTypes = {
    setShowLogs: PropTypes.func.isRequired,
};

export default LogTable;