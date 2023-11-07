export async function getEmailAmount(user_id) {
	const url = `/users/${user_id}/emails`;
	try {
		const response = await fetch(url, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});

		if (!response.ok) {
			throw new Error(`Failed to retrieve user data. Status code: ${response.status}`);
		}

		const userData = await response.json();
		return userData.length;
	} catch (error) {
		console.error(error);
	}
}
