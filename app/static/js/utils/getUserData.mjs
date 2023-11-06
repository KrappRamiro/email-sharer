export async function getUserData(user_id) {
	const url = `/users/${user_id}`;
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
		console.log(userData);
		return userData;
	} catch (error) {
		console.error(error);
	}
}
