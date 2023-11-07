import { Dialog } from "./components/email-dialog.mjs";
import { Email } from "./components/email.mjs";
import { EmailList } from "./components/emaillist.mjs";
import { Copylink } from "./components/copylink.mjs";
import { DropZone } from "./components/dropzone.mjs";
import { getUserEmails } from "./utils/getUserEmails.mjs";
import { getCurrentUserId } from "./utils/getCurrentUserId.mjs";
const currentUserId = getCurrentUserId();
document.addEventListener("DOMContentLoaded", async () => {
	// -------- Email upload dialog initialization -----------
	const dialogEl = document.querySelector("#email-upload-dialog");
	const openDialogButton = document.querySelector("[data-open-email-dialog]");
	const closeDialogButton = document.querySelector("[data-close-email-dialog]");
	let dialog = new Dialog(dialogEl, openDialogButton, closeDialogButton);

	// -------- Email list initialization -----------
	let emailList = new EmailList("#email-list");
	const userEmails = await getUserEmails(currentUserId);
	userEmails.forEach((emailData) => {
		const email = new Email(emailData);
		emailList.add(email.getHtmlElement());
	});

	// -------- Copylink initialization -----------
	const copylinks = document.querySelectorAll("[data-copylink]");
	copylinks.forEach((copylink) => {
		const activator = copylink.querySelector("[data-copylink-activator]");
		const target = copylink.querySelector("[data-copylink-target]");
		let myCopylink = new Copylink(activator, target);
	});

	// -------- Dropzone initialization ------------
	document.querySelectorAll(".drop-zone").forEach((dropZoneElement) => {
		new DropZone(dropZoneElement, true);
	});

	// -------- Stepper initialization ------------
});
