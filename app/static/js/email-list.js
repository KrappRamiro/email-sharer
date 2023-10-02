document.addEventListener("DOMContentLoaded", async () => {
	const emailListElement = document.querySelector("#email-list");
	const emailList = await getEmailList();
	emailList.forEach((email) => {
		let li = document.createElement("li");
		let emailElement = document.createElement("a");
		emailElement.text = email;
		if (email.endsWith(".htm") || email.endsWith(".html")) {
			emailElement.href = `email/get/html/?name=${email}`;
		} else {
			emailElement.href = `email/get/json/?name=${email}`;
		}
		li.appendChild(emailElement);
		emailListElement.appendChild(li);
	});
});

/**
 * Fetches a list of emails
 * @returns {Promise<string[]>} A promise that resolves to a list of emails
 */

async function getEmailList() {
	let response = await fetch("email/list");
	return await response.json();
}
