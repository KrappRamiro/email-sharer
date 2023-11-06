import { Dialog } from "./components/email-dialog.mjs";
import { Copylink } from "./components/copylink.mjs";
document.addEventListener("DOMContentLoaded", () => {
	// -------- Copylink initialization -----------
	const copylinks = document.querySelectorAll("[data-copylink]");
	copylinks.forEach((copylink) => {
		const activator = copylink.querySelector("[data-copylink-activator]");
		const target = copylink.querySelector("[data-copylink-target]");
		let myCopylink = new Copylink(activator, target);
	});

	// -------- Email upload dialog initialization -----------

	const dialogEl = document.querySelector("#email-upload-dialog");
	const openDialogButton = document.querySelector("[data-open-email-dialog]");
	const closeDialogButton = document.querySelector("[data-close-email-dialog]");

	let dialog = new Dialog(dialogEl, openDialogButton, closeDialogButton);
});
