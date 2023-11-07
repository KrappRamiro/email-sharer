import { Dialog } from "./components/email-dialog.mjs";
import { Email } from "./components/email.mjs";
import { EmailList } from "./components/emailList.mjs";
import { Paginator } from "./components/paginator.mjs";
import { Copylink } from "./components/copylink.mjs";
import { DropZone } from "./components/dropzone.mjs";
import { getUserEmails } from "./utils/getUserEmails.mjs";
import { getCurrentUserId } from "./utils/getCurrentUserId.mjs";
import { getEmailAmount } from "./utils/getEmailAmount.mjs";
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
	console.log(`found ${copylinks.length} copylinks`);
	copylinks.forEach((copylink) => {
		const activator = copylink.querySelector("[data-copylink-activator]");
		const target = copylink.querySelector("[data-copylink-target]");
		let myCopylink = new Copylink(activator, target);
	});

	// -------- Dropzone initialization ------------
	document.querySelectorAll(".drop-zone").forEach((dropZoneElement) => {
		new DropZone(dropZoneElement, true);
	});

	// -------- Paginator initialization ------------
	const dots = [
		document.querySelector("[data-paginator-tab-1]"),
		document.querySelector("[data-paginator-tab-2]"),
		document.querySelector("[data-paginator-tab-3]"),
	];
	const paginatorGoLeft = document.querySelector("[data-paginator-go-left]");
	const paginatorGoRight = document.querySelector("[data-paginator-go-right]");
	const numOfElements = await getEmailAmount(currentUserId);
	const paginator = new Paginator(paginatorGoLeft, paginatorGoRight, numOfElements, dots);

	// --------- Tooltip initialization ----------
	const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
	const tooltipList = [...tooltipTriggerList].map(
		(tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
	);
});
