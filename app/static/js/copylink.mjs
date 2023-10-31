import { findElementlWithinParent, findParentBySelector } from "./domHelpers.mjs";

const copylinks = document.querySelectorAll(".email__copylink");
copylinks.forEach((element) => {
	element.addEventListener("click", () => {
		copylink(element);
	});
});

function copylink(element) {
	const emailParent = findParentBySelector(element, ".email");
	const emailLinkElement = findElementlWithinParent(emailParent, ".email__link");
	copyLinkToClipboard(emailLinkElement);
}

function copyLinkToClipboard(anchorEl) {
	if (anchorEl) {
		var linkHref = anchorEl.getAttribute("href"); // Get the href attribute

		if (linkHref) {
			var textArea = document.createElement("textarea");
			textArea.value = linkHref;

			// Add the textarea to the document
			document.body.appendChild(textArea);

			// Select the text in the textarea
			textArea.select();

			try {
				// Execute the copy command
				document.execCommand("copy");
				console.log("Link copied to clipboard: " + linkHref);
			} catch (err) {
				console.error("Unable to copy link to clipboard: " + err);
			}

			// Remove the textarea from the document
			document.body.removeChild(textArea);
		} else {
			console.error("The selected <a> element does not have an 'href' attribute.");
		}
	} else {
		console.error("No <a> element found on the page.");
	}
}

