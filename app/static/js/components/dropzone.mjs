/**
* * Usage example:

** HTML:
    <div class="drop-zone">
        <input type="file" class="drop-zone__input" id="fileInput">
        <label for="fileInput" class="drop-zone__label">
            <div class="drop-zone__prompt">Drop file here or click to upload</div>
            <div class="drop-zone__thumb"></div>
        </label>
    </div>

** JS:
// Initialize DropZone for all elements with the class 'drop-zone'
document.querySelectorAll(".drop-zone").forEach((dropZoneElement) => {
	new DropZone(dropZoneElement);
});

*/
// Define a class for a drop zone element
export class DropZone {
	constructor(dropZoneElement, thumbnailEnabled = true) {
		this.dropZoneElement = dropZoneElement;
		this.inputElement = dropZoneElement.querySelector(".drop-zone__input");
		this.thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
		this.promptElement = dropZoneElement.querySelector(".drop-zone__prompt");
		this.iconElement = dropZoneElement.querySelector(".drop-zone__icon");
		this.thumbnailEnabled = thumbnailEnabled; // Control whether thumbnail functionality is enabled

		// Set up event listeners to handle user interactions
		this.setupEventListeners();
	}

	setupEventListeners() {
		// Clicking on the drop zone opens the file selection dialog
		this.dropZoneElement.addEventListener("click", (e) => {
			this.inputElement.click();
		});

		// Handle the file selection and update the thumbnail (if enabled)
		this.inputElement.addEventListener("change", () => {
			if (this.inputElement.files.length) {
				this.promptElement.innerText = this.inputElement.files[0].name;
				if (this.thumbnailEnabled) {
					this.updateThumbnail(this.inputElement.files[0]);
				}
			}
		});

		// Handle drag-and-drop events for file selection
		this.dropZoneElement.addEventListener("dragover", (e) => {
			e.preventDefault();
			this.dropZoneElement.classList.add("drop-zone--over");
		});

		// Handle drag-leave and drag-end events to remove the visual highlight
		["dragleave", "dragend"].forEach((type) => {
			this.dropZoneElement.addEventListener(type, () => {
				this.dropZoneElement.classList.remove("drop-zone--over");
			});
		});

		// Handle dropping files onto the drop zone
		this.dropZoneElement.addEventListener("drop", (e) => {
			console.log("dropzone drop event");
			e.preventDefault();

			if (e.dataTransfer.files.length) {
				this.inputElement.files = e.dataTransfer.files;
				if (this.thumbnailEnabled) {
					this.updateThumbnail(e.dataTransfer.files[0]);
				}
				this.promptElement.innerText = this.inputElement.files[0].name;
			}

			// Remove the visual highlight
			this.dropZoneElement.classList.remove("drop-zone--over");
		});
	}

	// Update the thumbnail for the selected file (if enabled)
	updateThumbnail(file) {
		if (this.promptElement) {
			this.promptElement.remove();
		}

		if (!this.thumbnailElement) {
			this.thumbnailElement = document.createElement("div");
			this.thumbnailElement.classList.add("drop-zone__thumb");
			this.dropZoneElement.appendChild(this.thumbnailElement);
		}

		// Set the label for the thumbnail
		this.thumbnailElement.dataset.label = file.name;

		// Show a thumbnail image for image files (if enabled)
		if (this.thumbnailEnabled && file.type.startsWith("image/")) {
			const reader = new FileReader();

			reader.readAsDataURL(file);
			reader.onload = () => {
				this.thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
			};
		} else {
			this.thumbnailElement.style.backgroundImage = null;
		}
	}
}
