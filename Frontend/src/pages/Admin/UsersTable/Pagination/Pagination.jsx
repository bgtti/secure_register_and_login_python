import React from 'react'
import PropTypes from 'prop-types'
import "./Pagination.css"

/**
 * Component for displaying pagination at the bottom of a table component
 * Returns a div element with nested p and button elements
 * @param {object} props
 * @param {number} props.currentPage should be int
 * @param {number} props.totalPages should be int
 * @param {func} props.handlePageChange function to handles page change
 * @returns {React.ReactElement}
 */
function Pagination(props) {
    const { currentPage, totalPages, handlePageChange } = props
    return (
        <div className="Pagination">
            <p>Page {currentPage} of {totalPages}</p>
            {
                totalPages > 1 && (
                    <div>
                        <button disabled={currentPage === 1} onClick={() => handlePageChange(currentPage - 1)}> &lt; Previous</button>
                        <button disabled={currentPage === totalPages} onClick={() => handlePageChange(currentPage + 1)}>Next &gt;</button>
                    </div>
                )
            }
        </div>
    )
};

Pagination.propTypes = {
    currentPage: PropTypes.number.isRequired,
    totalPages: PropTypes.number.isRequired,
    handlePageChange: PropTypes.func.isRequired,
};

export default Pagination;
