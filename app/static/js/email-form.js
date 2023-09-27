const emailForm = document.querySelector("#email-form");
emailForm.addEventListener("submit", async (event) => {
	event.preventDefault();
	email = await getEmailInfo(emailForm);
	console.dir(email);
});

/**
 * @param {HTMLFormElement} emailForm
 * @returns {Object}
 */
async function getEmailInfo(emailForm) {
	const formData = new FormData(emailForm);
	try {
		const response = await fetch("email-info", {
			method: "POST", // Change the HTTP method if needed
			body: formData, // Pass the form data as the request body
		});
		if (response.ok) {
			return await response.json();
		} else {
			console.log("ERROR: ", response.statusText);
		}
	} catch (error) {
		console.log("ERROR:", error);
	}
}
