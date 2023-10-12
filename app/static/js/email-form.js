const emailDialog = document.querySelector("#email-upload-dialog");
const emailForm = document.querySelector("#email-form");
emailForm.addEventListener("submit", async (event) => {
	event.preventDefault();
	email = await uploadEmail(emailForm);
	console.dir(email);
});

/**
 * @param {HTMLFormElement} emailForm
 * @returns {Object}
 */
async function uploadEmail(emailForm) {
	const formData = new FormData(emailForm);
	try {
		const response = await fetch("email/upload", {
			method: "POST", // Change the HTTP method if needed
			body: formData, // Pass the form data as the request body
		});
		if (response.ok) {
			console.log("Response OK when uploading email");
			emailDialog.close();
			return await response.json();
		} else {
			console.log("ERROR: ", response.statusText);
		}
	} catch (error) {
		console.log("ERROR:", error);
	}
}
