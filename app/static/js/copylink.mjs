import { findElementlWithinParent, findParentBySelector } from "./domHelpers.mjs";

const copylinks = document.querySelectorAll(".email__copylink");
copylinks.forEach((element) => {
	console.log("¿? wtf man");
	element.addEventListener("click", () => {
		copylink(element);
	});
});

function copylink(element) {
	const emailParent = findParentBySelector(element, ".email");
	const emailLinkElement = findElementlWithinParent(emailParent, ".email__link");
	console.log(Object.getPrototypeOf(emailLinkElement));
	copyToClipboard(emailLinkElement);
}

function copyToClipboard(copyText) {
	navigator.clipboard.writeText(copyText.href);
	console.log("Copied the text: " + copyText.href);
}
