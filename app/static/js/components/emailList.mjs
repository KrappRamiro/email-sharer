export class EmailList {
	constructor(querySelector) {
		this.emailListElement = document.querySelector(querySelector);
	}
	/**
	 * @param {HTMLElement} element
	 */
	add(element) {
		this.emailListElement.appendChild(element);
	}
}
