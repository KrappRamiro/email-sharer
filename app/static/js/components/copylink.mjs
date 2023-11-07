export class Copylink {
	/**
	 * @param {HTMLElement} activatorEl
	 * @param {HTMLAnchorElement} targetEl
	 */
	constructor(activatorEl, targetEl) {
		activatorEl.addEventListener("click", () => {
			this.copyLinkToClipboard(targetEl);
		});
	}

	/**
	 * @param {HTMLAnchorElement} anchorEl
	 */
	copyLinkToClipboard(anchorEl) {
		if (anchorEl) {
			let linkHref = anchorEl.getAttribute("href"); // Get the href attribute
			if (linkHref) {
				let textArea = document.createElement("textarea");
				textArea.value = linkHref;

				// Add the textarea to the document
				document.body.appendChild(textArea);

				// Select the text in the textarea
				textArea.select();

				try {
					// Execute the copy command
					document.execCommand("copy");
					console.log("Full URL copied to clipboard: " + linkHref);
				} catch (err) {
					console.error("Unable to copy full URL to clipboard: " + err);
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
}
