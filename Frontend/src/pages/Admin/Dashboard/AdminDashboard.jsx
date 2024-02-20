// import UsersTable from "../UsersTable/UsersTable";
import { useState, useEffect, lazy, Suspense, useRef } from "react";
import LogTable from "./LogTable/LogTable"
import "./admindashboard.css"

/**
 * Component showing main statistics and recent logs marked as 'warn' or 'suspiscious' linked to user activity.
 * 
 * @todo implement statistics from the backend
 * @todo implement log warnings from the backend
 * @todo lazy-load LogTable
 * 
 * @visibleName Admin Area: Admin Dashboard
 * @returns {React.ReactElement}
 */
function AdminDashboard() {
    const [showLogs, setShowLogs] = useState(false)

    function toggleShowLogs() {
        setShowLogs(!showLogs);
    }

    return (
        <div className="AdminDashboard">
            <h3>Admin Dashboard</h3>
            {
                !showLogs && (
                    <>
                        <section className="AdminDashboard-Section1">
                            <div>
                                <p>10</p>
                                <p>registered users</p>
                                <p>total</p>
                            </div>
                            <div>
                                <p>10</p>
                                <p>new users</p>
                                <p>this week</p>
                            </div>
                            <div>
                                <p>10%</p>
                                <p>user growth</p>
                                <p>this month</p>
                            </div>
                            <div>
                                <p>10</p>
                                <p>website visitors</p>
                                <p>this month</p>
                            </div>
                        </section>
                        <section className="AdminDashboard-Section2">
                            <div>
                                <div className="AdminDashboard-Suspiscious"></div>
                                <p>2 logs marked 'suspiscious'</p>
                                <div>
                                    <button onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>
                            <div>
                                <div className="AdminDashboard-Warn"></div>
                                <p>3 logs marked 'warn'</p>
                                <div>
                                    <button onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>
                        </section>
                    </>

                )
            }
            {
                showLogs && (
                    <LogTable
                        setShowLogs={setShowLogs}
                    />
                )
            }
        </div>
    );
}

export default AdminDashboard;