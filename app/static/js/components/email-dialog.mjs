export class Dialog {
	constructor(dialogEl, openDialogEl, closeDialogEl) {
		console.log("Constructing a new dialog element");
		openDialogEl.addEventListener("click", () => {
			console.log("Showing the dialog");
			dialogEl.showModal();
		});
		closeDialogEl.addEventListener("click", () => {
			console.log("Closing the dialog");
			dialogEl.close();
		});
	}
}
