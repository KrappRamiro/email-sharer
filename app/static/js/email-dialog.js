/**
 * @type {HTMLDialogElement} */
const dialog = document.querySelector("#email-upload-dialog");
const closeDialogButton = document.querySelector("#close-email-dialog-button");
const openDialogButton = document.querySelector("#open-email-dialog-button");

openDialogButton.addEventListener("click", () => {
	dialog.style.display = "flex";
	dialog.showModal();
});
closeDialogButton.addEventListener("click", () => {
	dialog.style.display = "none";
	dialog.close();
});
