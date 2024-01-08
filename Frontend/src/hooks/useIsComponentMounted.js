import { useEffect, useRef, useCallback } from "react";

/**
 * Custom hook to track the mounted/unmounted state of a component.
 * 
 * Usage: declare a variable inside your component and set its value to this hook. 
 * You can then call the variable as a function to get a boolean: true if the component in question is mounted, false if the component is unmounted. 
 * 
 * @returns {function(): boolean} getIsComponentMounted - Function to check if the component is mounted.
 * 
 * @example
 * const isComponentMounted = useIsComponentMounted();
 * if (isComponentMounted()) {
 *     setState(...);
 * }
 */
function useIsComponentMounted() {
    const isComponentMounted = useRef(false);

    useEffect(() => {
        isComponentMounted.current = true;
        return () => {
            isComponentMounted.current = false;
        };
    }, []);

    return useCallback(() => isComponentMounted.current, []);
}

export default useIsComponentMounted;