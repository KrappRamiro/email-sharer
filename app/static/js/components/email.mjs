import { localizeDate } from "../utils/localizeDate.mjs";
export class Email {
	/**
	 *
	 * @param {*} email Must be a python schemas.Email
	 */
	constructor(email) {
		email.date = localizeDate(email.date);
		this.email = email;
	}

	getHtmlElement() {
		const emailUrl = this.getEmailUrl();
		const emailElement = document.createElement("div");
		emailElement.classList.add("email");
		emailElement.setAttribute("data-copylink", "");
		emailElement.innerHTML = `
				<div class="email__left">
				 <div class="d-flex">
					<a class="email__subject" data-copylink-target href="${emailUrl}" >${this.email.subject}</a>
				 	<div class="copy-link-wrapper" data-bs-toggle="tooltip" data-bs-title="Copiar Link" data-copylink-activator>
						<box-icon name='link-alt' color='#0c1886' class="copy-link-icon" ></box-icon>
					</div>
				 </div>
					<div class="email__date"> ${this.email.date} </div>
				</div>
				<div class="email__middle">
				</div>
				<div class="email__right">
					<div class="email__delete-icon">
						<box-icon name='trash' type='solid' color='black'></box-icon>
					</div>
				</div>
		`;
		return emailElement;
	}
	getEmailUrl() {
		const serverUrl = window.location.origin;
		const fullEmailUrl = serverUrl + `/visualizar-email/${this.email.id}`;
		return fullEmailUrl;
	}
}
