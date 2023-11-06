import { getCurrentUserId } from "./utils/getCurrentUserId.mjs";
const emailForm = document.getElementById("email-form");

emailForm.addEventListener("submit", async (event) => {
	event.preventDefault();

	// Get the selected file from the file input field
	const emailFileInput = document.getElementById("email-file-input");
	const emailFile = emailFileInput.files[0];

	if (!emailFile) {
		alert("Por favor seleccione un email para subir.");
		return;
	}

	// Create a FormData object and append the file to it
	const formData = new FormData();
	formData.append("email_file", emailFile);

	const userId = getCurrentUserId();

	try {
		const response = await fetch(`/users/${userId}/email/`, {
			method: "POST",
			body: formData,
		});

		if (response.ok) {
			// Successfully uploaded the file
			console.log("File uploaded successfully.");
		} else {
			// Handle the error response, if any
			const errorMessage = await response.text();
			console.error(`Error: ${errorMessage}`);
		}
	} catch (error) {
		// Handle any network or fetch-related errors
		console.error(`Network or fetch error: ${error}`);
	}
});
