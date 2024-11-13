import { useState, useEffect, lazy, Suspense, useRef } from "react";
import iconMail from "../../../assets/icon_mail.svg";
import iconTodo from "../../../assets/icon_todo_checkbox.svg";
import iconLog from "../../../assets/icon_log.svg"
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
                        {/* ANALYTICS */}
                        <section className="AdminDashboard-Analytics">
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

                        <h4>Needs your attention:</h4>

                        {/* Alerts */}
                        <section className="AdminDashboard-Alerts">
                            {/* Messages */}
                            <div>
                                <div className="AdminDashboard-BgBlue"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Messages."}
                                        role="img"
                                        title={"Messages"}
                                        src={iconMail}
                                    />
                                </div>
                                <p>5 unanswered messages</p>
                                <div>
                                    <button onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>

                            {/* Admin tasks */}
                            <div>
                                <div className="AdminDashboard-BgBlue"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Tasks"}
                                        role="img"
                                        title={"Tasks"}
                                        src={iconTodo}
                                    />
                                </div>
                                <p>5 open tasks</p>
                                <div>
                                    <button onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>

                            {/* Logs marked suspicious */}
                            <div>
                                <div className="AdminDashboard-BgYellow"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Suspicious log"}
                                        role="img"
                                        title={"Suspicious log"}
                                        src={iconLog}
                                    />
                                </div>
                                <p>2 activity logs marked 'suspiscious'</p>
                                <div>
                                    <button onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>

                            {/* Logs marked warn */}
                            <div>
                                <div className="AdminDashboard-BgRed"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Warn log"}
                                        role="img"
                                        title={"Warn log"}
                                        src={iconLog}
                                    />
                                </div>
                                <p>3 activity logs marked 'warn'</p>
                                <div>
                                    <button onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>
                        </section>

                        <h4>Under control:</h4>

                        {/* Alerts ---- disabled*/}
                        {/* DIFFERENCE FROM THE ABOVE:
                        - FIRST DIV: gets className="AdminDashboard-BgDarkBlue"
                        - BUTTON: gets className="AdminDashboard-BtnDark" */}
                        <section className="AdminDashboard-Alerts">
                            {/* Messages */}
                            <div>
                                <div className="AdminDashboard-BgDarkBlue"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Messages."}
                                        role="img"
                                        title={"Messages"}
                                        src={iconMail}
                                    />
                                </div>
                                <p>5 unanswered messages</p>
                                <div>
                                    <button className="AdminDashboard-BtnDark"
                                        onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>

                            {/* Admin tasks */}
                            <div>
                                <div className="AdminDashboard-BgDarkBlue"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Tasks"}
                                        role="img"
                                        title={"Tasks"}
                                        src={iconTodo}
                                    />
                                </div>
                                <p>5 open tasks</p>
                                <div>
                                    <button className="AdminDashboard-BtnDark"
                                        onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>

                            {/* Logs marked suspicious */}
                            <div>
                                <div className="AdminDashboard-BgDarkBlue"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Suspicious log"}
                                        role="img"
                                        title={"Suspicious log"}
                                        src={iconLog}
                                    />
                                </div>
                                <p>2 activity logs marked 'suspiscious'</p>
                                <div>
                                    <button className="AdminDashboard-BtnDark"
                                        onClick={toggleShowLogs}>view</button>
                                </div>
                            </div>

                            {/* Logs marked warn */}
                            <div>
                                <div className="AdminDashboard-BgDarkBlue"></div>
                                <div className=" AdminDashboard-IconContainer">
                                    <img
                                        alt={"Warn log"}
                                        role="img"
                                        title={"Warn log"}
                                        src={iconLog}
                                    />
                                </div>
                                <p>3 activity logs marked 'warn'</p>
                                <div>
                                    <button className="AdminDashboard-BtnDark"
                                        onClick={toggleShowLogs}>view</button>
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