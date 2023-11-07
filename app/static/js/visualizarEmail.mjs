import { Copylink } from "./components/copylink.mjs";
// -------- Copylink initialization -----------
const copylinks = document.querySelectorAll("[data-copylink]");
copylinks.forEach((copylink) => {
	const activator = copylink.querySelector("[data-copylink-activator]");
	const target = copylink.querySelector("[data-copylink-target]");
	let myCopylink = new Copylink(activator, target);
});
