export async function getUserEmails(user_id) {
	const url = `/users/${user_id}/emails`;
	try {
		const response = await fetch(url, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});

		if (!response.ok) {
			throw new Error(`Failed to retrieve user emails. Status code: ${response.status}`);
		}

		const emails = await response.json();
		console.log(`For the user with the id ${user_id}, got the following emails:`);
		console.dir(emails);
		return emails;
	} catch (error) {
		console.error(error);
	}
}
