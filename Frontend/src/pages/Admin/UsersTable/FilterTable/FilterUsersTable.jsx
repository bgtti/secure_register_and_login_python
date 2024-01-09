import { useState } from "react";
import { flushSync } from 'react-dom';
import PropTypes from 'prop-types';
import "../usersTable.css"

/*******************  CONSTANTS  ********************/

/** 
 * Constants array for defining selection of items per page
 * @constant
 * @type {string[]}
 * @default 
 * ["5", "10", "25", "50"]
*/
const ITEMS_PER_PAGE = ["5", "10", "25", "50"];

/** 
 * Constants object for defining selection of order
 * @constant
 * @type {object}
 * @default 
 * {
    last_seen: "last seen",
    name: "name",
    email: "email",
    created_at: "created at"
}
*/
const ORDER_BY = {
    last_seen: "last seen",
    name: "name",
    email: "email",
    created_at: "created at"
}

/** 
 * Constants array for defining selection of sort
 * @constant
 * @type {string[]}
 * @default 
 * ["descending", "ascending"]
*/
const ORDER_SORT = ["descending", "ascending"];

/** 
 * Constants object for defining selection of filter
 * @constant
 * @type {object}
 * @default 
 * {
    none: "no filter",
    is_blocked: "blocked users"
}
*/
const FILTER_BY = {
    none: "no filter",
    is_blocked: "blocked users"
}

/*******************  THE COMPONENT  ********************/

/**
 * Component that enables filtering the user's table.
 * Will validate user input before changing the parent's state tableOptions.
 * 
 * @param {object} props
 * @param {function} props.setTableOptions updates props.tableOptions
 * @param {object} props.tableOptions state in parent
 * @param {string} props.tableOptions.itemsPerPage string containing int
 * @param {string} props.tableOptions.orderBy string 
 * @param {string} props.tableOptions.orderSort string 
 * @param {string} props.tableOptions.filterBy string 
 *
 * @returns {React.ReactElement}
 */
function FilterUsersTable(props) {
    const { tableOptions, setTableOptions } = props

    const [showOptions, setShowOptions] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const [formData, setFormData] = useState({
        itemsPerPage: tableOptions.itemsPerPage,
        orderBy: tableOptions.orderBy,
        orderSort: tableOptions.orderSort,
        filterBy: tableOptions.filterBy
    });

    function toggleShowOptions() {
        setShowOptions(!showOptions);
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        let itemsPerPage = parseInt(formData.itemsPerPage)
        itemsPerPage = (formData.itemsPerPage && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : false;
        let orderBy = (formData.orderBy && formData.orderBy in ORDER_BY) ? formData.orderBy : false;
        let orderSort = (formData.orderSort && ORDER_SORT.includes(formData.orderSort)) ? formData.orderSort : false;
        let filter = (formData.filterBy && formData.filterBy in FILTER_BY) ? formData.filterBy : false;

        let formIsValid = itemsPerPage && orderBy && orderSort && filter
        let stateChanged = JSON.stringify(tableOptions) !== JSON.stringify(formData)

        if (formIsValid && stateChanged) {
            setErrorMessage("")
            setTableOptions({ ...formData })
            setShowOptions(false);
        } else {
            (formIsValid && !stateChanged) ?
                setErrorMessage("Oops, no changes detected. Change selection and try again.") :
                setErrorMessage("An error occurred. Change selection and try again.")
        };
    };

    return (
        <div>
            <button className={`UsersTableFilters-btn ${showOptions ? "UsersTableFilters-btn-selected" : ""}`} onClick={toggleShowOptions}>
                {showOptions ? "Hide table options ↓" : "Show table options ->"}
            </button>
            {
                showOptions && (
                    <form action="" className="MAIN-form UsersTableFilters-form" onSubmit={handleSubmit}>
                        <div className="MAIN-form-display-table">
                            <label htmlFor="itemsPerPage">Items per page:</label>
                            <select name="itemsPerPage" id="itemsPerPage" defaultValue={formData.itemsPerPage} onChange={handleChange}>
                                {
                                    ITEMS_PER_PAGE.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                        <div className="MAIN-form-display-table">
                            <label htmlFor="orderBy">Sort by:</label>
                            <select name="orderBy" id="orderBy" defaultValue={formData.orderBy} onChange={handleChange}>
                                {
                                    Object.keys(ORDER_BY).map((key, index) => (
                                        <option value={key} key={index}>{ORDER_BY[key]}</option>
                                    ))
                                }
                            </select>
                        </div>
                        <div className="MAIN-form-display-table">
                            <label htmlFor="orderSort">Sort order:</label>
                            <select name="orderSort" id="orderSort" defaultValue={formData.orderSort} onChange={handleChange}>
                                {
                                    ORDER_SORT.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                        <div className="MAIN-form-display-table">
                            <label htmlFor="filterBy">Filter:</label>
                            <select name="filterBy" id="filterBy" defaultValue={formData.filterBy} onChange={handleChange}>
                                {
                                    Object.keys(FILTER_BY).map((key, index) => (
                                        <option value={key} key={index}>{FILTER_BY[key]}</option>
                                    ))
                                }
                            </select>
                        </div>
                        {
                            errorMessage !== "" && (
                                <p className="MAIN-error-message">
                                    <i>{errorMessage}</i>
                                </p>
                            )
                        }
                        <button type="submit">Apply selection</button>
                    </form>
                )
            }
        </div>
    );
};

FilterUsersTable.propTypes = {
    setTableOptions: PropTypes.func.isRequired,
    tableOptions: PropTypes.shape({
        itemsPerPage: PropTypes.string,
        orderBy: PropTypes.string,
        orderSort: PropTypes.string,
        filterBy: PropTypes.string,
        tableOptionsChanged: PropTypes.bool
    })
};

export default FilterUsersTable;