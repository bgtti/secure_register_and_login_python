import { PropTypes } from "prop-types";
import iconClose from "../../assets/icon_close.svg"
import { capitalizeFirstLetter } from "../../utils/helpers"
import "./modal.css"

/**
 * Component is a modal wrapper. Returns a div with the content passed as props
 * 
 * This component controls how modals are displayed throughout the application.
 * 
 * Important when using the Modal component, place the following in the parent:
modalStatus ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
(replacing "modalStatus" with whatever variable name used to keep track of modal state)
 * 
 * @visibleName Modal Wrapper
 * @param {object} props
 * @param {bool} modalStatus defines whether you want to show the modal
 * @param {func} props.setModalStatus enabled the change of modalStatus
 * @param {string} props.title title of the modal
 * @param {element} props.content the body of the modal
 * @param {bool} [props.dontCapitalizeTitle = false] optional prop, set to true if you want the title to appear exactly as you wrote it. If set to false, each first letter of the title will be capitalized.
 * @returns {React.ReactElement}
 * 
 * @example
 * import Modal from ".../components/Modal/Modal"
 * import { useState} from "react";
 * //inside the functional component:
 * const [showModal, setShowModal] = useState(false)
 * function toggleModal() {setShowModal(!showModal)}
 * const modalInfo = <p>This is the modal body content</p>
 * showModal ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active"); // <- include this!
 * return (
 * <Modal title="Modal Example" content={modalInfo} modalStatus={showModal} setModalStatus={setShowModal} ></Modal> 
 * )
 */
function Modal(props) {
    const { modalStatus, setModalStatus, title, content, dontCapitalizeTitle } = props;

    //optional props dontCapitalizeTitle will capitalize every first letter in string if set to true.
    let displayTitle;
    !dontCapitalizeTitle ? displayTitle = capitalizeFirstLetter(title) : displayTitle = title;

    const toggleModal = () => {
        setModalStatus(!modalStatus);
    }
    return (
        modalStatus && (
            <div className="Modal">
                <div className="Modal-Container">
                    <div className="Modal-Heading">
                        <h2>{displayTitle}</h2>
                        <div>
                            <img
                                alt="Close modal"
                                className="Modal-Heading-icon"
                                role="button"
                                title="Close modal"
                                src={iconClose}
                                onClick={toggleModal} />
                        </div>
                    </div>
                    {content}
                </div>
            </div>
        )
    );
};

Modal.propTypes = {
    modalStatus: PropTypes.bool.isRequired,
    setModalStatus: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    content: PropTypes.element.isRequired,
    dontCapitalizeTitle: PropTypes.bool
};

export default Modal;