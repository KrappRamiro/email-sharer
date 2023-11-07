import { removeElementsBySelector } from "../utils/domHelpers.mjs";
export class EmailList {
	constructor(querySelector) {
		/** @type {HTMLElement} */
		this.emailListElement = document.querySelector(querySelector);
	}
	/**
	 * @param {HTMLElement} element
	 */
	add(element) {
		this.emailListElement.appendChild(element);
	}

	clear() {
		console.log("Clearing the email list");
		removeElementsBySelector(this.emailListElement, ".email");
	}
}
