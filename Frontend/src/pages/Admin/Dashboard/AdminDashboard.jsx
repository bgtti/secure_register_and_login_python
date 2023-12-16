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
                </div>
                <div>
                    <p>10</p>
                    <p>website visitors</p>
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