export class Email {
	/**
	 *
	 * @param {*} email Must be a python schemas.Email
	 */
	constructor(email) {
		this.email = email;
	}
	getHtmlElement() {
		const emailUrl = this.getEmailUrl();
		const emailElement = document.createElement("div");
		emailElement.innerHTML = `
			<div class="email">
				<div class="email__left">
					<div class="email__owner-name"> ${this.email.sender} </div>
					<div class="email__date"> ${this.email.date} </div>
				</div>
				<div>
					<div class="email__middle">
						<a class="email__subject" href="${emailUrl}" >${this.email.subject}</a>
					</div>
				</div>
				<div class="email__right">
					<div class="email__share-icon"> <box-icon name='share-alt' type='solid' color='black' ></box-icon>	</div>
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
