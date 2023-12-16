import UsersTable from "../UsersTable/UsersTable";

import "./admindashboard.css"
function AdminDashboard() {

    return (
        <div className="AdminDashboard">
            <h3>Admin Dashboard</h3>
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
                        <button>view</button>
                    </div>
                </div>
                <div>
                    <div className="AdminDashboard-Warn"></div>
                    <p>3 logs marked 'warn'</p>
                    <div>
                        <button>view</button>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default AdminDashboard;