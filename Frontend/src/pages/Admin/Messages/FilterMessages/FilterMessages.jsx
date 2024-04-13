import { useState } from "react";
import PropTypes from 'prop-types';
import "./filterMessages.css"

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
 * Constants array for defining date order
 * @constant
 * @type {string[]}
 * @default 
 * ["descending", "ascending"]
*/
const ORDER_BY_DATE = ["descending", "ascending"];

/** 
 * Constants object for defining selection of filter
 * @constant
 * @type {object}
*/
const FILTER_BY = {
    answer_needed: "answer needed",
    answered_not_needed: "answer not needed",
    all: "all",
}

/*******************  THE COMPONENT  ********************/

/**
 * Component that enables filtering messages.
 * Will validate user input before changing the parent's state filterOptions.
 * 
 * @param {object} props
 * @param {function} props.setFilterOptions updates props.filterOptions
 * @param {object} props.filterOptions state in parent
 * @param {string} props.filterOptions.itemsPerPage string containing int
 * @param {string} props.filterOptions.orderByDate string 
 * @param {string} props.filterOptions.filterBy string 
 *
 * @returns {React.ReactElement}
 */
function FilterMessages(props) {
    const { filterOptions, setFilterOptions } = props

    const [showOptions, setShowOptions] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    const [formData, setFormData] = useState({
        itemsPerPage: filterOptions.itemsPerPage,
        orderByDate: filterOptions.orderByDate,
        filterBy: filterOptions.filterBy
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
        //Check data
        let itemsPerPage = parseInt(formData.itemsPerPage)
        itemsPerPage = (formData.itemsPerPage && Number.isInteger(itemsPerPage) && itemsPerPage >= 5 && itemsPerPage <= 50 && itemsPerPage % 5 === 0) ? itemsPerPage : false;
        let orderByDate = (formData.orderByDate && ORDER_BY_DATE.includes(formData.orderByDate)) ? formData.orderByDate : false;
        let filter = (formData.filterBy && formData.filterBy in FILTER_BY) ? formData.filterBy : false;

        //Make sure form is valid and that fields were changed
        let formIsValid = itemsPerPage && orderByDate && filter
        let stateChanged = JSON.stringify(filterOptions) !== JSON.stringify(formData)

        if (formIsValid && stateChanged) {
            setErrorMessage("")
            setFilterOptions({ ...formData })
            setShowOptions(false);
        } else {
            (formIsValid && !stateChanged) ?
                setErrorMessage("Oops, no changes detected. Change selection and try again.") :
                setErrorMessage("An error occurred. Change selection and try again.")
        };
    };

    return (
        <div>
            <button className={`FilterMessages-btn ${showOptions ? "FilterMessages-btn-selected" : ""}`} onClick={toggleShowOptions}>
                {showOptions ? "Hide filter options ↓" : "Show filter options ->"}
            </button>
            {
                showOptions && (
                    <form action="" className="MAIN-form FilterMessages-form" onSubmit={handleSubmit}>
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
                            <label htmlFor="orderByDate">Sort order:</label>
                            <select name="orderByDate" id="orderByDate" defaultValue={formData.orderByDate} onChange={handleChange}>
                                {
                                    ORDER_BY_DATE.map((item, index) => (
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

FilterMessages.propTypes = {
    setFilterOptions: PropTypes.func.isRequired,
    filterOptions: PropTypes.shape({
        itemsPerPage: PropTypes.string.isRequired,
        orderByDate: PropTypes.string.isRequired,
        filterBy: PropTypes.string.isRequired,
    })
};

export default FilterMessages;