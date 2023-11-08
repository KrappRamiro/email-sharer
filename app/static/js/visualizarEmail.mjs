import { Copylink } from "./components/copylink.mjs";
import { localizeDate } from "./utils/localizeDate.mjs";
// -------- Copylink initialization -----------
const copylinks = document.querySelectorAll("[data-copylink]");
copylinks.forEach((copylink) => {
	const activator = copylink.querySelector("[data-copylink-activator]");
	const target = copylink.querySelector("[data-copylink-target]");
	let myCopylink = new Copylink(activator, target);

	// --------- Tooltip initialization ----------
	const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
	const tooltipList = [...tooltipTriggerList].map(
		(tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
	);
	const emailDate = document.querySelector("[data-translate-date]");
	emailDate.textContent = `${localizeDate(emailDate.textContent)}`;
});
