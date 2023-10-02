document.addEventListener("DOMContentLoaded", async () => {
	const emailListElement = document.querySelector("#email-list");
	const emailList = await getEmailList();
	emailList.forEach((email) => {
		let li = document.createElement("li");
		let emailElement = document.createElement("a");
		emailElement.text = email;
		emailElement.href = `email/get/json/?name=${email}`;
		li.appendChild(emailElement);
		emailListElement.appendChild(li);
	});
});

async function getEmailList() {
	let response = await fetch("email/list");
	return await response.json();
}
