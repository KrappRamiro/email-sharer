/**
 *
 * @param {HTMLElement} htmlElement
 * @param {string} querySelector
 * @returns {htmlElement}
 */
export function findElementlWithinParent(htmlElement, querySelector) {
	const parentElement = htmlElement.parentElement;
	// Find the element with querySelector within the parent element
	const labelElement = parentElement.querySelector(querySelector);
	return labelElement;
}

/**
 *
 * @param {HTMLElement} element
 * @param {string} selector
 * @returns
 */
export function findParentBySelector(element, selector) {
	let parent = element.parentElement;

	while (parent) {
		if (parent.matches(selector)) {
			return parent; // Return the matching parent element
		}
		parent = parent.parentElement; // Move up the DOM hierarchy
	}

	return null; // Return null if no matching parent is found
}
export function removeElementsBySelector(parentElement, elementSelector) {
	if (parentElement) {
		const elementsToRemove = parentElement.querySelectorAll(elementSelector);

		elementsToRemove.forEach((element) => {
			element.remove();
		});
	}
}
