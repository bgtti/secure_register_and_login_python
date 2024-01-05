import { useState } from "react";
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
 * Component that enables filtering the user's table
 * 
 * @param {object} props
 * @param {func} props.getUsers function from parent that manages api call
 * @param {func} props.setFilterBy updates state in parent
 * @param {string} props.filterBy state in parent 
 * @returns {React.ReactElement}
 */
function FilterUsersTable(props) {
    const { getUsers, setFilterBy, filterBy } = props

    const [showOptions, setShowOptions] = useState(false);

    const [formData, setFormData] = useState({
        itemsPerPage: "25",
        orderBy: "last_seen",
        orderSort: "descending",
        filterBy: { filterBy },
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

        if (formIsValid) {
            setFilterBy(filter)
            getUsers(1, itemsPerPage, orderBy, orderSort, filter);
        } else {
            console.warn("You are trying to submit invalid data.");
        }
        setShowOptions(false);
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
                        <button type="submit">Apply selection</button>
                    </form>
                )
            }
        </div>
    );
};

FilterUsersTable.propTypes = {
    getUsers: PropTypes.func.isRequired,
    setFilterBy: PropTypes.func.isRequired,
    filterBy: PropTypes.string.isRequired,
};

export default FilterUsersTable;